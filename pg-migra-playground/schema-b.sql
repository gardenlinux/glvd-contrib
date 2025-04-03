--
-- Name: all_cve; Type: TABLE; Schema: public; Owner: glvd
--

CREATE TABLE public.all_cve (
    cve_id text NOT NULL,
    last_mod timestamp with time zone DEFAULT now() NOT NULL,
    data json NOT NULL
);


ALTER TABLE public.all_cve OWNER TO glvd;

--
-- Name: cve_context; Type: TABLE; Schema: public; Owner: glvd
--

CREATE TABLE public.cve_context (
    dist_id integer,
    gardenlinux_version text,
    cve_id text NOT NULL,
    create_date timestamp with time zone DEFAULT now() NOT NULL,
    context_descriptor text NOT NULL,
    score_override numeric,
    description text NOT NULL,
    is_resolved boolean DEFAULT true
);


ALTER TABLE public.cve_context OWNER TO glvd;

--
-- Name: cve_context_kernel; Type: TABLE; Schema: public; Owner: glvd
--

CREATE TABLE public.cve_context_kernel (
    cve_id text NOT NULL,
    lts_version text NOT NULL,
    fixed_version text,
    is_fixed boolean NOT NULL,
    is_relevant_module boolean NOT NULL,
    source_data jsonb NOT NULL
);


ALTER TABLE public.cve_context_kernel OWNER TO glvd;

--
-- Name: deb_cve; Type: TABLE; Schema: public; Owner: glvd
--

CREATE TABLE public.deb_cve (
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


ALTER TABLE public.deb_cve OWNER TO glvd;

--
-- Name: debsec_cve; Type: TABLE; Schema: public; Owner: glvd
--

CREATE TABLE public.debsec_cve (
    dist_id integer,
    gardenlinux_version text,
    cve_id text NOT NULL,
    last_mod timestamp with time zone DEFAULT now() NOT NULL,
    deb_source text NOT NULL,
    deb_version_fixed public.debversion,
    debsec_tag text,
    debsec_note text
);


ALTER TABLE public.debsec_cve OWNER TO glvd;

--
-- Name: debsrc; Type: TABLE; Schema: public; Owner: glvd
--

CREATE TABLE public.debsrc (
    dist_id integer,
    gardenlinux_version text,
    last_mod timestamp with time zone DEFAULT now() NOT NULL,
    deb_source text NOT NULL,
    deb_version public.debversion NOT NULL
);


ALTER TABLE public.debsrc OWNER TO glvd;

--
-- Name: dist_cpe; Type: TABLE; Schema: public; Owner: glvd
--

CREATE TABLE public.dist_cpe (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    cpe_vendor text NOT NULL,
    cpe_product text NOT NULL,
    cpe_version text NOT NULL,
    deb_codename text NOT NULL
);


ALTER TABLE public.dist_cpe OWNER TO glvd;

CREATE OR REPLACE VIEW public.cve_with_context
 AS
 SELECT cve_context.dist_id,
    cve_context.cve_id
   FROM cve_context
  GROUP BY cve_context.dist_id, cve_context.cve_id;

ALTER TABLE public.cve_with_context
    OWNER TO glvd;
