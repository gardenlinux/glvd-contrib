import argparse
import requests


def fetch_patch_release_notes(hostname, version):
    url = f"{hostname}/v1/patchReleaseNotes/{version}"
    response = requests.get(url)
    response.raise_for_status()  # Will raise an error for bad responses
    return response.json()


def generate_formatted_output(data):
    output = [
        "The following packages have been upgraded, to address the mentioned CVEs:"
    ]
    for package in data["packageList"]:
        upgrade_line = (
            f"- upgrade '{package['sourcePackageName']}' from `{package['oldVersion']}` "
            f"to `{package['newVersion']}`"
        )
        output.append(upgrade_line)

        if package["fixedCves"]:
            for c in package["fixedCves"]:
                output.append(f"  - {c}")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Print information about fixed CVEs in Garden Linux patch releases."
    )
    parser.add_argument(
        "--hostname",
        type=str,
        required=False,
        default="https://security.gardenlinux.org",
        help="The hostname of the API endpoint.",
    )
    parser.add_argument(
        "--version",
        type=str,
        required=True,
        help="The version number for the patch release notes.",
    )

    args = parser.parse_args()

    data = fetch_patch_release_notes(args.hostname, args.version)
    formatted_output = generate_formatted_output(data)
    print(formatted_output)


if __name__ == "__main__":
    main()
