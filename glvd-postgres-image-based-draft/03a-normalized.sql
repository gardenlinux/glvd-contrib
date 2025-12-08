-- canonical normalized table
CREATE TABLE image_variantA (
  id bigserial PRIMARY KEY,
  image_name text NOT NULL,         -- renamed from cname
  image_version text NOT NULL,            -- new field for version
  commit_id text,                   -- new field for commit id
  metadata jsonb DEFAULT '{}'       -- optional
);

CREATE TABLE image_package (
  image_variantA_id bigint NOT NULL REFERENCES image_variantA(id) ON DELETE CASCADE,
  package_name text NOT NULL,
  PRIMARY KEY (image_variantA_id, package_name)
);

CREATE INDEX idx_image_package_package ON image_package (package_name);
CREATE INDEX idx_image_package_image ON image_package (image_variantA_id);

-- optional denormalized cache for fast set ops
ALTER TABLE image_variantA ADD COLUMN packages text[] DEFAULT '{}'::text[];
CREATE INDEX idx_image_variantA_packages_gin ON image_variantA USING GIN (packages);

-- Insert data with separated version and commit_id, and image_name without version/commit
INSERT INTO image_variantA (image_name, image_version, commit_id, packages) VALUES
  ('gcp-gardener_prod', '1592.4', 'deadbeef', ARRAY['python3.12', 'rsync', 'jinja2']),
  ('aws-gardener_prod', '1592.4', 'beefdead', ARRAY['python3.13', 'python3.12', 'rsync']);

INSERT INTO image_package (image_variantA_id, package_name)
SELECT id, unnest(packages)
FROM image_variantA;



CREATE VIEW public.sourcepackagecve_a AS
SELECT DISTINCT
  ac.cve_id,
  dc.deb_source   AS source_package_name,
  dc.deb_version  AS source_package_version,
  dpc.cpe_version AS gardenlinux_version,
  ((dc.debsec_vulnerable AND (cc.is_resolved IS NOT TRUE)) = true) AS is_vulnerable,
  dc.debsec_vulnerable,
  iv.image_name,
  iv.image_version,
  iv.commit_id
FROM public.all_cve     ac
JOIN public.deb_cve     dc USING (cve_id)
JOIN public.dist_cpe    dpc ON dc.dist_id = dpc.id
LEFT JOIN public.cve_context cc USING (cve_id, dist_id)
-- join to image_package -> image_variantA to restrict to packages in the image
JOIN public.image_package ip ON ip.package_name = dc.deb_source
JOIN public.image_variantA   iv ON iv.id = ip.image_variantA_id
-- join dpc.cpe_version on iv.image_version
WHERE 
  dpc.cpe_product = 'gardenlinux'
  AND dc.debsec_vulnerable = true
  AND dc.deb_source <> 'linux'
  AND dpc.cpe_version = iv.image_version;
