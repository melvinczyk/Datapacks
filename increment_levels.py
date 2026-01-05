import os
import json

# Configuration
FOLDER_PATH = "/Users/nicholasburczyk/Desktop/Minecraft server stuff/Datapacks/Cobblemon Season/rct/data/rctmod/trainers" # <- Set your folder path here
LEVEL_INCREMENT = 5                  # <- Change this to the desired level increase
ALLOWED_PREFIXES = ["elite_four_"]

def should_process_file(filename):
    return any(filename.startswith(prefix) for prefix in ALLOWED_PREFIXES)

def update_levels_in_file(file_path, level_increment):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if "team" in data:
        for pokemon in data["team"]:
            if "level" in pokemon:
                pokemon["level"] += level_increment

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

def update_all_files_in_folder(folder_path, level_increment):
    for filename in os.listdir(folder_path):
        if not filename.endswith(".json"):
            continue

        file_path = os.path.join(folder_path, filename)
        try:
            update_levels_in_file(file_path, level_increment)
            print(f"Updated: {filename}")
        except Exception as e:
            print(f"Failed to update {filename}: {e}")

if __name__ == "__main__":
    update_all_files_in_folder(FOLDER_PATH, LEVEL_INCREMENT)
