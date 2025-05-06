import os
import re
import sys


def extract_weapon_name(content):
    """Extracts the weapon name from the quest description, stopping at 'by', 'using', or 'with'."""
    match = re.search(r'description:\s*\["Craft (?:an|a) (.*?)\s+(?:by|using|with)\b', content)
    if match:
        return match.group(1).strip()  # Extracted weapon name
    return "Unknown Weapon"

def extract_all_damage_values(text):
    # Regex pattern to match all the commands with weapon damage
    damage_pattern = r'command:\s*"/attribute @s hoths_jeg_attributes:(\w+)_damage base set (\d+\.\d+)"'
    
    # Find all matches of the pattern
    matches = re.findall(damage_pattern, text)

    # If matches are found, print the weapon names and their respective damage values
    if matches:
        for weapon_name, damage in matches:
            print(f"Weapon: {weapon_name}, Damage: {damage}")
    else:
        print("No matches found.")
        
def modify_damage_values(file_content):
    # Regex pattern to find weapon names and their corresponding damage values
    damage_pattern = r'command:\s*"/attribute @s hoths_jeg_attributes:(\w+)_damage base set (\d+\.\d+)"'
    
    # Find all matches of the pattern (weapon_name, damage_value)
    matches = re.findall(damage_pattern, file_content)

    # If matches are found, start modifying them
    if matches:
        # Create a list of all damage values as floats
        damage_values = [float(damage) for weapon_name, damage in matches]

        # Start with the first value and apply the changes incrementally
        new_damage_map = {}  # Dictionary to store old vs new values
        new_damage_values = []

        # Start by adding 0.25 to the first value
        new_damage_values.append(damage_values[0])

        # For each subsequent value, add 0.5 to the previous damage value
        for i in range(1, len(damage_values) - 1):  # Exclude the last value for now
            new_damage_values.append(new_damage_values[i - 1] + 0.5)

        # Add 3 to the last value
        new_damage_values.append(new_damage_values[-1] + 3)

        # Now create a dictionary with old values as keys and new values as values
        for i, (weapon_name, _) in enumerate(matches):
            old_damage_value = float(matches[i][1])
            new_damage_value = new_damage_values[i]
            new_damage_map[old_damage_value] = new_damage_value

        # Now, we need to swap the 5th and 6th key-value pairs (index 4 and 5)
        keys = list(new_damage_map.keys())
        if len(keys) >= 6:
            key_5, key_6 = keys[4], keys[5]
            new_damage_map[key_5], new_damage_map[key_6] = new_damage_map[key_6], new_damage_map[key_5]

        # Sort the dictionary by the old damage values in descending order
        sorted_new_damage_map = dict(sorted(new_damage_map.items(), reverse=True))

        # Now, replace all the old damage values with the new ones in one go
        for old_damage_value, new_damage_value in sorted_new_damage_map.items():
            # Find the weapon name for the current old value
            weapon_name = next(weapon for weapon, damage in matches if float(damage) == old_damage_value)
            
            # Create the updated command string with the new damage value
            new_command = f'command: "/attribute @s hoths_jeg_attributes:{weapon_name}_damage base set {new_damage_value:.2f}"'

            # Replace all occurrences of the old damage value in the file content
            file_content = re.sub(
                fr'command:\s*"/attribute @s hoths_jeg_attributes:\w+_damage base set {old_damage_value:.2f}"',
                new_command,
                file_content
            )
            print(f"old: {old_damage_value}, new: {new_damage_value}")

    return file_content
        

def modify_quest_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if the group matches the required one
    if 'group: "2E8BF1A1F4DB9EE3"' not in content:
        print(f"Skipping {file_path}: Group ID does not match.")
        return
    
    weapon_name = extract_weapon_name(content)
    print(f"Processing {file_path} - Detected Weapon: {weapon_name}")

    modified_content = content

    # Modify zombie/skeleton kill count from 100 to 50
    modified_content = re.sub(r'(\bentity:\s*"minecraft:zombie".*?\bvalue:\s*)\d+L', r'\g<1>30L', modified_content, flags=re.DOTALL)
    modified_content = re.sub(r'(\bentity:\s*"minecraft:skeleton".*?\bvalue:\s*)\d+L', r'\g<1>15L', modified_content, flags=re.DOTALL)
    
    modified_content = re.sub(r'(\bentity:\s*"minecraft:spider".*?\bvalue:\s*)\d+L', r'\g<1>20L', modified_content, flags=re.DOTALL)
    modified_content = re.sub(r'(\bentity:\s*"minecraft:stray".*?\bvalue:\s*)\d+L', r'\g<1>15L', modified_content, flags=re.DOTALL)

    # Modify pillager, vindicator, and witch kill counts
    modified_content = re.sub(r'(\bentity:\s*"minecraft:pillager".*?\bvalue:\s*)\d+L', r'\g<1>15L', modified_content, flags=re.DOTALL)
    modified_content = re.sub(r'(\bentity:\s*"minecraft:vindicator".*?\bvalue:\s*)\d+L', r'\g<1>10L', modified_content, flags=re.DOTALL)
    modified_content = re.sub(r'(\bentity:\s*"minecraft:witch".*?\bvalue:\s*)\d+L', r'\g<1>7L', modified_content, flags=re.DOTALL)
    
    modified_content = re.sub(r'(\bentity:\s*"variantsandventures:gelid".*?\bvalue:\s*)\d+L', r'\g<1>15L', modified_content, flags=re.DOTALL)
    modified_content = re.sub(r'(\bentity:\s*"variantsandventures:thicket".*?\bvalue:\s*)\d+L', r'\g<1>15L', modified_content, flags=re.DOTALL)
    modified_content = re.sub(r'(\bentity:\s*"minecraft:husk".*?\bvalue:\s*)\d+L', r'\g<1>15L', modified_content, flags=re.DOTALL)
    
    modified_content = re.sub(r'(\bentity:\s*"born_in_chaos_v1:zombie_bruiser".*?\bvalue:\s*)\d+L', r'\g<1>3L', modified_content, flags=re.DOTALL)
    modified_content = re.sub(r'(\bentity:\s*"born_in_chaos_v1:skeleton_thrasher".*?\bvalue:\s*)\d+L', r'\g<1>3L', modified_content, flags=re.DOTALL)
    modified_content = re.sub(r'(\bentity:\s*"born_in_chaos_v1:nightmare_stalker".*?\bvalue:\s*)\d+L', r'\g<1>3L', modified_content, flags=re.DOTALL)
    
    modified_content = re.sub(r'(\bentity:\s*"mutantmonsters:mutant_zombie".*?\bvalue:\s*)\d+L', r'\g<1>3L', modified_content, flags=re.DOTALL)
    modified_content = re.sub(r'(\bentity:\s*"mutantmonsters:mutant_skeleton".*?\bvalue:\s*)\d+L', r'\g<1>3L', modified_content, flags=re.DOTALL)
    modified_content = re.sub(r'(\bentity:\s*"crimsonsteves_mutant_mobs:mutant_skeleton".*?\bvalue:\s*)\d+L', r'\g<1>2L', modified_content, flags=re.DOTALL)

    modified_content = re.sub(r'(\bentity:\s*"born_in_chaos_v1:missioner".*?\bvalue:\s*)\d+L', r'\g<1>1L', modified_content, flags=re.DOTALL)
    modified_content = re.sub(r'(\bentity:\s*"fromtheshadows:nehemoth".*?\bvalue:\s*)\d+L', r'\g<1>1L', modified_content, flags=re.DOTALL)
    
    modified_content = re.sub(r'\bentity:terra_entity:eye_of_cthulhu\b', 'terra_entity:eye_of_cthulhu', modified_content)
    modified_content = re.sub(r'\bterra_entity:eye_of_cthulhu_spawn_egg\b', 'terra_entity:cthulhu_eye_spawn_egg', modified_content)
    modified_content = re.sub(r'\bmajruszsdifficulty:wither_treasure_bag\b', 'minecraft:wither_skeleton_skull', modified_content)
    
    modified_content = re.sub(r'\bthe_spino:spino\b', 'cartoon_soul:observer', modified_content)
    modified_content = re.sub(r'\bthe_spino:tooth\b', 'cartoon_soul:theobserver', modified_content)
    
    modified_content = re.sub(r'\billageandspillage:spiritcaller\b', 'razor_tyrant:razor_tyrant', modified_content)
    modified_content = re.sub(r'\billageandspillage:spellbound_book\b', 'create:electron_tube', modified_content)
    
    modified_content = re.sub(r'\bfromtheshadows:nehemoth\b', 'threateningly_mobs:ferox_ice_worm', modified_content)
    modified_content = re.sub(r'\bfromtheshadows:crystallized_blood\b', 'threateningly_mobs:ice_demon_eyes', modified_content)
    
    modified_content = re.sub(r'\bborn_in_chaos_v1:missioner\b', 'terra_entity:brain_of_cthulhu', modified_content)
    modified_content = re.sub(r'\bborn_in_chaos_v1:missionary_hat_helmet\b', 'terra_entity:brain_of_cthulhu_spawn_egg', modified_content)
    
    modified_content = re.sub(r'\bterramity:void_alloy\b', 'terramity:reverium', modified_content)

    modified_content = re.sub(fr'\+0\.25 {weapon_name} Damage', fr'+0.5 {weapon_name} Damage', modified_content)
    modified_content = re.sub(fr'\+3.5 {weapon_name} Damage', fr'+3 {weapon_name} Damage', modified_content)

    
    # Update subtitle text
    modified_content = re.sub(
        fr'subtitle: "Kill 20 Pillagers, Vindicators, and 7 Witches with {weapon_name}"',
        f'subtitle: "Kill 15 Pillagers, 10 Vindicators, and 7 Witches with {weapon_name}"',
        modified_content
    )
    modified_content = re.sub(
        fr'subtitle: "Kill 20 Gelid, Thickets, and Husks with {weapon_name}"',
        f'subtitle: "Kill 15 Gelid, Thickets, and Husks with {weapon_name}"',
        modified_content
    )
    
    modified_content = re.sub(
        fr'subtitle: "Kill 25 Spiders and 20 Strays with {weapon_name}"',
        f'subtitle: "Kill 20 Spiders and 15 Strays with {weapon_name}"',
        modified_content
    )
    modified_content = re.sub(
        fr'subtitle:\s*"Kill\s*6\s*Zombie bruisers,\s*Skeleton thrashers,\s*and\s*3 Nightmare Stalkers with {weapon_name}"',
        f'subtitle: "Kill 3 Zombie bruisers, Skeleton thrashers, and 3 Nightmare Stalkers with {weapon_name}"',
        modified_content
    )
    modified_content = re.sub(
        r'subtitle:\s*"Kill\s*3\s*Mutant Zombies,\s*Skeletons,\s*and\s*Stunt Skeletons"',
        f'subtitle: "Kill 3 Mutant Zombies, Skeletons, and Stunt Skeletons with {weapon_name}"',
        modified_content
    )
    modified_content = re.sub(
        fr'subtitle:\s*"Kill One Missioner,\s*Nehemoth,\s*Lich,\s*Solscarab Maximus,\s*and\s*Steel Boar with {weapon_name}"',
        f'subtitle: "Kill One Brain of Cthulhu, Ferox Ice Worm, Lich, Solscarab Maximus, and Steel Boar with {weapon_name}"',
        modified_content
    )
    modified_content = re.sub(
        fr'subtitle:\s*"Kill\s*30\s*Zombies\s*and\s*20\s*Skeletons with {weapon_name}"',
        f'subtitle: "Kill 30 Zombies and 15 Skeletons with {weapon_name}"',
        modified_content
    )
    modified_content = re.sub(
        fr'subtitle: "Kill 1 Wither, Pigzilla, Eye of Cthulu, Spiritcaller, Spinowane, and Corundum Guardian with {weapon_name}"',
        f'subtitle: "Kill 1 Wither, Pigzilla, Eye of Cthulu, Razor Tyrant, Observer, and Corundum Guardian with {weapon_name}"',
        modified_content
    )
    modified_content = re.sub(
        r'subtitle: "Kill 1 Super Sniffer"',
        f'subtitle: "Kill 1 Super Sniffer with {weapon_name}"',
        modified_content
    )
    modified_content = re.sub(
        fr'''description: [
				"The Spiritcaller can be fought during raids in the final wave"
				""
				"The Spinowane has a low chance of spawning at night."
				""
				"The Corundum Guardian can be summoned by using the Corundum Guardian Memory item."
				""
				"Pigzilla starts out as Biting Pig and slowing kills and gets larger into Pigzilla."
			]''',
        fr'''description: [
				"The Observer can be found throughout the land"
				""
				"The Razor Tyrant can be summoned via spawn egg"
				""
				"The Corundum Guardian can be summoned by using the Corundum Guardian Memory item."
				""
				"Pigzilla starts out as Biting Pig and slowing kills and gets larger into Pigzilla."
			]''',
        modified_content
    )
    
    damage = modify_damage_values(content)
    print(damage)
    
    
######## Damage #########
    
    # Save the modified file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(modified_content)
    
    # with open(file_path, "w") as file:
    #     file.write(damage)

def process_folder(folder_path):
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        return
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):  # Process only files
            modify_quest_file(file_path)

if __name__ == "__main__":
    process_folder("/Users/nicholasburczyk/Documents/curseforge/minecraft/Instances/Server V3 (Guns) (1)/config/ftbquests/quests/chapters")
