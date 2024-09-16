-- View: public.sourcepackagecve

-- DROP VIEW public.sourcepackagecve;

CREATE OR REPLACE VIEW public.sourcepackagecve
 AS
 SELECT all_cve.cve_id AS cve_id,
    deb_cve.deb_source AS source_package_name,
    deb_cve.deb_version AS source_package_version,
    dist_cpe.cpe_version AS gardenlinux_version,
    deb_cve.debsec_vulnerable AS is_vulnerable,
    all_cve.data ->> 'published'::text AS cve_published_date,
    (data->'metrics'->'cvssMetricV40'->0->'cvssData'->>'baseScore')::numeric AS base_score_v40,
    (data->'metrics'->'cvssMetricV31'->0->'cvssData'->>'baseScore')::numeric AS base_score_v31,
    (data->'metrics'->'cvssMetricV30'->0->'cvssData'->>'baseScore')::numeric AS base_score_v30,
    (data->'metrics'->'cvssMetricV40'->0->'cvssData'->>'vectorString')::text AS vector_string_v40,
    (data->'metrics'->'cvssMetricV31'->0->'cvssData'->>'vectorString')::text AS vector_string_v31,
    (data->'metrics'->'cvssMetricV30'->0->'cvssData'->>'vectorString')::text AS vector_string_v30
   FROM all_cve
     JOIN deb_cve USING (cve_id)
     JOIN dist_cpe ON deb_cve.dist_id = dist_cpe.id
  WHERE dist_cpe.cpe_product = 'gardenlinux'::text
  ORDER BY all_cve.cve_id;

ALTER TABLE public.sourcepackagecve
    OWNER TO glvd;

-- View: public.sourcepackage

-- DROP VIEW public.sourcepackage;

CREATE OR REPLACE VIEW public.sourcepackage
 AS
 SELECT debsrc.deb_source AS source_package_name,
    debsrc.deb_version AS source_package_version,
    dist_cpe.cpe_version AS gardenlinux_version
   FROM debsrc
     JOIN dist_cpe ON debsrc.dist_id = dist_cpe.id
  WHERE dist_cpe.cpe_product = 'gardenlinux'::text;

ALTER TABLE public.sourcepackage
    OWNER TO glvd;
