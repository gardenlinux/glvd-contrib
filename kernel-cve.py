import json
import logging
import os
import glob
import psycopg2
import argparse

# proof of concept, not a productive implementation

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

# List of irrelevant kernel submodules
irrelevant_submodules = [
    "afs", "xen", "x86/hyperv", "wifi", "video/", "staging", "drm", "can", "Bluetooth", "mmc", "nfc", "thunderbolt",
    "s390", "riscv", "powerpc", "nouveau", "media", "leds", "usb", "MIPS", "nilfs2", "ubifs", "ocfs2", "spi", "i3c",
    "um", "udf", "atm", "eventfs", "fs/9p", "gtp", "hid", "i2c", "ice", "hwmon", "mailbox", "misc", "f2fs", "libfs",
    "dma-buf", "binder", "alsa", "dev/parport", "closures", "devres", "fs/ntfs3", "hfs", "hfsplus", "ibmvnic", "iio",
    "jfs", "misdn", "padata", "pds_core", "parisc", "loongarch"
]

def compare_versions(v1, v2):
    v1_parts = list(map(int, v1.split('.')))
    v2_parts = list(map(int, v2.split('.')))
    
    # Compare each part of the version
    for v1_part, v2_part in zip(v1_parts, v2_parts):
        if v1_part < v2_part:
            return -1
        elif v1_part > v2_part:
            return 1
    
    # If all parts are equal, compare the length of the version parts
    if len(v1_parts) < len(v2_parts):
        return -1
    elif len(v1_parts) > len(v2_parts):
        return 1
    return 0

def is_relevant_module(program_files):
    for file in program_files:
        for submodule in irrelevant_submodules:
            if submodule in file:
                return False
    return True

def get_fixed_versions(lts_versions, cve_data):
    fixed_versions = {lts: None for lts in lts_versions}
    
    for entry in cve_data['containers']['cna']['affected']:
        if 'versions' not in entry:
            logging.debug(f"No 'versions' key in entry: {entry}")
            continue
        
        for ver in entry['versions']:
            if ver['status'] == 'unaffected':
                for lts in lts_versions:
                    if ver['version'].startswith(lts):
                        if fixed_versions[lts] is None or compare_versions(ver['version'], fixed_versions[lts]) < 0:
                            version: str = ver['version']
                            logging.debug(f"Updating fixed version for {lts}: {fixed_versions[lts]} -> {version}")
                            fixed_versions[lts] = version
                        else:
                            logging.debug(f"Skipping version {ver['version']} for {lts} as it is not earlier than {fixed_versions[lts]}")
            else:
                logging.debug(f"Version {ver['version']} is affected, skipping")
    return fixed_versions

# Database connection parameters
conn_params = {
    'dbname': 'glvd',
    'user': 'glvd',
    'password': 'glvd',
    'host': 'localhost',
    'port': '5432'
}

# Connect to the PostgreSQL database
conn = psycopg2.connect(**conn_params)
cur = conn.cursor()

# Directory containing the JSON files
# Parse command line arguments
parser = argparse.ArgumentParser(description='Process CVE JSON files.')
parser.add_argument('directory', type=str, help='Directory containing the JSON files')
args = parser.parse_args()

directory = args.directory

# LTS kernel versions to check
lts_versions = ["6.6", "6.12"]

# Iterate over all JSON files in the directory
for filepath in glob.glob(os.path.join(directory, '**/*.json'), recursive=True):
    logging.debug(f"Processing file: {filepath}")
    
    contents = ''
    # Load JSON data from file
    with open(filepath, 'r') as file:
        cve_data = json.load(file)
        contents = json.dumps(cve_data)
    
    # Determine if the CVE affects a relevant module
    program_files = []
    for entry in cve_data['containers']['cna']['affected']:
        program_files.extend(entry.get('programFiles', []))
    relevant_module = is_relevant_module(program_files)
    
    # Get fixed versions for the specified LTS kernels
    fixed_versions = get_fixed_versions(lts_versions, cve_data)
    
    # Insert the results into the database
    cve_id = os.path.basename(filepath).replace('.json', '')
    for lts, version in fixed_versions.items():
        is_fixed = version is not None
        cur.execute(
            """
            INSERT INTO public.cve_context_kernel (cve_id, lts_version, fixed_version, is_fixed, is_relevant_module, source_data)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (cve_id, lts_version) DO UPDATE
            SET fixed_version = EXCLUDED.fixed_version,
                is_fixed = EXCLUDED.is_fixed,
                is_relevant_module = EXCLUDED.is_relevant_module,
                source_data = EXCLUDED.source_data
            """,
            (cve_id, lts, version, is_fixed, relevant_module, contents)
        )
    conn.commit()

# Close the database connection
cur.close()
conn.close()
