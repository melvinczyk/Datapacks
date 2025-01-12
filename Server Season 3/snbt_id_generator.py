import re
import uuid
import shutil
import os

def generate_quest_id():
    """Generate a quest-compatible ID in uppercase hex format."""
    return str(uuid.uuid4()).replace('-', '').upper()[:16]

def modify_weapon_quest(file_path, weapon_name, weapon_id, attribute_name, base_damage):
    """
    Modify an existing SNBT quest file to update weapon-specific information and manage IDs.
    """
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Generate new chapter ID
        chapter_pattern = r'id: "([A-F0-9]+)"'
        chapter_match = re.search(chapter_pattern, content)
        if chapter_match:
            original_chapter_id = chapter_match.group(1)
            new_chapter_id = generate_quest_id()
            content = content.replace(f'id: "{original_chapter_id}"', f'id: "{new_chapter_id}"', 1)

        # Find and store all quest IDs in order
        quest_matches = list(re.finditer(r'(?<=id: ")[A-F0-9]+(?=")', content))
        id_mapping = {}
        
        # Generate new IDs and create mapping
        for match in quest_matches:
            old_id = match.group(0)
            new_id = generate_quest_id()
            id_mapping[old_id] = new_id

        # Replace all quest IDs with their new values
        for old_id, new_id in id_mapping.items():
            content = content.replace(f'id: "{old_id}"', f'id: "{new_id}"')

        # Update existing dependencies using the ID mapping
        dependency_pattern = r'dependencies: \["([A-F0-9]+)"\]'
        for match in re.finditer(dependency_pattern, content):
            old_dep_id = match.group(1)
            if old_dep_id in id_mapping:
                new_dep_id = id_mapping[old_dep_id]
                content = content.replace(
                    f'dependencies: ["{old_dep_id}"]',
                    f'dependencies: ["{new_dep_id}"]'
                )

        # Replace weapon-specific content
        content = content.replace('AR-15', weapon_name)
        content = content.replace('ar15', weapon_name.lower().replace(' ', ''))
        content = content.replace('AR15', weapon_name.replace(' ', ''))
        content = content.replace('aurorasarsenal:ar_15', weapon_id)
        content = content.replace('hoths_jeg_attributes:ar_15_damage', f'hoths_jeg_attributes:{attribute_name}')

        # Handle damage progression
        PROGRESSION_STEPS = {
            6.75: 1, 7.0: 2, 7.25: 3, 7.5: 4,
            7.75: 5, 8.0: 6, 8.25: 7, 8.5: 8,
            9.5: None
        }

        def replace_damage(match):
            old_value = float(match.group(1))
            if old_value == 9.5:
                new_value = base_damage + 3.0
            else:
                step = PROGRESSION_STEPS.get(old_value, 1)
                new_value = base_damage + (0.25 * step)
            return f'command: "/attribute @s hoths_jeg_attributes:{attribute_name} base set {new_value:.2f}"'

        command_pattern = r'command: "/attribute @s hoths_jeg_attributes:[^"]+base set (\d+\.?\d*)"'
        content = re.sub(command_pattern, replace_damage, content)

        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        return f"Successfully modified {file_path}"

    except Exception as e:
        return f"Error processing file: {str(e)}"

def create_weapon_quest(base_path: str, filename: str, weapon_name: str, weapon_id: str, attribute_name: str, base_damage: float):
    """
    Creates a new weapon quest file from the AR-15 template and modifies it.
    """
    source_file = os.path.join(base_path, "ar15.snbt")
    target_file = os.path.join(base_path, f"{filename}.snbt")
    
    # Make sure we have a clean target file
    if os.path.exists(target_file):
        os.remove(target_file)
    
    # Copy the template file
    shutil.copy2(source_file, target_file)
    
    # Modify the copied file
    return modify_weapon_quest(target_file, weapon_name, weapon_id, attribute_name, base_damage)

# Example usage:
if __name__ == "__main__":
    base_path = "/Users/nicholasburczyk/Documents/curseforge/minecraft/Instances/Server V3 (Guns)/config/ftbquests/quests/chapters"
    result = create_weapon_quest(
        base_path=base_path,
        filename="akm",
        weapon_name="AKM",
        weapon_id="mteg:akm",
        attribute_name="akm_damage",
        base_damage=9.5
    )
    print(result)