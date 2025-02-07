import os
import sys
import json

"""
Parses files from git.kernel.org/pub/scm/linux/kernel/git/lee/vulns.git/cve/published to identify fixed kernel CVEs.
"""

current_maintained_kernels = ['6.6', '6.12']

def process_line(line):
    parts = line.strip().split(':')
    if len(parts) == 4:
        kernel_version = parts[2]
        commit_id = parts[3]
        if kernel_version == '0':
            return None, None
        return kernel_version, commit_id
    return None, None

def read_file(filepath):
    kernel_versions = {}
    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            kernel_version, commit_id = process_line(line)
            if kernel_version:
                for k in current_maintained_kernels:
                    if kernel_version.startswith(k):
                        kernel_versions[kernel_version] = commit_id
    return kernel_versions

def process_directory(directory):
    cve_data = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('dyad'):
                filepath = os.path.join(root, file)
                kernel_versions = read_file(filepath)
                cve_name = file.replace('.dyad', '')
                if kernel_versions:
                    cve_data[cve_name] = kernel_versions

    return cve_data

if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit(1)

    directory_to_process = sys.argv[1]
    cve_data = process_directory(directory_to_process)
    print(json.dumps(cve_data, indent="  "))
