import os
import zipfile
import re
from packaging import version

MODS_DIR = "/Users/nicholasburczyk/Desktop/mods"
CURRENT_FORGE_VERSION = version.parse("47.2.23")

def parse_version_range(range_str):
    # Supports formats like [47.1.0,), (47.2.0,47.4.0], etc.
    match = re.match(r"([\[\(])([\d\.]+)?,?([\d\.]+)?([\]\)])", range_str)
    if not match:
        return None
    lower_inclusive = match.group(1) == "["
    upper_inclusive = match.group(4) == "]"
    lower = version.parse(match.group(2)) if match.group(2) else None
    upper = version.parse(match.group(3)) if match.group(3) else None
    return lower, lower_inclusive, upper, upper_inclusive

def is_version_compatible(range_str, current_version):
    parsed = parse_version_range(range_str)
    if not parsed:
        return True  # Assume compatible if range not readable
    lower, lower_incl, upper, upper_incl = parsed
    if lower:
        if lower_incl and current_version < lower:
            return False
        if not lower_incl and current_version <= lower:
            return False
    if upper:
        if upper_incl and current_version > upper:
            return False
        if not upper_incl and current_version >= upper:
            return False
    return True

def extract_forge_version_range(jar_path):
    try:
        with zipfile.ZipFile(jar_path, 'r') as jar:
            if "META-INF/mods.toml" in jar.namelist():
                with jar.open("META-INF/mods.toml") as file:
                    content = file.read().decode("utf-8")
                    match = re.search(r'modId\s*=\s*"forge".*?versionRange\s*=\s*"([^"]+)"', content, re.DOTALL)
                    if match:
                        return match.group(1)
    except Exception as e:
        return f"Error: {e}"
    return None

def check_mods_compatibility(mods_dir):
    incompatible = {}
    for filename in os.listdir(mods_dir):
        if filename.endswith(".jar"):
            jar_path = os.path.join(mods_dir, filename)
            range_str = extract_forge_version_range(jar_path)
            if range_str and not is_version_compatible(range_str, CURRENT_FORGE_VERSION):
                incompatible[filename] = range_str
    return incompatible

# Run it
incompatibles = check_mods_compatibility(MODS_DIR)
for mod, required in incompatibles.items():
    print(f"❌ {mod}: Incompatible with Forge 47.3.22 (requires {required})")

if not incompatibles:
    print("✅ All mods are compatible with Forge 47.3.22")
