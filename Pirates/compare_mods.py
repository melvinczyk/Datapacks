from pathlib import Path
import hashlib
import re
from collections import defaultdict

# --- CONFIG ---
FOLDER_A = Path(r"/Users/nicholasburczyk/Desktop/Minecraft server stuff/Datapacks/Pirates/mods")
FOLDER_B = Path(r"/Users/nicholasburczyk/Documents/curseforge/minecraft/Instances/Pirates/mods")

# Compare only these extensions
EXTS = (".jar", ".jar.disabled", ".input")

# --- HELPERS ---
def sha256(path: Path, chunk_size=1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()

# Trailing version-ish segment (ex: -1.2.3, -v6.3.1, +mc1.20.1, -build.16, etc.)
_versionish = re.compile(r"""
    (?:[-_. ]?)                  # optional separator
    (?:v)?                       # optional leading v
    (?:\d+\.)*\d+                # digits like 1.2.3 or 20.1
    (?:[-+._][0-9a-z]+)*         # extra bits like +mc1.20.1, -forge, -build.16
    $                            # must be at the end
""", flags=re.IGNORECASE | re.VERBOSE)

# Minecraft version tags (mc1.20.1, minecraft-1.20.1, etc.)
_mc_tag = re.compile(r"(?:\+?mc\d+\.\d+(?:\.\d+)?)|(?:minecraft[-_ ]?\d+\.\d+(?:\.\d+)?)",
                     flags=re.IGNORECASE)

def mod_key(filename: str) -> str:
    """
    Convert a jar filename to a normalized 'mod identity' key, ignoring version suffixes.
    """
    name = filename.strip()

    # strip extensions in a consistent order
    for ext in (".jar.disabled", ".jar", ".input"):
        if name.lower().endswith(ext):
            name = name[: -len(ext)]
            break

    name = name.strip()

    # remove minecraft version tags
    name = _mc_tag.sub("", name).strip()

    # remove trailing version-ish component
    name = _versionish.sub("", name).strip()

    # normalize separators/case
    name = re.sub(r"[\s._]+", "-", name)
    name = re.sub(r"-{2,}", "-", name)
    return name.lower().strip("-")

def list_files(root: Path) -> dict[str, list[Path]]:
    """
    Map: mod_key -> list of matching file paths under root (recursive).
    """
    out = defaultdict(list)
    if not root.exists():
        raise SystemExit(f"Folder does not exist: {root}")
    for p in root.rglob("*"):
        if p.is_file() and p.name.lower().endswith(EXTS):
            out[mod_key(p.name)].append(p)
    return out

# --- MAIN ---
mods_a = list_files(FOLDER_A)
mods_b = list_files(FOLDER_B)

keys_a = set(mods_a.keys())
keys_b = set(mods_b.keys())

only_a = sorted(keys_a - keys_b)
only_b = sorted(keys_b - keys_a)
both = sorted(keys_a & keys_b)

print(f"Folder A mod-keys: {len(keys_a)}")
print(f"Folder B mod-keys: {len(keys_b)}")

print("\n=== Present only in A (by mod identity) ===")
for k in only_a:
    for p in sorted(mods_a[k]):
        print(f"  {k:40} -> {p.relative_to(FOLDER_A)}")

print("\n=== Present only in B (by mod identity) ===")
for k in only_b:
    for p in sorted(mods_b[k]):
        print(f"  {k:40} -> {p.relative_to(FOLDER_B)}")

print("\n=== Present in BOTH but different contents (hash mismatch) ===")
diffs = 0
for k in both:
    # Compare all candidates on each side; if any exact hash match exists, treat as matched.
    a_paths = mods_a[k]
    b_paths = mods_b[k]

    a_hashes = {sha256(p): p for p in a_paths}
    b_hashes = {sha256(p): p for p in b_paths}

    # if no shared hash, they differ
    if set(a_hashes.keys()).isdisjoint(set(b_hashes.keys())):
        diffs += 1
        # pick representative files to print (shortest name heuristic)
        a_rep = min(a_paths, key=lambda p: len(p.name))
        b_rep = min(b_paths, key=lambda p: len(p.name))
        print(f"  {k}")
        print(f"    A: {a_rep.name}")
        print(f"    B: {b_rep.name}")

if diffs == 0:
    print("  (none)")
