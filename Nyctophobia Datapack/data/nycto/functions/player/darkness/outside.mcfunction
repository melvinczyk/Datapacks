playsound minecraft:grue.escape hostile @s[tag=nycto.indarkness,scores={grue.darknesstimer=1..330}]

title @s[tag=nycto.indarkness,scores={grue.darknesstimer=1..150}] actionbar [{"text": "You escaped... This time","color": "red"}]


execute if score .diff grue.diff matches 1 run scoreboard players set @s grue.darknesstimer 3600
execute if score .diff grue.diff matches 2 run scoreboard players set @s grue.darknesstimer 3000
execute if score .diff grue.diff matches 3 run scoreboard players set @s grue.darknesstimer 378


stopsound @s hostile minecraft:grue.warning

tag @s[tag=nycto.indarkness] remove nycto.indarkness