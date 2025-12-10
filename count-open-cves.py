import urllib.request
import json
import argparse


def get_cve_count(endpoint, version):
    url = f"{endpoint}/v1/cves/{version}?sortBy=cveId&sortOrder=ASC"
    req = urllib.request.Request(url, headers={"accept": "application/json"})
    with urllib.request.urlopen(req) as response:
        data = response.read()
        cves = json.loads(data)
        print(f"{version:<10} {len(cves):>7,}")


def main():
    parser = argparse.ArgumentParser(
        description="Count open CVEs for Gardenlinux versions."
    )
    parser.add_argument(
        "--endpoint",
        default="https://security.gardenlinux.org",
        help="API endpoint URL",
    )
    args = parser.parse_args()
    for version in ["today", "1877.8", "1592.15"]:
        get_cve_count(args.endpoint, version)


if __name__ == "__main__":
    main()
