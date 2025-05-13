import os
import json

BASE_FOLDER = '/Users/nicholasburczyk/Desktop/Minecraft server stuff/Datapacks/Server Season 3/trophies/data'
OLD_DROP_CHANCE = 0.01
NEW_DROP_CHANCE = 0.015

def update_existing_drop_chance(base_folder):
    for root, dirs, files in os.walk(base_folder):
        if 'trophies' in root.split(os.sep):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        try:
                            data = json.load(f)
                        except json.JSONDecodeError:
                            print(f"Skipping invalid JSON: {file_path}")
                            continue

                    if data.get("drop_chance") == OLD_DROP_CHANCE:
                        data["drop_chance"] = NEW_DROP_CHANCE
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2)
                        print(f"Updated drop_chance in: {file_path}")

if __name__ == "__main__":
    update_existing_drop_chance(BASE_FOLDER)
