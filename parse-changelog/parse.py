from debian import changelog
import re
import requests
import lzma
import tarfile
import io

def parse_debian_apt_source_index_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Split entries by blank lines
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
                # Assuming files are indented (e.g., start with spaces or tabs)
                if line.strip() == '':
                    continue
                if line.startswith(' ') or line.startswith('\t'):
                    files.append(line.strip())
                else:
                    # End of files section if not indented
                    in_files_section = False

        results.append({
            'Format': format_,
            'Directory': directory,
            'Files': files,
            'Package': package
        })

    return results


vulnerable_cves = []
with open('vulnerable-cves') as file:
    vulnerable_cves = file.readlines()

print(vulnerable_cves)

resolved_cves = {}


def add_cve_entry(resolved_cves, cve_id, package_name, changelog_text):
    if cve_id not in resolved_cves:
        resolved_cves[cve_id] = {}
    if package_name not in resolved_cves[cve_id]:
        resolved_cves[cve_id][package_name] = []
    resolved_cves[cve_id][package_name].append(changelog_text)

file_path = 'package-list'
parsed_entries = parse_debian_apt_source_index_file(file_path)
for entry in parsed_entries:
    
    index = 0
    # print(entry)
    if entry['Format'] == "3.0 (quilt)":

        debian_tar_xz_file = next((f.split(' ')[2] for f in entry['Files'] if f.endswith('debian.tar.xz')), '')

        if debian_tar_xz_file != '':
            url = f"https://packages.gardenlinux.io/gardenlinux/{entry['Directory']}/{debian_tar_xz_file}"

            # Download the file
            response = requests.get(url)
            response.raise_for_status()

            # Decompress xz
            decompressed = lzma.decompress(response.content)

            # Open as tar archive
            with tarfile.open(fileobj=io.BytesIO(decompressed)) as tar:
                changelog_member = tar.getmember("debian/changelog")
                changelog_file = tar.extractfile(changelog_member)
                changelog_content = changelog_file.read().decode("utf-8")
                # print(changelog_content)
                cl = changelog.Changelog(changelog_content)
                for changelog_entry in cl:
                    # with open(f"temp/{entry['Package']}{index}.txt", "w") as out_file:
                    #     out_file.write('\n'.join(changelog_entry.changes()))
                    # index = index + 1
                    
                    for c in changelog_entry.changes():
                        for cve in vulnerable_cves:
                            cve = str.strip(cve)
                            # # print(f'\n\n{cve} in {entry['Package']}')
                            # xx: list = resolved_cves.get(cve, [])
                            # xx.append(entry['Package'])
                            # resolved_cves[cve] = xx
                            # # print(resolved_cves)
                            if cve in c:
                                add_cve_entry(resolved_cves, cve, entry['Package'], c)
                                
                                print(resolved_cves)
                    
                    
                    
                    # print(entry.version, entry.distributions, entry.urgency)
                    # for c in changelog_entry.changes():
                    #     # print(c)
                    #     packagename = entry['Package']
                    #     filename = f"temp/{packagename}{index}.txt"
                    #     index = index + 1
                    #     with open(filename, "w") as out_file:
                    #         out_file.write(c)
    elif entry['Format'] == "3.0 (native)":
        pass
    elif entry['Format'] == "1.0":
        pass


print(resolved_cves)
