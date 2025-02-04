import os
import json

# Set the directory containing the JSON files
FOLDER_PATH = "/Users/nicholasburczyk/Desktop/Minecraft server stuff/Datapacks/Server Season 3/Aurora's-Arsenal/data/aurorasarsenal/guns"  # Change this to the actual folder path
NEW_TRAIL_LENGTH_MULTIPLIER = 5.0  # Change this to your desired value

def update_json_files(folder_path, new_value):
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                
                # Update the trailLengthMultiplier
                if "projectile" in data:
                    if "trailLengthMultiplier" in data["projectile"]:
                        data["projectile"]["trailLengthMultiplier"] = new_value
                    
                    # Check and update projectile speed
                    if "speed" in data["projectile"] and data["projectile"]["speed"] > 12:
                        data["projectile"]["speed"] = 12
                        print(f"Speed reduced to 12 in: {filename}")
                    
                    # Write back the updated JSON
                    with open(file_path, "w", encoding="utf-8") as file:
                        json.dump(data, file, indent=2)
                    
                    print(f"Updated: {filename}")
                else:
                    print(f"Skipped (no projectile section found): {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    update_json_files(FOLDER_PATH, NEW_TRAIL_LENGTH_MULTIPLIER)