summon minecraft:husk ~ ~ ~ {CanBreakDoors:1,CustomName:'[{"text":"Grue"}]',Health:800,Silent:1b,Tags:["grue.gruemob"],ActiveEffects:[{Id:14,Duration:1000000,Amplifier:1,ShowParticles:0b}],ArmorItems:[{},{},{},{id:"string",tag:{CustomModelData:557001},Count:1}],ArmorDropChances:[0f,0f,0f,0.00f],Attributes:[{Name:"generic.movement_speed",Base:0.5d},{Name:"generic.attack_damage",Base:300d},{Name:"generic.max_health",Base:800d}]}
playsound minecraft:grue.growl1 hostile @a ~ ~ ~ 1
execute as @a[distance=..8] at @s run playsound minecraft:grue.spawn hostile @s ~ ~ ~ 0.8
execute as @a[distance=9..30] at @s run playsound minecraft:grue.mistake hostile @s ~ ~ ~ 0.8