tellraw @a [{"text": "[Nyctophobia] ","bold": true,"color": "green"},{"text": "Remember to set the difficulty of the datapack using /function nycto:difficulty/(difficulty) or the datapack will not work. Also turn your hostile mob sounds up for an optimal experience!","color": "yellow","bold": false}]

# - Schedules

schedule clear nycto:tick_20t
schedule function nycto:tick_20t 20t

function nycto:difficulty/normal

# - Scoreboards

scoreboard objectives add grue.darknesstimer dummy
scoreboard objectives add grue.rng dummy
scoreboard objectives add grue.diff dummy

# - Settings



# - General