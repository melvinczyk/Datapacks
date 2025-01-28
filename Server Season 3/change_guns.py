import json

# Input JSON file path
input_file = "/Users/nicholasburczyk/Desktop/Minecraft server stuff/Datapacks/Server Season 3/factions.json"
# Output formatted file path
output_file = "/Users/nicholasburczyk/Desktop/Minecraft server stuff/Datapacks/Server Season 3/factions_formatted.txt"

# Load the JSON data from the file
with open(input_file, "r") as file:
    data = json.load(file)

# Ensure data is a list
if not isinstance(data, list):
    raise ValueError("Expected a list in the JSON file.")

# Process and write to the new file
with open(output_file, "w") as file:
    for line in data:
        # Remove any accidental newline characters inside the string
        formatted_line = line.replace("\n", "")
        file.write(formatted_line + "\n")

print("✅ Formatted data has been saved to:", output_file)
