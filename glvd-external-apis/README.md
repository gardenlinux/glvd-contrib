# GLVD External Data Sources

## NIST API

Example data https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2021-22901

Json object with pretty complex structure and lot of fields

Important:
  - id
  - published
  - metrics.*.baseScore

Suggestion: use the [humao.rest-client vs code extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) to open nist-api.http and discover the contents

## Debian Security Tracker

From this file: https://salsa.debian.org/security-tracker-team/security-tracker/-/blob/master/data/CVE/list?ref_type=heads

Contains entries like

```
CVE-2024-6197 (libcurl's ASN1 parser has this utf8asn1str() function used for parsing ...)
        - curl 8.9.0-1 (bug #1076996)
        [bookworm] - curl <not-affected> (Vulnerable code introduced later)
        [bullseye] - curl <not-affected> (Vulnerable code introduced later)
        NOTE: https://curl.se/docs/CVE-2024-6197.html
        NOTE: Introduced in: https://github.com/curl/curl/commit/623c3a8fa0bdb2751f14b3741760d81910b7ec64 (curl-8_6_0)
        NOTE: Fixed by: https://github.com/curl/curl/commit/3a537a4db9e65e545ec45b1b5d5575ee09a2569d (curl-8_9_0)
CVE-2024-38550 (In the Linux kernel, the following vulnerability has been resolved:  A ...)
        - linux 6.8.12-1
        [bookworm] - linux 6.1.94-1
        [bullseye] - linux <not-affected> (Vulnerable code not present)
        [buster] - linux <not-affected> (Vulnerable code not present)
        NOTE: https://git.kernel.org/linus/ea60ab95723f5738e7737b56dda95e6feefa5b50 (6.10-rc1)
```

Code to ingest in glvd: https://github.com/gardenlinux/glvd/blob/7ca2ff54e01da5e9eae61d1cd565eaf75f3c62ce/src/glvd/cli/data/ingest_debsec.py#L1
