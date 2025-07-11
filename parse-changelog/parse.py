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
            'Files': files
        })

    return results

file_path = 'package-list'
parsed_entries = parse_debian_apt_source_index_file(file_path)
for entry in parsed_entries:
    print(entry)
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
                for entry in cl:
                    print(entry.version, entry.distributions, entry.urgency)
                    for c in entry.changes():
                        print(c)
    elif entry['Format'] == "3.0 (native)":
        pass
    elif entry['Format'] == "1.0":
        pass
