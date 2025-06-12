SELECT
    debsec_cve.cve_id,
    debsrc.deb_source,
    debsrc.deb_version,
    debsec_cve.deb_version_fixed,
    COALESCE(debsrc.deb_version < debsec_cve.deb_version_fixed, TRUE) AS debsec_vulnerable,
    COALESCE(
        CASE WHEN split_part(debsrc.deb_version::text, '.', 2) <> ''
            AND split_part(debsec_cve.deb_version_fixed::text, '.', 2) <> ''
            AND split_part(debsrc.deb_version::text, '.', 2) = split_part(debsec_cve.deb_version_fixed::text, '.', 2) THEN
            debsrc.deb_version < debsec_cve.deb_version_fixed
        ELSE
            NULL
        END, TRUE) AS debsec_vulnerable2,
    debsec_note
FROM
    debsrc
    LEFT OUTER JOIN debsec_cve ON debsec_cve.deb_source = debsrc.deb_source
INNER JOIN nvd_cve ON nvd_cve.cve_id = debsec_cve.cve_id
WHERE
    debsrc.dist_id = 21
