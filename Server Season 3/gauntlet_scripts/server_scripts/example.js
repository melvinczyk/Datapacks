ServerEvents.recipes(event => {
  // Totem of Mech
  event.shaped('cartoon_soul:totemofmech', [
    ' A ',
    'IBI',
    ' I '
  ], {
    A: 'immersive_weathering:mossy_stone',
    I: 'minecraft:iron_block',
    B: 'minecraft:totem_of_undying'
  }).id('kubejs:totem_of_mech_recipe');

  // Totem of Freak
  event.shaped('cartoon_soul:totem_of_freak', [
    ' A ',
    'BCB',
    ' D '
  ], {
    A: 'terramity:red_gnome_hat_helmet',
    B: 'terramity:prismatic_crystal_block',
    C: 'minecraft:totem_of_undying',
    D: 'terramity:amethyst_block'
  }).id('kubejs:totem_of_freak_recipe');

  // Creator Hand Spawn Egg
  event.shaped('cartoon_soul:hand_spawn_egg', [
    'GII',
    'BDI',
    ' I '
  ], {
    G: 'minecraft:gold_block',
    I: 'minecraft:iron_block',
    B: 'terramity:prismatic_crystal_block',
    D: 'minecraft:diamond'
  }).id('kubejs:creator_hand_recipe');

  // Corundum Guardian Spawn Egg
  event.shaped('corundumguardian:corundum_guardian_spawn_egg', [
    'TTT',
    'EBE',
    'T T'
  ], {
    T: 'scguns:treated_iron_block',
    E: 'create:electron_tube',
    B: 'terramity:battery',
    ' ': 'minecraft:air'
  }).id('kubejs:corundum_spawn_recipe');

  // Observer Spawn Egg
  event.shaped('cartoon_soul:observer_spawn_egg', [
    'VVV',
    'RBR',
    'W W'
  ], {
    V: 'create:cut_veridium',
    R: 'minecraft:redstone',
    B: 'create:experience_block',
    W: 'create:cut_veridium_wall'
  }).id('kubejs:observer_spawn_recipe');

  // Furious Light
  event.shaped('cartoon_soul:furious_light', [
    'I I',
    'NB ',
    'NNN'
  ], {
    I: 'scguns:treated_iron_ingot',
    N: 'minecraft:nether_bricks',
    B: 'born_in_chaos_v1:bone_heart'
  }).id('kubejs:furious_recipe');

  // Frost Guardian Spawn Egg
  event.shaped('cartoon_soul:frostguardian_spawn_egg', [
    'BPB',
    'PSP',
    'BPB'
  ], {
    B: 'minecraft:blue_ice',
    P: 'philipsruins:frozen_prismarine',
    S: 'terramity:sapphire'
  }).id('kubejs:frost_guardian_recipe');

  // Razor Tyrant Spawn Egg
  event.shaped('razor_tyrant:razor_tyrant_spawn_egg', [
    'ITI',
    'ERE',
    ' B '
  ], {
    I: 'minecraft:iron_block',
    T: 'scguns:treated_iron_block',
    E: 'create:electron_tube',
    R: 'minecraft:redstone_block',
    B: 'minecraft:blast_furnace'
  }).id('kubejs:razor_spawn_recipe');

  // MonstroSteve Spawn Egg
  event.shaped('monstrosteve:monstrosteve_spawn_egg', [
    'CSC',
    'BBB',
    'GGG'
  ], {
    C: 'minecraft:cyan_concrete',
    S: 'minecraft:skeleton_skull',
    B: 'minecraft:blue_concrete',
    G: 'minecraft:gray_concrete'
  }).id('kubejs:steve_spawn_recipe');

  // Creative Picture Frame
  event.shaped('littleframes:creative_pic_frame', [
    'PPP',
    'PPP',
    'PPP'
  ], {
    P: 'minecraft:oak_planks'
  }).id('kubejs:frame_recipe');
});
