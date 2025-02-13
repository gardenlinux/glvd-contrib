CREATE TABLE public.cve_context_kernel (
    id SERIAL PRIMARY KEY,
    cve_id TEXT NOT NULL,
    lts_version TEXT NOT NULL,
    fixed_version TEXT,
    is_fixed BOOLEAN NOT NULL,
    is_relevant_module BOOLEAN NOT NULL,
    source_file TEXT NOT NULL,
    UNIQUE (cve_id, lts_version)
);
