-- stmt_cpe_version
SELECT
    *
FROM
    all_cve
    INNER JOIN deb_cve USING (cve_id)
    INNER JOIN dist_cpe ON (deb_cve.dist_id = dist_cpe.id)
WHERE
    dist_cpe.cpe_vendor = 'debian'
    AND dist_cpe.cpe_product = 'debian_linux'
    AND dist_cpe.deb_codename = 'bookworm'
    AND COALESCE(deb_cve.cvss_severity, 0) >= 5.0
    AND deb_cve.deb_source = 'capnproto'
    AND (
        deb_cve.deb_version_fixed > '0.0.0'
        OR deb_cve.deb_version_fixed IS NULL
    )
ORDER BY
    all_cve.cve_id
