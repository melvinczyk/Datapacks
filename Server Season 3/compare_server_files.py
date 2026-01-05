import os

def compare_directories(dir1, dir2):
    # Get sets of filenames from both directories
    files1 = set(os.listdir(dir1))
    files2 = set(os.listdir(dir2))

    # Compute differences
    only_in_dir1 = files1 - files2
    only_in_dir2 = files2 - files1
    in_both = files1 & files2

    print(f"\nFiles only in {dir1}:")
    if only_in_dir1:
        for f in sorted(only_in_dir1):
            print("  -", f)
    else:
        print("  (none)")

    print(f"\nFiles only in {dir2}:")
    if only_in_dir2:
        for f in sorted(only_in_dir2):
            print("  -", f)
    else:
        print("  (none)")

    print("\nFiles present in both:")
    if in_both:
        for f in sorted(in_both):
            print("  -", f)
    else:
        print("  (none)")


# Example usage:
compare_directories("/Users/nicholasburczyk/Desktop/Minecraft server stuff/mods/server_mods/mods", "/Users/nicholasburczyk/Documents/curseforge/minecraft/Instances/Server V3 (Guns) (1)/mods")
