import os
import json

# Set the directory containing the JSON files
folder_path = "/Users/nicholasburczyk/Desktop/Minecraft server stuff/Datapacks/Server Season 3/SCG/data/scguns/guns"

# Loop through all JSON files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):  # Ensure it's a JSON file
        file_path = os.path.join(folder_path, filename)
        
        # Open and load JSON file
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON file: {filename}")
                continue

        # Check and add "trailColor" if missing
        if "projectile" in data and "trailColor" not in data["projectile"]:
            data["projectile"]["trailColor"] = -256
            print(f"Updated {filename}: Added 'trailColor'.")

            # Write back to the file
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2)
        else:
            print(f"{filename} already has 'trailColor'.")

print("Processing complete.")
