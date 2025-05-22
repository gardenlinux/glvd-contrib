import argparse
import gzip
import io
import sys
import requests
from debian.debian_support import Version

SECURITY_TRACKER_JSON = "https://security-tracker.debian.org/tracker/data/json"
CURRENT_SOURCES_URL = "http://deb.debian.org/debian/dists/testing/main/source/Sources.gz"
SNAPSHOT_URL_TEMPLATE = "https://snapshot.debian.org/archive/debian/{date}/dists/testing/main/source/Sources.gz"

def get_cve_info(cve_id):
    print(f"Fetching CVE info for {cve_id} from Debian Security Tracker...")
    resp = requests.get(SECURITY_TRACKER_JSON)
    resp.raise_for_status()
    data = resp.json()
    cve_data = data['glibc'][cve_id]
    if not cve_data:
        print(f"CVE {cve_id} not found in Security Tracker.")
        sys.exit(1)
    # Find all affected packages and their fixed versions in testing
    results = []
    print(cve_data)
    releases = cve_data.get("releases", {})
    print(releases)
    testing = releases.get("trixie")
    print(testing)
    if testing:
        fixed_version = testing.get("fixed_version")
        status = testing.get("status")
        results.append(('glibc', fixed_version, status))
    if not results:
        print(f"No testing release info found for {cve_id}.")
        sys.exit(1)
    return results

def get_sources_gz(date=None):
    if date:
        # Format: YYYYMMDDTHHMMSSZ, e.g. 20240501T000000Z
        url = SNAPSHOT_URL_TEMPLATE.format(date=date)
    else:
        url = CURRENT_SOURCES_URL
    print(f"Downloading Sources.gz from: {url}")
    resp = requests.get(url)
    resp.raise_for_status()
    return gzip.decompress(resp.content).decode("utf-8")

def parse_sources(sources_text, package):
    versions = []
    current_pkg = None
    for line in sources_text.splitlines():
        if line.startswith("Package: "):
            current_pkg = line.split(":", 1)[1].strip()
        elif line.startswith("Version: ") and current_pkg == package:
            ver = line.split(":", 1)[1].strip()
            versions.append(ver)
    return versions

def main():
    parser = argparse.ArgumentParser(description="Find fixed versions for a CVE in Debian testing.")
    parser.add_argument("cve_id", help="CVE ID (e.g. CVE-2024-33601)")
    parser.add_argument("--date", help="Snapshot date (YYYYMMDDTHHMMSSZ) for historical testing, e.g. 20240501T000000Z")
    args = parser.parse_args()

    cve_info = get_cve_info(args.cve_id)
    sources_text = get_sources_gz(args.date)

    print(cve_info)
    for package, fixed_version, status in cve_info:
        print(f"\nPackage: {package}")
        print(f"  Fixed version in testing: {fixed_version or '(not yet fixed)'} (status: {status})")
        versions = parse_sources(sources_text, package)
        print(versions)
        if not versions:
            print("  No versions found in testing at this time.")
            continue
        print("  Versions in testing at this time:")
        for ver in sorted(versions, key=Version):
            ver_minor = ver.split('-')[0]
            print(ver_minor)
            fixed_minor = fixed_version.split('-')[0] if fixed_version else None
            if ver_minor == fixed_minor:
                if fixed_version and Version(ver) >= Version(fixed_version):
                    print(ver)
                else:
                    print(f"{ver} not fixed")

if __name__ == "__main__":
    main()
