-- View: public.sourcepackagecve

-- DROP VIEW public.sourcepackagecve;

CREATE OR REPLACE VIEW public.sourcepackagecve
 AS
 SELECT ((all_cve.cve_id || deb_cve.deb_source) || deb_cve.deb_version::text) || dist_cpe.cpe_version AS my_id,
    all_cve.cve_id,
    deb_cve.deb_source AS source_package_name,
    deb_cve.deb_version AS source_package_version,
    dist_cpe.cpe_version AS gardenlinux_version,
    deb_cve.debsec_vulnerable AS is_vulnerable,
    all_cve.data ->> 'published'::text AS cve_published_date
   FROM all_cve
     JOIN deb_cve USING (cve_id)
     JOIN dist_cpe ON deb_cve.dist_id = dist_cpe.id
  WHERE dist_cpe.cpe_product = 'gardenlinux'::text
  ORDER BY all_cve.cve_id;

ALTER TABLE public.sourcepackagecve
    OWNER TO glvd;

