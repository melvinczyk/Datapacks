import shutil

def modify_weapon_quest(file_path, weapon_name, weapon_id, attribute_name, base_damage):
    """
    Modify an existing SNBT quest file to update weapon-specific information.
    
    Args:
        file_path (str): Path to the existing SNBT file to modify
        weapon_name (str): Name of the weapon to replace "AR-15" with
        weapon_id (str): Full weapon ID to replace "aurorasarsenal:ar_15" with
        attribute_name (str): Custom attribute name for the command (replaces ar_15_damage)
        base_damage (float): Base damage value to calculate progression from
    """
    try:
        # Read the file
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Replace weapon name (AR-15)
        content = content.replace('AR-15', weapon_name)
        content = content.replace('ar15', weapon_name.lower().replace(' ', '_'))
        
        # Replace weapon ID (aurorasarsenal:ar_15)
        content = content.replace('aurorasarsenal:ar_15', weapon_id)
        
        # Replace attribute name in commands
        content = content.replace('hoths_jeg_attributes:ar_15_damage', f'hoths_jeg_attributes:{attribute_name}')
        
        # Replace damage values in commands using regex to ensure we catch all instances
        import re
        
        # Define the pattern for command damage values
        command_pattern = r'command: "/attribute @s hoths_jeg_attributes:[^"]+base set (\d+\.?\d*)"'
        
        def replace_damage(match):
            old_value = float(match.group(1))
            
            # Determine which step in the progression we're at
            if old_value == 9.5:  # Final mastery value
                new_value = base_damage + 3.0
            else:
                # Map old values to progression steps
                progression_map = {
                    6.75: 1, 7.0: 2, 7.25: 3, 7.5: 4,
                    7.75: 5, 8.0: 6, 8.25: 7, 8.5: 8
                }
                step = progression_map.get(old_value, 1)
                new_value = base_damage + (0.25 * step)
            
            return f'command: "/attribute @s hoths_jeg_attributes:{attribute_name} base set {new_value:.2f}"'
        
        # Apply the replacements
        content = re.sub(command_pattern, replace_damage, content)
        
        # Write the modified content back to the same file
        with open(file_path, 'w') as file:
            file.write(content)
            
        return f"Successfully modified {file_path}"
        
    except FileNotFoundError:
        return f"Error: Could not find file at {file_path}"
    except Exception as e:
        return f"Error processing file: {str(e)}"

    
if __name__ == "__main__":
    filename = "vss_vintorez"
    
    shutil.copy("/Users/nicholasburczyk/Documents/curseforge/minecraft/Instances/Server V3 (Guns)/config/ftbquests/quests/chapters/ar15.snbt",f"/Users/nicholasburczyk/Documents/curseforge/minecraft/Instances/Server V3 (Guns)/config/ftbquests/quests/chapters/{filename}.snbt")

    result = modify_weapon_quest(
        f"/Users/nicholasburczyk/Documents/curseforge/minecraft/Instances/Server V3 (Guns)/config/ftbquests/quests/chapters/{filename}.snbt",  # Path to existing file to modify
        "Vss Vintorez",                               # New weapon name
        f"mteg:{filename}",                # New weapon ID
        f"{filename}_damage",                        # Custom attribute name
        10
    )
    print(result)
