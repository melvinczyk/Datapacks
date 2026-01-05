import os
import re

# === Paths (update these as needed) ===
correct_folder = "/Users/nicholasburczyk/Desktop/ftbquests/quests/chapters"
corrupted_folder = "/Users/nicholasburczyk/Documents/curseforge/minecraft/Instances/Server V3 (Guns) (1)/config/ftbquests/quests/chapters"
output_folder = "/Users/nicholasburczyk/Desktop/new quests/quests/chapters"

os.makedirs(output_folder, exist_ok=True)

def extract_tasks_by_id(text):
    """Extract all task blocks keyed by task id from a quest file."""
    task_pattern = re.compile(
        r'(id: "(?P<id>[A-F0-9]+)".*?type: "(?P<type>[^"]+)".*?)(?=\n\s*(?:id:|\]|}))',
        re.DOTALL
    )
    return {match.group("id"): match.group(1).strip() for match in task_pattern.finditer(text)}

def replace_custom_tasks(corrupted_content, correct_tasks_map):
    """Replace all tasks of type 'custom' in the corrupted file using the correct tasks."""
    def replacer(match):
        full_task = match.group(0)
        task_id = match.group("id")
        task_type = match.group("type")

        if task_type == "custom" and task_id in correct_tasks_map:
            print(f"  Replacing custom task {task_id}")
            return correct_tasks_map[task_id]
        return full_task

    task_regex = re.compile(
        r'(?P<full>(id: "(?P<id>[A-F0-9]+)".*?type: "(?P<type>[^"]+)".*?))(?=\n\s*(?:id:|\]|}))',
        re.DOTALL
    )

    return task_regex.sub(replacer, corrupted_content)

# === Main Processing ===
for filename in os.listdir(correct_folder):
    if not filename.endswith(".snbt"):
        continue

    correct_path = os.path.join(correct_folder, filename)
    corrupted_path = os.path.join(corrupted_folder, filename)
    output_path = os.path.join(output_folder, filename)

    if not os.path.exists(corrupted_path):
        print(f"⚠️ Skipping {filename}: no matching corrupted file.")
        continue

    with open(correct_path, "r", encoding="utf-8") as f:
        correct_content = f.read()

    with open(corrupted_path, "r", encoding="utf-8") as f:
        corrupted_content = f.read()

    correct_tasks = extract_tasks_by_id(correct_content)
    fixed_content = replace_custom_tasks(corrupted_content, correct_tasks)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(fixed_content)

    print(f"✅ Fixed: {filename}")

print("\n✅ All files processed.")
