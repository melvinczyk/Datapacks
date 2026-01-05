import os
import json

# === CONFIGURATION ===
BASE_DIR = "trophies/data"                     # Base directory to search for trophies
OUTPUT_LOOT_TABLE = "random_trophy.json"       # Output file for loot table
IGNORE_ENTITIES = {
  "mokels_boss_mantyd:boss_mantyd",
  "threateningly_mobs:solscarab_maximus",
  "threateningly_mobs:inferno",
  "threateningly_mobs:lich",
  "jeg:terror_phantom",
  "bosses_of_mass_destruction:lich",
  "bosses_of_mass_destruction:void_blossom",
  "bosses_of_mass_destruction:gauntlet",
  "bosses_of_mass_destruction:obsidilith",
  "theinkarena:blot",
  "terra_entity:queen_bee",
  "terra_entity:king_slime",
  "terra_entity:eye_of_cthulhu",
  "terra_entity:skeletron",
  "terra_entity:brain_of_cthulhu",
  "terra_entity:eater_of_worlds",
  "monstrosteve:monstrosteve",
  "alexsmobs:void_worm",
  "illageandspillage:magispeller",
  "illageandspillage:freakager",
  "illageandspillage:spiritcaller",
  "terramity:super_sniffer",
  "terramity:gob",
  "terramity:trial_guardian",
  "terramity:ultra_sniffer",
  "terramity:gundalf",
  "corundumguardian:corundum_guardian",
  "born_in_chaos_v1:lord_pumpkinhead_withouta_horse",
  "born_in_chaos_v1:lord_pumpkinhead",
  "born_in_chaos_v1:lords_felsteed",
  "hs_bosses:sand_warrior",
  "cartoon_soul:observer",
  "cartoon_soul:dwarfgolem",
  "cartoon_soul:furious",
  "cartoon_soul:frostguardian",
  "cartoon_soul:jesterknight",
  "cartoon_soul:hand",
  "macabre:gargamaw",
  "macabre:the_hollow_man",
  "macabre:gomoria",
  "macabre:valamon",
  "macabre:morphegor",
  "macabre:baal",
  "the_spino:spino",
  "razor_tyrant:razor_tyrant",
  "pigzilla:pigzilla",
  "mythsandlegends:black_charro",
  "whisperwoods:hirschgeist",
  "cataclysm:ignis",
  "cataclysm:ancient_remnant",
  "cataclysm:ender_guardian",
  "cataclysm:maledictus",
  "cataclysm:netherite_monstrosity",
  "cataclysm:the_harbinger",
  "mofus_better_end_:reborn_litch",
  "mofus_better_end_:endermite_queen",
  "mofus_better_end_:eye_guardian",
  "mofus_better_end_:forgotten_litch",
  "eeeabsmobs:nameless_guardian"
}


# === FIND ENTITY IDS ===
entity_ids = []

for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".json") and "/trophies/" in os.path.join(root, file).replace("\\", "/"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    entity_id = data.get("entity")
                    if entity_id and entity_id not in IGNORE_ENTITIES:
                        entity_ids.append(entity_id)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Skipping {file_path}: {e}")

# === BUILD LOOT TABLE ===
loot_table = {
    "type": "minecraft:chest",
    "pools": [
        {
            "rolls": 1,
            "entries": []
        }
    ]
}

for entity in sorted(set(entity_ids)):
    entry = {
        "type": "minecraft:item",
        "name": "obtrophies:trophy",
        "functions": [
            {
                "function": "minecraft:set_nbt",
                "tag": f"{{BlockEntityTag:{{entity:\"{entity}\"}}}}"
            }
        ]
    }
    loot_table["pools"][0]["entries"].append(entry)

# === OUTPUT ===
with open(OUTPUT_LOOT_TABLE, "w", encoding="utf-8") as out_file:
    json.dump(loot_table, out_file, indent=2)

print(f"Generated loot table with {len(loot_table['pools'][0]['entries'])} entries to '{OUTPUT_LOOT_TABLE}'")
