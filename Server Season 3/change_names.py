import os
import json

folder_path = "loot/data/lootintegrations/loot"

for filename in os.listdir(folder_path):
    if filename.endswith("_trophy.json"):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'r') as f:
            data = json.load(f)

        # Set max_result_itemcount to 1
        data["max_result_itemcount"] = 1

        # Set all integrated_loot_tables values to 1
        if "integrated_loot_tables" in data:
            data["integrated_loot_tables"] = {key: 1 for key in data["integrated_loot_tables"]}

        # Save the modified file
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

print("All _trophy.json files updated with new values.")
