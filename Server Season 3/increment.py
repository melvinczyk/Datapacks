import os
import re

def extract_base_set_values(content):
    """Extracts all base set values from the quest content for different weapons."""
    # General pattern for any weapon's base set value in the command field (e.g., hoths_jeg_attributes:xyz_damage)
    pattern = r'command:\s*"/attribute @s hoths_jeg_attributes:(\w+)_damage base set (\d+\.\d+)"'
    
    matches = re.findall(pattern, content)
    base_set_values = {}
    
    # Create a dictionary where the key is the weapon name (e.g., akm_custom, xyz), and the value is the base set value
    for weapon, value in matches:
        base_set_values[weapon] = float(value)  # Store the base set value as a float

    return base_set_values

def modify_quest_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if the group matches the required one
    if 'group: "2E8BF1A1F4DB9EE3"' not in content:
        print(f"Skipping {file_path}: Group ID does not match.")
        return

    # Extract all base set values for different weapons
    base_set_values = extract_base_set_values(content)
    if not base_set_values:
        print(f"Skipping {file_path}: No base set values found.")
        return

    print(f"Found base set values: {base_set_values} in {file_path}")

    increment_value = 0.5  # The increment for each quest

    # Find all reward "command" lines where base set is mentioned
    reward_pattern = r'command:\s*"/attribute @s hoths_jeg_attributes:(\w+)_damage base set (\d+\.\d+)"'
    matches = re.findall(reward_pattern, content)

    # Modify each quest's base set value by incrementing
    for index, (weapon, match_value) in enumerate(matches):
        if weapon in base_set_values:
            # Calculate the new base set value for each quest
            starting_value = base_set_values[weapon]
            new_base_value = starting_value + (index * increment_value)
            updated_value = f"{new_base_value:.2f}"  # Ensure 2 decimal places
            
            # Update the command with the new base set value
            content = re.sub(
                r'command:\s*"/attribute @s hoths_jeg_attributes:' + re.escape(weapon) + r'_damage base set ' + re.escape(match_value) + '"',
                f'command: "/attribute @s hoths_jeg_attributes:{weapon}_damage base set {updated_value}"',
                content
            )
            print(f"Updated base set value to {updated_value} for weapon {weapon}, quest {index + 1}")

    # Save the modified file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Updated base set values in {file_path}")

def process_folder(folder_path):
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        return
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):  # Process only files
            modify_quest_file(file_path)

if __name__ == "__main__":
    process_folder("/Users/nicholasburczyk/Documents/curseforge/minecraft/Instances/Server V3 (Guns)/config/ftbquests/quests/chapters")
