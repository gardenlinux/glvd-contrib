The purpose of this directory is to draft and store SQL queries that are useful for GLVD.

Queries can be mapped to user stories / personas.

Draft notes

## issue [#88](https://github.com/gardenlinux/glvd/issues/88)
given:
 - CVE-ID
 - Garden linux version

want:
 - is fixed?

how to find out?

if cve-id in deb_cve:
 - take source package from deb_cve
 - check deb_version_fixed
 - take version of that source package in given gl version
 - compare version
 - fixed if version-we-have >= deb_version_fixed

sample vulnerable

```sql
SELECT
    all_cve.cve_id , deb_cve.deb_source , deb_cve.deb_version , deb_cve.deb_version_fixed , deb_cve.debsec_vulnerable , deb_cve.cvss_severity  
FROM
    all_cve
    INNER JOIN deb_cve USING (cve_id)
    INNER JOIN dist_cpe ON (deb_cve.dist_id = dist_cpe.id)
WHERE
    dist_cpe.cpe_vendor = 'sap'
    AND dist_cpe.cpe_product = 'gardenlinux'
    AND dist_cpe.deb_codename = '1592.0'
    AND all_cve.cve_id = 'CVE-2024-8088'
```

sample fixed:

```sql
SELECT
    all_cve.cve_id , deb_cve.deb_source , deb_cve.deb_version , deb_cve.deb_version_fixed , deb_cve.debsec_vulnerable, deb_cve.cvss_severity   
FROM
    all_cve
    INNER JOIN deb_cve USING (cve_id)
    INNER JOIN dist_cpe ON (deb_cve.dist_id = dist_cpe.id)
WHERE
    dist_cpe.cpe_vendor = 'sap'
    AND dist_cpe.cpe_product = 'gardenlinux'
    AND dist_cpe.deb_codename = '1592.0'
    AND all_cve.cve_id = 'CVE-2022-40303'
```


else:
 - search cpe in all_cpe
 - try to match cpe to one or multiple source packages

## issue [#87](https://github.com/gardenlinux/glvd/issues/87)
given:
 - Garden Linux version

want:
 - How many and with CVE should I care about?

```sql
SELECT
    all_cve.cve_id , deb_cve.deb_source , deb_cve.deb_version , deb_cve.deb_version_fixed , deb_cve.debsec_vulnerable , deb_cve.cvss_severity  
FROM
    all_cve
    INNER JOIN deb_cve USING (cve_id)
    INNER JOIN dist_cpe ON (deb_cve.dist_id = dist_cpe.id)
WHERE
    dist_cpe.cpe_vendor = 'sap'
    AND dist_cpe.cpe_product = 'gardenlinux'
    AND dist_cpe.deb_codename = '1592.0'
    AND deb_cve.debsec_vulnerable = TRUE 
```


## issue [#76](https://github.com/gardenlinux/glvd/issues/76)
given:
 - A source package "busybox"

want:
 - How many and with CVE should I care about?

how to find out?

```sql
SELECT
    all_cve.cve_id , deb_cve.deb_source , deb_cve.deb_version , deb_cve.deb_version_fixed , deb_cve.debsec_vulnerable , deb_cve.cvss_severity  
FROM
    all_cve
    INNER JOIN deb_cve USING (cve_id)
    INNER JOIN dist_cpe ON (deb_cve.dist_id = dist_cpe.id)
WHERE
    dist_cpe.cpe_vendor = 'sap'
    AND dist_cpe.cpe_product = 'gardenlinux'
    AND dist_cpe.deb_codename = '1592.0'
    AND deb_cve.debsec_vulnerable = TRUE 
    AND deb_cve.deb_source = 'busybox'
```
