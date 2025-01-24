import shutil
import os

def copy_file(src_folder, dest_folder, filename):
    """
    Copies a file from src_folder to dest_folder while keeping the same filename.

    :param src_folder: Path to the source folder
    :param dest_folder: Path to the destination folder
    :param filename: Name of the file to copy (including extension)
    """
    src_path = os.path.join(src_folder, filename)
    dest_path = os.path.join(dest_folder, filename)

    # Check if the source file exists
    if not os.path.exists(src_path):
        print(f"Error: {filename} does not exist in {src_folder}.")
        return False

    try:
        shutil.copy2(src_path, dest_path)  # copy2 preserves metadata
        print(f"Copied {filename} to {dest_folder}")
        return True
    except Exception as e:
        print(f"Error copying {filename}: {e}")
        return False

src_folder = "/Users/nicholasburczyk/Desktop/Minecraft server stuff/Datapacks/Server Season 3/JEG/jeg-common.toml"
dest_folder = "/Users/nicholasburczyk/Documents/curseforge/minecraft/instances/Server V3 (Guns)/config"
filename = "jeg-common.toml"

copy_file(src_folder, dest_folder, filename)
