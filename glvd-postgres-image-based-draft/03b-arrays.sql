CREATE TABLE image_variantB (
    id            serial PRIMARY KEY,
    name          text NOT NULL UNIQUE,        -- e.g. 'gcp-gardener_prod-arm64-1592.4-deadbeef'
    packages      text[] NOT NULL DEFAULT '{}' -- list of source package names
);

-- GIN index for fast array ops (&&, @>, <@, =, etc.)
CREATE INDEX idx_image_variantB_packages_gin ON image_variantB USING GIN (packages);

-- optional: materialized / cached package count for quick cardinality checks
ALTER TABLE image_variantB
    ADD COLUMN package_count int GENERATED ALWAYS AS (cardinality(packages)) STORED;
CREATE INDEX idx_image_variantB_package_count ON image_variantB (package_count);

INSERT INTO image_variantB (name, packages) VALUES
    ('gcp-gardener_prod-amd64-1592.4-deadbeef', ARRAY['python3.12', 'rsync', 'jinja2']),
    ('aws-gardener_prod-amd64-1592.4-beefdead', ARRAY['python3.13', 'python3.12', 'rsync']);

CREATE VIEW public.sourcepackagecve_b AS
SELECT DISTINCT
  ac.cve_id,
  dc.deb_source   AS source_package_name,
  dc.deb_version  AS source_package_version,
  dpc.cpe_version AS gardenlinux_version,
  ((dc.debsec_vulnerable AND (cc.is_resolved IS NOT TRUE)) = true) AS is_vulnerable,
  dc.debsec_vulnerable
FROM public.all_cve    ac
JOIN public.deb_cve    dc USING (cve_id)
JOIN public.dist_cpe   dpc ON dc.dist_id = dpc.id
LEFT JOIN public.cve_context cc USING (cve_id, dist_id)
JOIN public.image_variantB iv
  ON iv.packages @> ARRAY[dc.deb_source]::text[]
WHERE 
    -- iv.name = 'gcp-gardener_prod-amd64-1592.4-deadbeef' AND 
  dpc.cpe_product = 'gardenlinux'
  AND dc.debsec_vulnerable = true
  AND dc.deb_source <> 'linux';
