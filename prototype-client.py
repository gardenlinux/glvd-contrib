import subprocess
import requests

def convert_binary_package_name_to_source_package_name(binary_package_name):
    apt_cache_show = subprocess.run(['apt-cache', 'show', binary_package_name], capture_output=True)
    apt_cache_show_stdout = apt_cache_show.stdout.decode("utf-8")

    apt_cache_show_lines = apt_cache_show_stdout.splitlines()
    apt_cache_show_lines_filtered = [line for line in apt_cache_show_lines if line.startswith('Source')]

    # No 'Source:' means the binary package name is the source package name
    if len(apt_cache_show_lines_filtered) == 0:
        binary_package_lines = [line for line in apt_cache_show_lines if line.startswith('Package')]
        if len(binary_package_lines) == 0:
            return binary_package_name
        if len(binary_package_lines) > 1:
            print('warning: multiple package names')
        return binary_package_lines[0].split(' ')[1]

    # print(apt_cache_show_lines_filtered)
    # assert len(apt_cache_show_lines_filtered) == 1
    if len(apt_cache_show_lines_filtered) > 1:
        print("warning: multiple source lines")
        print(apt_cache_show_lines_filtered)

    apt_cache_show_source_line = apt_cache_show_lines_filtered[0]

    source_package_name = apt_cache_show_source_line.split(' ')[1]

    return source_package_name


query_out = subprocess.run(['dpkg-query', '--list', '--no-pager'], capture_output=True).stdout.decode("utf-8")
lines = [line for line in query_out.splitlines() if line.startswith('ii')]

binary_package_names = [line.split(" ")[2] for line in lines]
source_package_names = list(set([convert_binary_package_name_to_source_package_name(binary_package_name) for binary_package_name in binary_package_names]))

print(source_package_names)

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

params = {
    'sortBy': 'cveId',
    'sortOrder': 'ASC',
}

json_data = {
    'packageNames': source_package_names,
}

response = requests.put(
    'https://glvd.ingress.glvd.gardnlinux.shoot.canary.k8s-hana.ondemand.com/v1/cves/1592.0/packages',
    params=params,
    headers=headers,
    json=json_data,
)

print(response)
print(response.text)
