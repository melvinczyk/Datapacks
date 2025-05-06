import re
import sys

def modify_quest_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return

    modified_content = content

    # Change all `xp_levels` values to 35
    modified_content = re.sub(r'(\bid:\s*".*?"\s*type:\s*"xp_levels"\s*xp_levels:\s*)\d+', r'\g<1>35', modified_content)

    # Ensure gunpowder count is at least 40
    modified_content = re.sub(r'(\bcount:\s*)([0-3]?[0-9])(\s*id:\s*".*?"\s*item:\s*"minecraft:gunpowder"\s*type:\s*"item")', r'\g<1>40\g<3>', modified_content)

    # Save the modified file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(modified_content)

    print(f"Updated xp_levels and gunpowder count in {file_path}")

if __name__ == "__main__":
    modify_quest_file("/Users/nicholasburczyk/Documents/curseforge/minecraft/Instances/Server V3 (Guns)/config/ftbquests/quests/chapters/miniboss.snbt")
