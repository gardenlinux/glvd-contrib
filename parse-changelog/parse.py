import logging
from debian import changelog
import re
import requests
import lzma
import tarfile
import io
import json
import tempfile
import gzip
import shutil

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def parse_debian_apt_source_index_file(file_path):
    logger.debug(f"Parsing Debian APT source index file: {file_path}")
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        logger.error(f"Failed to read file {file_path}: {e}")
        raise

    entries = re.split(r'\n\s*\n', content.strip())
    results = []

    for entry in entries:
        lines = entry.strip().split('\n')
        format_ = None
        directory = None
        files = []
        in_files_section = False

        for line in lines:
            if line.startswith('Format:'):
                format_ = line.split(':', 1)[1].strip()
            elif line.startswith('Directory:'):
                directory = line.split(':', 1)[1].strip()
            elif line.startswith('Package:'):
                package = line.split(':', 1)[1].strip()
            elif line.startswith('Files:'):
                in_files_section = True
            elif in_files_section:
                if line.strip() == '':
                    continue
                if line.startswith(' ') or line.startswith('\t'):
                    files.append(line.strip())
                else:
                    in_files_section = False

        # We have special handling for the kernel because we don't use debian's build for that
        if package != 'linux':
            results.append({
                'Format': format_,
                'Directory': directory,
                'Files': files,
                'Package': package
            })

    logger.debug(f"Parsed {len(results)} entries from source index file")
    return results

def add_cve_entry(resolved_cves, cve_id, package_name, changelog_text):
    logger.debug(f"Adding CVE entry: {cve_id} for package {package_name}")
    if cve_id not in resolved_cves:
        resolved_cves[cve_id] = {}
    if package_name not in resolved_cves[cve_id]:
        resolved_cves[cve_id][package_name] = []
    resolved_cves[cve_id][package_name].append(changelog_text)

def do_work(file_path):
    logger.info(f"Processing source index file: {file_path}")
    parsed_entries = parse_debian_apt_source_index_file(file_path)
    logger.info(f"Found {len(parsed_entries)} entries in source index file")
    for entry in parsed_entries:
        logger.debug(f"Processing entry: {entry.get('Package', 'unknown')}")
        if entry['Format'] == "3.0 (quilt)":
            debian_tar_xz_file = next((f.split(' ')[2] for f in entry['Files'] if f.endswith('debian.tar.xz')), '')
            if debian_tar_xz_file != '':
                url = f"https://packages.gardenlinux.io/gardenlinux/{entry['Directory']}/{debian_tar_xz_file}"
                logger.debug(f"Downloading debian.tar.xz from {url}")
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                except Exception as e:
                    logger.error(f"Failed to download {url}: {e}")
                    continue

                try:
                    decompressed = lzma.decompress(response.content)
                except Exception as e:
                    logger.error(f"Failed to decompress xz file for {entry['Package']}: {e}")
                    continue

                try:
                    with tarfile.open(fileobj=io.BytesIO(decompressed)) as tar:
                        changelog_member = tar.getmember("debian/changelog")
                        changelog_file = tar.extractfile(changelog_member)
                        changelog_content = changelog_file.read().decode("utf-8")
                        cl = changelog.Changelog(changelog_content)
                        for changelog_entry in cl:
                            for change in changelog_entry.changes():
                                for cve in vulnerable_cves:
                                    cve = str.strip(cve)
                                    if cve in change:
                                        add_cve_entry(resolved_cves, cve, entry['Package'], change)
                except Exception as e:
                    logger.error(f"Failed to extract or parse changelog for {entry['Package']}: {e}")
                    continue
        elif entry['Format'] == "3.0 (native)":
            logger.debug(f"Skipping native format for {entry.get('Package', 'unknown')}")
            pass
        elif entry['Format'] == "1.0":
            logger.debug(f"Skipping format 1.0 for {entry.get('Package', 'unknown')}")
            pass

    try:
        with open('resolved_cves.json', 'w') as f:
            json.dump(resolved_cves, f, indent=2)
        logger.info("Wrote resolved CVEs to resolved_cves.json")
    except Exception as e:
        logger.error(f"Failed to write resolved_cves.json: {e}")

def download_and_extract_sources(gl_version, tmpdir):
    sources_url = f"https://packages.gardenlinux.io/gardenlinux/dists/{gl_version}/main/source/Sources.gz"
    logger.info(f"Downloading Sources.gz from {sources_url}")
    try:
        response = requests.get(sources_url, stream=True)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to download Sources.gz: {e}")
        raise
    
    gz_path = f"{tmpdir}/Sources.gz"
    sources_path = f"{tmpdir}/Sources"
    try:
        with open(gz_path, "wb") as f:
            shutil.copyfileobj(response.raw, f)
        with gzip.open(gz_path, "rb") as f_in, open(sources_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        logger.info(f"Downloaded and extracted Sources.gz to {sources_path}")
        return sources_path
    except Exception as e:
        logger.error(f"Failed to extract Sources.gz: {e}")
        raise

def main():
    gl_version = '1877.1'
    global vulnerable_cves
    global resolved_cves
    resolved_cves = {}

    cves_url = f"https://glvd.ingress.glvd.gardnlinux.shoot.canary.k8s-hana.ondemand.com/v1/cves/{gl_version}"
    logger.info(f"Fetching vulnerable CVEs from {cves_url}")
    try:
        response = requests.get(cves_url)
        response.raise_for_status()
        vulnerable_cves = [item["cveId"] for item in response.json() if item.get("vulnerable") == True]
        logger.info(f"Fetched {len(vulnerable_cves)} vulnerable CVEs")
    except Exception as e:
        logger.error(f"Failed to fetch CVEs: {e}")
        return

    with tempfile.TemporaryDirectory() as tmpdir:

        sources_path = download_and_extract_sources(gl_version, tmpdir)
        do_work(sources_path)

if __name__ == "__main__":
    main()
