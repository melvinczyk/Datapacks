import json

# Path to your JSON file
file_path = "/Users/nicholasburczyk/Desktop/Minecraft server stuff/Datapacks/Server Season 3/custom_entity_attributes/basic.json5"

# Load the JSON data
with open(file_path, "r") as file:
    data = json.load(file)

# Define the movement speed attribute
movement_speed_attribute = {
    "attribute": "minecraft:generic.movement_speed",
    "value": 0.15,
    "operation": "MULTIPLY_BASE"
}

# Iterate through all entities
for entity in data.get("modifiers", []):
    attributes = entity.get("attributes", [])

    # Check if the movement speed attribute already exists
    has_movement_speed = any(attr["attribute"] == "minecraft:generic.movement_speed" for attr in attributes)

    # If it doesn't exist, add it
    if not has_movement_speed:
        attributes.append(movement_speed_attribute)

# Save the modified JSON back to the file
with open(file_path, "w") as file:
    json.dump(data, file, indent=2)

print("✅ Movement speed attribute added where necessary.")
