import json
import os

def update_gunnite_count(json_data):
    for material in json_data.get("materials", []):
        if material.get("item") == "born_in_chaos_v1:dark_metal_ingot":
            material["count"] += 1
    return json_data

def process_json_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, "r") as file:
                json_data = json.load(file)
            
            updated_json = update_gunnite_count(json_data)
            
            with open(file_path, "w") as file:
                json.dump(updated_json, file, indent=2)

folder_path = "/Users/nicholasburczyk/Desktop/Minecraft server stuff/Datapacks/Server Season 3/M'TEG/data/mteg/recipes"
process_json_files(folder_path)
