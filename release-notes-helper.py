import requests


# just a proof of concept, don't judge the code

version = 'today'
previous_version = '1592.4'



url = f"https://glvd.ingress.glvd.gardnlinux.shoot.canary.k8s-hana.ondemand.com/v1/cves/{version}"
cves_new = requests.get(url)
foo = cves_new.json()

url_previous = f"https://glvd.ingress.glvd.gardnlinux.shoot.canary.k8s-hana.ondemand.com/v1/cves/{previous_version}"
cves_old = requests.get(url_previous)
bar = cves_old.json()


list_cves_new = [{'cveId': x['cveId'], 'sourcePackageName': x['sourcePackageName'], 'sourcePackageVersion': x['sourcePackageVersion']} for x in foo]
list_cves_old = [{'cveId': x['cveId'], 'sourcePackageName': x['sourcePackageName'], 'sourcePackageVersion': x['sourcePackageVersion']} for x in bar]



diff = list(set([x['cveId'] for x in list_cves_old]) - set([x['cveId'] for x in list_cves_new]))

print(diff)

for cve in diff:
    for x in list_cves_old:
        if x['cveId'] == cve:
            print(x)

