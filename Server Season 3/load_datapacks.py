import os
import zipfile
import shutil

def zip_and_copy_datapacks(server_season_folder, datapacks_folder):
    """
    Zips the 'data' folder and 'pack.mcmeta' file in each subfolder of the server season folder
    and copies the resulting zip files to the datapacks folder.

    Args:
        server_season_folder (str): Path to the "Server Season 3" directory.
        datapacks_folder (str): Path to the "datapacks" directory where zip files will be copied.
    """
    os.makedirs(datapacks_folder, exist_ok=True)
    print(f"Ensured that datapacks folder exists at: {datapacks_folder}\n")

    for folder in os.listdir(server_season_folder):
        folder_path = os.path.join(server_season_folder, folder)

        if os.path.isdir(folder_path):
            data_folder = os.path.join(folder_path, "data")
            pack_mcmeta_file = os.path.join(folder_path, "pack.mcmeta")

            if os.path.exists(data_folder) and os.path.exists(pack_mcmeta_file):
                zip_file_name = f"{folder}.zip"
                zip_file_path = os.path.join(folder_path, zip_file_name)

                try:
                    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                        for root, _, files in os.walk(data_folder):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, start=folder_path)
                                zipf.write(file_path, arcname)

                        # Add the "pack.mcmeta" file
                        zipf.write(pack_mcmeta_file, os.path.relpath(pack_mcmeta_file, start=folder_path))

                    print(f"Created zip file: {zip_file_path}")

                    destination_path = os.path.join(datapacks_folder, zip_file_name)
                    shutil.copy(zip_file_path, destination_path)
                    print(f"Copied {zip_file_name} to {datapacks_folder}\n")

                except Exception as e:
                    print(f"Failed to process {folder_path}: {e}\n")
            else:
                print(f"Skipping {folder_path}: 'data' folder or 'pack.mcmeta' file is missing.\n")

    print("All eligible folders have been processed.")

if __name__ == "__main__":
    server_season_folder_path = r"/Users/nicholasburczyk/Desktop/Minecraft server stuff/Datapacks/Server Season 3"
    datapacks_folder_path = r"/Users/nicholasburczyk/Documents/curseforge/minecraft/Instances/Server V3 (Guns)/saves/New World/datapacks"

    zip_and_copy_datapacks(server_season_folder_path, datapacks_folder_path)
