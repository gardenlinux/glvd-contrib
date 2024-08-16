CREATE TYPE description AS (lang TEXT, value TEXT);

CREATE TYPE tag AS (sourceIdentifier TEXT, tags TEXT []);

CREATE TYPE reference AS ("url" TEXT, source TEXT);

CREATE TYPE cvssMetricV40 AS (
    source TEXT,
    "type" TEXT,
    vector text --fixme just for testing
);

CREATE TYPE cvssMetricV31 AS (
    source TEXT,
    "type" TEXT,
    vector text --fixme just for testing
);

CREATE TYPE cvssMetricV30 AS (
    source TEXT,
    "type" TEXT,
    vector text --fixme just for testing
);

CREATE TYPE cvssMetricV2 AS (
    source TEXT,
    "type" TEXT,
    vector text --fixme just for testing
);

CREATE TYPE metrics AS (
    v40 cvssMetricV40 [],
    v31 cvssMetricV31 [],
    v30 cvssMetricV30 [],
    v2 cvssMetricV2 []
);

CREATE TABLE cve_item (
    id text NOT NULL,
    sourceIdentifier TEXT,
    vulnStatus TEXT,
    published TEXT,
    lastModified TEXT,
    evaluatorComment TEXT,
    evaluatorSolution TEXT,
    cisaExploitAdd TEXT,
    cisaActionDue TEXT,
    cisaRequiredAction TEXT,
    cisaVulnerabilityName TEXT,
    -- this seems to be empty always.. have not found a counter sample yet
    cveTags tag [],
    descriptions description [],
    "references" reference [],
    metrics metrics,
    CONSTRAINT cve_item_pk PRIMARY KEY (id)
);
