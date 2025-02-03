import requests

# just a proof of concept, don't judge the code

version = '1592.5'
previous_version = '1592.4'

url = f"https://glvd.ingress.glvd.gardnlinux.shoot.canary.k8s-hana.ondemand.com/v1/cves/{version}"
cves_new = requests.get(url).json()

url_previous = f"https://glvd.ingress.glvd.gardnlinux.shoot.canary.k8s-hana.ondemand.com/v1/cves/{previous_version}"
cves_old = requests.get(url_previous).json()

list_cves_new = [{'cveId': cve['cveId'], 'sourcePackageName': cve['sourcePackageName'], 'sourcePackageVersion': cve['sourcePackageVersion']} for cve in cves_new]
list_cves_old = [{'cveId': cve['cveId'], 'sourcePackageName': cve['sourcePackageName'], 'sourcePackageVersion': cve['sourcePackageVersion']} for cve in cves_old]

diff = list(set([x['cveId'] for x in list_cves_old]) - set([x['cveId'] for x in list_cves_new]))

# print(diff)


url = f"https://glvd.ingress.glvd.gardnlinux.shoot.canary.k8s-hana.ondemand.com/v1/distro/{version}"

new_version_numbers = requests.get(url).json()



packages = []
packages_to_fix_mapping = {}

for cve in diff:
    for package_name in list_cves_old:
        if package_name['cveId'] == cve:
            # print(package_name)
            pkg = package_name['sourcePackageName']
            packages.append(pkg)
            # print(pkg)
            if pkg in packages_to_fix_mapping:
                packages_to_fix_mapping[pkg]['fixes'].append(cve)
            else:
                for v in new_version_numbers:
                    if pkg == v['sourcePackageName']:
                        version_new = v['sourcePackageVersion']
                        version_old = package_name['sourcePackageVersion']
                        packages_to_fix_mapping[pkg] = {'fixes': [cve], 'version': version_new, 'version_old': version_old}

packages = set(sorted(packages))
# print(packages)
# print(packages_to_fix_mapping)

print('The following packages have been upgraded, to address the mentioned CVEs:')
for package_name in packages_to_fix_mapping.keys():
    package = packages_to_fix_mapping[package_name]
    print(f"- upgrade '{package_name}' from `{package['version_old']}` to `{package['version']}`")
    for cve in package['fixes']:
        print(f'  - {cve}')
