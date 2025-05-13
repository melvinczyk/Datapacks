def batch_update_effects_in_file(filename, updates):
    """
    :param filename: str - Path to the input file
    :param updates: dict - {entity_id: {effect_id: new_level, ...}, ...}
    """
    updated_lines = []

    with open(filename, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            if not stripped_line or "': '" not in stripped_line:
                updated_lines.append(line)
                continue

            entity_id = stripped_line.split("': '")[0].strip("'")
            if entity_id in updates:
                try:
                    prefix, effect_string = stripped_line.split("': '", 1)
                    effect_string = effect_string.rstrip("'")
                    effects = effect_string.split('|')

                    new_effects = []
                    for effect in effects:
                        if ',' in effect:
                            eff_id, lvl_part = effect.split(',lvl:')
                            if eff_id in updates[entity_id]:
                                new_lvl = updates[entity_id][eff_id]
                                new_effects.append(f"{eff_id},lvl:{new_lvl}")
                            else:
                                new_effects.append(effect)
                        else:
                            new_effects.append(effect)

                    updated_line = f"'{prefix}': '{'|'.join(new_effects)}'\n"
                    updated_lines.append(updated_line)
                except Exception as e:
                    print(f"Error processing line: {line}")
                    updated_lines.append(line)
            else:
                updated_lines.append(line)

    with open(filename, 'w') as file:
        file.writelines(updated_lines)

# Example usage:
updates = {
    'terramity:gob': {
        'minecraft:resistance': 2,
        'minecraft:fire_resistance': 4
    },
    'terramity:trial_guardian': {
        'minecraft:resistance': 2
    },
    "cartoon_soul:furious": {
        'minecraft:resistance': 2,
        'minecraft:fire_resistance': 4
    },
    "cartoon_soul:jesterknight": {
        'minecraft:resistance': 2,
        'minecraft:fire_resistance': 4
    },
    'razor_tyrant:razor_tyrant': {
        'minecraft:resistance': 2,
        'minecraft:fire_resistance': 4
    },
    'corundumguardian:corundum_guardian': {
        'minecraft:resistance': 2,
        'minecraft:fire_resistance': 4
    },
    "cartoon_soul:hand": {
        'minecraft:resistance': 2,
        'minecraft:fire_resistance': 4
    },
    "cartoon_soul:frostguardian": {
        'minecraft:resistance': 2,
        'minecraft:fire_resistance': 4
    },
    "terramity:super_sniffer": {
        'minecraft:resistance': 2,
        'minecraft:fire_resistance': 4
    },
    "terramity:ultra_sniffer": {
        'minecraft:resistance': 2,
        'minecraft:fire_resistance': 4
    },
    "eeeabsmobs:nameless_guardian": {
        'minecraft:resistance': 1,
        'minecraft:fire_resistance': 4
    },
    "cataclysm:ignis": {
        'minecraft:resistance': 1,
        'minecraft:fire_resistance': 4
    },
    "cataclysm:netherite_monstrosity": {
        'minecraft:resistance': 1,
        'minecraft:fire_resistance': 4
    },
    "cataclysm:the_harbinger": {
        'minecraft:resistance': 2,
        'minecraft:fire_resistance': 4
    },
    "cataclysm:ancient_remnant": {
        'minecraft:resistance': 1,
        'minecraft:fire_resistance': 4
    },
    "threateningly_mobs:solscarab_maximus": {
        'minecraft:resistance': 1,
        'minecraft:fire_resistance': 4
    },
    "threateningly_mobs:inferno": {
        'minecraft:resistance': 1,
        'minecraft:fire_resistance': 4
    },
    "threateningly_mobs:lich": {
        'minecraft:resistance': 1,
        'minecraft:fire_resistance': 4
    },
    "threateningly_mobs:terra_dragon": {
        'minecraft:resistance': 1,
        'minecraft:fire_resistance': 4
    },
    "terra_entity:eye_of_cthulhu": {
        'minecraft:resistance': 1,
        'minecraft:fire_resistance': 4
    },
    "terra_entity:skeletron": {
        'minecraft:resistance': 1,
        'minecraft:fire_resistance': 4
    },
    "terra_entity:king_slime": {
        'minecraft:resistance': 1,
        'minecraft:fire_resistance': 4
    },
    "terra_entity:eater_of_worlds": {
        'minecraft:resistance': 1,
        'minecraft:fire_resistance': 4
    },
    "terra_entity:brain_of_cthulhu": {
        'minecraft:resistance': 1,
        'minecraft:fire_resistance': 4
    }
}

batch_update_effects_in_file('/Users/nicholasburczyk/Desktop/Minecraft server stuff/Datapacks/Server Season 3/permanenteffects.txt', updates)
