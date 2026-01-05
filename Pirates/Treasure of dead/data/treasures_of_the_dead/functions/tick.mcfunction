#ROTATING SKULLS
execute as @e[tag=TOTD_Rotate] at @s run tp @s ~ ~ ~
execute as @e[tag=TOTD_Rotate] at @s run tag @s remove TOTD_Rotate

#SHADOW SKELETONS PARTICLES
execute at @e[type=treasures_of_the_dead:shadow_skeleton, nbt={IsShadow:1b}] run particle minecraft:smoke ~ ~1 ~ 0.25 0.5 0.25 0.01 10
execute at @e[type=treasures_of_the_dead:captain_shadow_skeleton, nbt={IsShadow:1b}] run particle minecraft:smoke ~ ~1 ~ 0.25 0.5 0.25 0.01 10

#execute at @e[type=treasures_of_the_dead:totd_skeleton, nbt={IsGoingToBlowUp:1b}] run particle minecraft:smoke ~ ~1 ~ 0.25 0.5 0.25 0.01 10

#CAPTAIN NAMES VISIBILITY
execute as @e[type=treasures_of_the_dead:captain_skeleton] run team join CaptainSkeletons @s
execute as @e[type=treasures_of_the_dead:captain_blooming_skeleton] run team join CaptainSkeletons @s
execute as @e[type=treasures_of_the_dead:captain_shadow_skeleton] run team join CaptainSkeletons @s
execute as @e[type=treasures_of_the_dead:captain_golden_skeleton] run team join CaptainSkeletons @s
#execute as @e[team=CaptainSkeletons] at @s if entity @p[distance=..8] run data merge entity @s {CustomNameVisible:1}
#execute as @e[team=CaptainSkeletons] at @s if entity @p[distance=8..] run data merge entity @s {CustomNameVisible:0}

