CREATE TABLE public.all_cve (
    cve_id text NOT NULL,
    last_mod timestamp with time zone DEFAULT now() NOT NULL,
    data json NOT NULL
);


CREATE TABLE public.distro (
    id integer NOT NULL,
    cpe_vendor text NOT NULL,
    cpe_product text NOT NULL,
    cpe_version text NOT NULL,
    deb_codename text
);


CREATE TABLE public.nvd_cve (
    cve_id text NOT NULL,
    last_mod timestamp with time zone NOT NULL,
    data json NOT NULL
);

CREATE TABLE public.debian_security_cve (
    dist_id integer NOT NULL,
    cve_id text NOT NULL,
    last_mod timestamp with time zone DEFAULT now() NOT NULL,
    deb_source text NOT NULL,
    deb_version_fixed public.debversion,
    debsec_tag text,
    debsec_note text
);

CREATE TABLE public.source_package (
    dist_id integer,
    gardenlinux_version text,
    last_mod timestamp with time zone DEFAULT now() NOT NULL,
    deb_source text NOT NULL,
    deb_version public.debversion NOT NULL
);


CREATE TABLE public.debian_cve (
    dist_id integer,
    gardenlinux_version text,
    cve_id text NOT NULL,
    last_mod timestamp with time zone DEFAULT now() NOT NULL,
    cvss_severity integer,
    deb_source text NOT NULL,
    deb_version public.debversion NOT NULL,
    deb_version_fixed public.debversion,
    debsec_vulnerable boolean NOT NULL,
    data_cpe_match json NOT NULL
);
