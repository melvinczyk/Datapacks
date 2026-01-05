const mobs2 = [
  { id: 'netherexp:banshee', tag: 'gauntlet_1' },
  { id: 'terra_entity:devourer', tag: 'gauntlet_2' },
  { id: 'terramity:duskrok', tag: 'gauntlet_3' },
  { id: 'luminous_nether:soul_furnace', tag: 'gauntlet_4' },
  { id: 'fromtheshadows:nehemoth', tag: 'gauntlet_5' }
]

const countdownSeconds2 = 10
const seconds2 = 60
const timeLimitTicks2 = 20 * seconds2

let activeGauntlets = new Map() // uuid string → { round, entityId, timeoutTask, waiting, failed }
let scheduledCountdowns = new Map() // uuid string → [scheduledTask]
let gauntletSpawnPositions = new Map(); // uuid string → {x, y, z}\
let gauntletParticleTasks = new Map(); // uuid string → repeating task


ServerEvents.commandRegistry(event => {
  const { commands: Commands } = event

  event.register(
    Commands.literal('start_soul_fire_gauntlet')
      .requires(src => true)
      .executes(ctx => {
        const player = ctx.source.getPlayerOrException();
        const uuidStr = String(player.uuid);

        if (activeGauntlets.has(uuidStr)) {
          player.tell(Text.red("❌ You are already in a gauntlet!"));
          return 0;
        }

        const pos = player.blockPosition(); // Capture position once at command start

        activeGauntlets.set(uuidStr, {
          round: 0,
          entity: null,
          timeoutTask: null,
          waiting: false,
          failed: false,
          completed: false,
          spawnPos: pos // Store player's starting position here
        });

        startPreSpawnCountdown(player, 0);

        return 1;
      })
  );
})

function startPreSpawnCountdown(player, round) {
  const preSpawncountdownSeconds = 10;
  player.runCommandSilent('title @s title {"text":"Soul Fire Gauntlet","color":"aqua"}')
  player.runCommandSilent(`title @s subtitle {"text":"Starting in ${preSpawncountdownSeconds} seconds","color":"yellow"}`)
  const uuidStr = String(player.uuid);

  for (let i = 1; i <= preSpawnCountdownSeconds; i++) {
    let currentSecond = i;
    player.server.scheduleInTicks(currentSecond * 20, () => {
      let secondsLeft = preSpawnCountdownSeconds - currentSecond;
      if (secondsLeft > 0) {
        if (4 > secondsLeft > 0)
        {
          player.tell(Text.yellow(`${secondsLeft}`));
        }
      } else {
        startRound(player, round); // Start the first wave after countdown
      }
    });
  }
}

function startRound(player, round) {
  const uuidStr = String(player.uuid)

  const state = activeGauntlets.get(uuidStr)
  if (!state) {
    return // Safety check
  }

  const pos = state.spawnPos // Use stored spawn position
  
  if (round >= mobs2.length) {
    
    // Check if already completed to prevent double execution
    if (state.completed) {
      return
    }
    
    // Mark as completed immediately to prevent double execution
    state.completed = true
    activeGauntlets.set(uuidStr, state)
    
    
    // Add title command first
    try {
      player.runCommandSilent('title @s title {"text":"VICTORY!","color":"gold","bold":true}')
      player.runCommandSilent('title @s subtitle {"text":"Gauntlet Complete!","color":"green"}')
    } catch (e) {
    }
    
    try {
      player.runCommandSilent(`playsound minecraft:entity.player.levelup master @a ${pos.x} ${pos.y} ${pos.z} 1 1`)
    } catch (e) {
      // Try alternative playsound syntax
      try {
        player.runCommandSilent(`playsound minecraft:entity.player.levelup master @s`)
      } catch (e2) {
      }
    }
    
    // === Complete the FTB Quest ===
    let teamData = player.ftbTeamData;
let questId = "3E21D301D4051643";

try {
  player.server.runCommandSilent(`ftbquests change_progress ${player.name.string} complete ${questId}`);
  player.tell(Text.green("✅ Quest marked complete!"));
} catch (e) {
  console.log(`[Gauntlet] ❌ Failed to run quest completion command: ${e}`);
}

    
    // Add a small delay before cleanup
    player.server.scheduleInTicks(1, () => {
      activeGauntlets.delete(uuidStr)
    })
    return
  }

  const mobData = mobs2[round]
  const level = player.level

  // Summon the champion mob using the command (tier 3 for example)
  player.runCommandSilent(`champions summonpos ${pos.x} ${pos.y} ${pos.z} ${mobData.id} 5`)
  player.runCommandSilent(`playsound terramity:ultra_sniffer_teleport master @a ${pos.x} ${pos.y} ${pos.z} 1 1`)

  // Wait a tick or two to let the mob spawn
  player.server.scheduleInTicks(2, () => {
    const allEntities = level.getAllEntities()
    let championEntity = null

    for (const ent of allEntities) {
      if (!ent.tags) continue
      if (ent.tags.contains(mobData.tag)) continue
      if (ent.type !== mobData.id) continue

      // Use let instead of var here
      let dx = ent.x - pos.x
      let dy = ent.y - pos.y
      let dz = ent.z - pos.z
      let distance = Math.sqrt(dx * dx + dy * dy + dz * dz)
      if (distance > 5) continue

      let nbt = ent.getNbt()
      if (!nbt) continue
      let forgeSpawnType = nbt.getString('forge:spawn_type')
      if (forgeSpawnType !== 'COMMAND') continue

      championEntity = ent
      break
    }

    if (!championEntity) {
      player.tell(Text.red("❌ Failed to spawn champion mob for this wave!"))
      activeGauntlets.delete(uuidStr)
      return
    }
    
    player.runCommandSilent(`effect give ${championEntity.uuid} terramity:immunity 30 1 true`)

    championEntity.addTag(mobData.tag)
    championEntity.glowing = true
    championEntity.addTag("persistent")
    championEntity.addTag(`gauntlet_player_${uuidStr}`)
    championEntity.addTag(`gauntlet_round_${round}`)
    championEntity.customName = Text.aqua(`Wave ${round + 1}`)
    championEntity.customNameVisible = true

    player.tell(Text.gold(`Wave ${round + 1} has begun!!`))
    player.tell(Text.gray(`⏱ You have ${timeLimitTicks2 / 20} seconds.`))

    const timeoutTask = player.server.scheduleInTicks(timeLimitTicks2, () => {
      const state = activeGauntlets.get(uuidStr)
      if (!state || state.round !== round || state.waiting) return

      const allEntities = player.level.getAllEntities()
      let found = false

      player.runCommandSilent('title @s title {"text":"❌ YOU FAILED!","color":"red","bold":true}')
      player.runCommandSilent(`playsound terramity:fail master @a ${pos.x} ${pos.y} ${pos.z} 1 1`)
      activeGauntlets.delete(uuidStr)
      cancelCountdown(uuidStr)
      
      for (const ent of allEntities) {
        if (
          ent.tags &&
          ent.tags.contains(`gauntlet_round_${round}`) &&
          ent.tags.contains(`gauntlet_player_${uuidStr}`) &&
          !ent.isRemoved()
        ) {
          ent.discard()
          found = true
          break
        }
      }

      if (!found) {
      }
    })

    activeGauntlets.set(uuidStr, {
      round: round,
      entity: championEntity,
      timeoutTask: timeoutTask,
      waiting: false,
      failed: false,
      completed: false,
      spawnPos: pos
    })

    // Notify player when 3 seconds are left
const warningTask = player.server.scheduleInTicks((timeLimitTicks2 - 100), () => {
  const state = activeGauntlets.get(uuidStr)
  if (!state || state.round !== round || state.failed || state.waiting) return

  player.tell(Text.red("5 seconds remaining!"))
  player.runCommandSilent(`playsound minecraft:block.note_block.pling master @s ~ ~ ~ 1 2`)
})

  })
}

function cancelCountdown(uuidStr) {
  if (scheduledCountdowns.has(uuidStr)) {
    var tasks = scheduledCountdowns.get(uuidStr)
    if (Array.isArray(tasks)) {
      tasks.forEach(task => {
        if (task && typeof task.cancel === "function") {
          try {
            task.cancel()
          } catch (e) {
            // Ignore cancellation errors
          }
        }
      })
    }
    scheduledCountdowns.delete(uuidStr)
  }
}

function startNextRoundCountdown(player, nextRound) {
  const uuidStr = String(player.uuid)
  cancelCountdown(uuidStr)

  const currentState = activeGauntlets.get(uuidStr)
  if (currentState) {
    currentState.waiting = true
    currentState.failed = false
    if (currentState.timeoutTask && typeof currentState.timeoutTask.cancel === "function") {
      currentState.timeoutTask.cancel()
    }
    activeGauntlets.set(uuidStr, currentState)
  }

  player.tell(Text.yellow(`Next wave in ${countdownSeconds2} seconds...`))

  const countdownTasks = []
  for (let i = 1; i <= countdownSeconds2; i++) {
    let currentSecond = i; // Capture current loop index
    var task = player.server.scheduleInTicks(currentSecond * 20, () => {
      const state = activeGauntlets.get(uuidStr);
      if (!state || state.failed) return;

      const secondsLeft = countdownSeconds2 - currentSecond;
      if (4 > secondsLeft > 1) {
        player.tell(Text.yellow(`Next wave in ${secondsLeft} seconds...`))
      }
    });

    countdownTasks.push(task);
  }

  const startTask = player.server.scheduleInTicks(countdownSeconds2 * 20, () => {
    const state = activeGauntlets.get(uuidStr)
    if (!state || state.failed) return
    state.waiting = false
    activeGauntlets.set(uuidStr, state)
    startRound(player, nextRound)
  })
  countdownTasks.push(startTask)

  scheduledCountdowns.set(uuidStr, countdownTasks)
}

EntityEvents.death(event => {
  const entity = event.entity
  
  // Check if this entity has any gauntlet round tags
  let isGauntletMob = false
  let round = -1
  
  if (entity.tags && entity.tags.contains) {
    for (let i = 0; i < mobs2.length; i++) {
      if (entity.tags.contains(`gauntlet_round_${i}`)) {
        round = i
        isGauntletMob = true
        break
      }
    }
  }
  
  if (!isGauntletMob) return


  const server = entity.level.server
  const players = server.getPlayerList().getPlayers()

  for (const player of players) {
    const uuidStr = String(player.uuid)
    const state = activeGauntlets.get(uuidStr)
    
    if (state && state.round === round && !state.waiting && !state.failed && !state.completed) {
      
      player.tell(Text.green(`✅ Wave ${round + 1} complete!`))

      if (state.timeoutTask && typeof state.timeoutTask.cancel === "function") {
        state.timeoutTask.cancel()
      }

      const nextRound = round + 1
      
      // FIXED: Removed duplicate completion logic from here
      // Let startRound() handle the completion when nextRound >= mobs2.length
      
      if (nextRound >= mobs2.length) {
        // Just call startRound with the next round, it will handle completion
        startRound(player, nextRound)
      } else {
        startNextRoundCountdown(player, nextRound)
      }
      break
    }
  }
})

PlayerEvents.loggedOut(event => {
  const player = event.player
  const uuidStr = String(player.uuid)

  if (activeGauntlets.has(uuidStr)) {
    const entities = player.level.getAllEntities()
    entities.forEach(entity => {
      if (entity.hasTag && entity.hasTag(`gauntlet_player_${uuidStr}`)) {
        entity.dispose()
      }
    })

    activeGauntlets.delete(uuidStr)
    cancelCountdown(uuidStr)
    console.log(`Cleaned up gauntlet for disconnected player: ${player.name}`)
  }
})

ServerEvents.commandRegistry(event => {
  const { commands: Commands } = event

  event.register(
    Commands.literal('stopgauntlet')
      .requires(src => src.hasPermission(2))
      .executes(ctx => {
        const player = ctx.source.getPlayerOrException()
        const uuidStr = String(player.uuid)

        if (!activeGauntlets.has(uuidStr)) {
          player.tell(Text.red("You are not in a gauntlet!"))
          return 0
        }

        const entities = player.level.getAllEntities()
        entities.forEach(entity => {
          if (entity.hasTag && entity.hasTag(`gauntlet_player_${uuidStr}`)) {
            entity.dispose()
          }
        })

        activeGauntlets.delete(uuidStr)
        cancelCountdown(uuidStr)

        player.tell(Text.yellow("Gauntlet cancelled."))
        return 1
      })
  )
})