import os
import json

# Set the base directory where the "trophies/data/" folder is located
BASE_DIR = "trophies/data"
OUTPUT_FILE = "trophy_entities.txt"

entity_ids = []

# Walk through the directory tree
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".json") and "/trophies/" in os.path.join(root, file).replace("\\", "/"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    entity_id = data.get("entity")
                    if entity_id:
                        entity_ids.append(entity_id)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Skipping {file_path}: {e}")

# Write all found entity IDs to the output file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
    for entity in sorted(set(entity_ids)):
        f_out.write(entity + "\n")

print(f"Extracted {len(entity_ids)} entity IDs to {OUTPUT_FILE}")
