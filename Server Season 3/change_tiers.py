import re

def update_tier_in_file(filepath, delete_rewards):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    # 1. Change tier 5 to 4 in champions:champion
    tier_pattern = r'("champions:champion":\s*\{\s*tier:\s*)5(\s*\})'
    content = re.sub(tier_pattern, r'\g<1>3\g<2>', content)

    # 2. Replace "Ultimate" with "Legendary"
    content = re.sub(r'\bUltimate\b', 'Elite', content)

    # 3. Remove all rewards: [ ... ] blocks (greedy match, spans newlines)
    if delete_rewards:
        content = re.sub(r'rewards:\s*\[\s*.*?\s*\](?=\s*\w+:)', '', content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"File updated: {filepath}")

# Example usage
update_tier_in_file("/Users/nicholasburczyk/Documents/curseforge/minecraft/Instances/Server V3 (Guns) (1)/config/ftbquests/quests/chapters/elite_mobs.snbt", True)
