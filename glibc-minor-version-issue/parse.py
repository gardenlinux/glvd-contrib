import json
from collections import defaultdict

# Script to collect as much information as possible regarding vulnerabilities for various minor versions of debian packages.
# We need this to address https://github.com/gardenlinux/glvd/issues/149

def extract_minor_version(version_str):
    """
    Extracts the minor version (e.g., '2.36' from '2.36-9+deb12u7').
    Returns None if not found.
    """
    if not version_str or version_str == "0":
        return None
    parts = version_str.split('-')[0].split('.')
    if len(parts) >= 2:
        return '.'.join(parts[:2])
    return None

with open('json', 'r') as f:
    data = json.load(f)

# Structure: {component: {CVE: {minor_version: [release_info, ...]}}}
result = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

for package, package_data in data.items():
    for key, value in package_data.items():
        if key.startswith("CVE-"):
            cve_id = key
            cve_obj = value
            releases = cve_obj.get("releases", {})
            for release_name, release_info in releases.items():
                fixed_version = release_info.get("fixed_version")
                minor_version = extract_minor_version(fixed_version)
                if minor_version:
                    entry = {
                        "package": package,
                        "release": release_name,
                        "fixed_version": fixed_version,
                        "status": release_info.get("status"),
                        "urgency": release_info.get("urgency"),
                        "repositories": release_info.get("repositories", {})
                    }
                    result[package][cve_id][minor_version].append(entry)

output = {}

# Example output: print all fixed versions per CVE, grouped by minor version
for component, cves in result.items():
    # print(f"Component: {component}")
    output[component] = {}
    for cve_id, minors in cves.items():
        # print(f"  {cve_id}:")
        # Only consider cases where we have fixed versions for more than one minor version
        # All other cases are unambiguous anyways
        if len(minors) > 1:
            output[component][cve_id] = {}
            for minor_version, entries in minors.items():
                # print(f"    Minor version {minor_version}:")
                output[component][cve_id][str(minor_version)] = {}
                output[component][cve_id][str(minor_version)]['fixed_versions'] = []
                for entry in entries:
                    # print(f"      Release: {entry['release']}, Fixed version: {entry['fixed_version']}, Status: {entry['status']}, Urgency: {entry['urgency']}")
                    output[component][cve_id][str(minor_version)]['fixed_versions'].append(entry['fixed_version'])
    # print()

print(json.dumps(output, indent=2))
