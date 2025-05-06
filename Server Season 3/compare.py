import os

def get_filenames(directory):
    """Returns a set of filenames in the given directory."""
    try:
        return set(os.listdir(directory))
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
        return set()

def compare_directories(dir1, dir2):
    """Compares files in two directories and prints differences."""
    files1 = get_filenames(dir1)
    files2 = get_filenames(dir2)
    
    only_in_dir1 = files1 - files2
    only_in_dir2 = files2 - files1
    
    if not only_in_dir1 and not only_in_dir2:
        print("Both directories have the same filenames.")
    else:
        if only_in_dir1:
            print("Files only in", dir1, ":", only_in_dir1)
        if only_in_dir2:
            print("Files only in", dir2, ":", only_in_dir2)

if __name__ == "__main__":
    dir1 = "/Users/nicholasburczyk/Documents/curseforge/minecraft/Instances/Server V3 (Guns)/mods"
    dir2 = "/Users/nicholasburczyk/Documents/curseforge/minecraft/Instances/Server V3 (Guns) (1)/mods"
    compare_directories(dir1, dir2)
