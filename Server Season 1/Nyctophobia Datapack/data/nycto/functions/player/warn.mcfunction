execute store result score @s grue.rng run loot spawn ~ ~ ~ loot nycto:rng/1-6
execute if score @s grue.rng matches 1 run title @s actionbar [{"text": "The grue is coming","color": "dark_gray"}]
execute if score @s grue.rng matches 2 run title @s actionbar [{"text": "Watch out!!!","color": "dark_gray"}]
execute if score @s grue.rng matches 3 run title @s actionbar [{"text": "He is watching","color": "dark_gray"}]
execute if score @s grue.rng matches 4 run title @s actionbar [{"text": "You feel like you are watched","color": "dark_gray"}]
execute if score @s grue.rng matches 5 run title @s actionbar [{"text": "You feel uneasy","color": "dark_gray"}]
execute if score @s grue.rng matches 6 run title @s actionbar [{"text": "Heavy breathing approaches slowly","color": "dark_gray"}]