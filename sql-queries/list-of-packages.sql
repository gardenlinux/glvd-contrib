SELECT
    *
FROM
    all_cve
    INNER JOIN deb_cve USING (cve_id)
    INNER JOIN dist_cpe ON (deb_cve.dist_id = dist_cpe.id)
WHERE
    dist_cpe.cpe_vendor = 'sap'
    AND dist_cpe.cpe_product = 'gardenlinux'
    AND dist_cpe.deb_codename = '1443'
    AND deb_cve.deb_source = ANY(ARRAY ['firefox-esr', 'vim'])
ORDER BY
    all_cve.cve_id
