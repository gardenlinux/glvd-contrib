import re

def extract_minor(version):
    # Remove epoch if present (e.g., '1:' in '1:1.37.0-5')
    version = version.split(':', 1)[-1]
    # Extract the numeric part before any dash or plus
    main_part = re.split(r'[-+]', version)[0]
    # Split by dot and take first two numeric components
    parts = main_part.split('.')
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}"
    elif len(parts) == 1:
        return parts[0]
    else:
        return None

with open("version-numbers.txt") as f:
    versions = [line.strip() for line in f if line.strip()]

for v in versions:
    print(f"{v} -> {extract_minor(v)}")

# To compare a candidate version:
def has_same_minor(candidate, version_set):
    candidate_minor = extract_minor(candidate)
    return candidate_minor in {extract_minor(v) for v in version_set}

# Example:
candidate = "2.12.1-1"
print(has_same_minor(candidate, versions))  # True, matches '2.12-7' and '2.12.7+dfsg+really2.9.14-1gl0'
