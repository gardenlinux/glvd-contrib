#!/usr/bin/env bash

# Set CVE_ID (e.g., passed as an argument or defined explicitly)
CVE_ID=$1

# Query NVD API for the CVE_ID
nvd_result=$(curl -s "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=${CVE_ID}")

# Query local vulnerabilities list (assumes it's stored in a file `vulnerabilities.json`)
jq_result=$(echo "$nvd_result" | jq --arg CVE_ID "$CVE_ID" '.vulnerabilities[] | select(.cve.id == $CVE_ID)')

# Extract all references, gracefully handling missing "tags"
references_with_tags=$(echo "$jq_result" | jq -r '.cve.references[] | "\(.url), \((.tags // ["None"]) | join(", "))"')

# Output results
#echo "=== NVD API Result ==="
#echo "$nvd_result" | jq

echo "=== References with Tags (or None) ==="
echo "$references_with_tags"
