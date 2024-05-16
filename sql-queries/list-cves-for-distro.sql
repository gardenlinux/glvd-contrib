SELECT
    deb_cve.deb_source, deb_cve.cvss_severity, deb_cve.cve_id 
FROM
    all_cve
    INNER JOIN deb_cve USING (cve_id)
    INNER JOIN dist_cpe ON (deb_cve.dist_id = dist_cpe.id)
WHERE
    dist_cpe.cpe_vendor = 'debian'
    AND dist_cpe.cpe_product = 'debian_linux'
    AND dist_cpe.deb_codename = 'trixie'
    AND deb_cve.debsec_vulnerable = TRUE
    AND COALESCE(deb_cve.cvss_severity, 0) >= 5.0
