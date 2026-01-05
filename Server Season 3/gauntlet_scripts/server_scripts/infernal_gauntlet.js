const infernal_mobs = [
  { id: 'terra_entity:hell_bat', tag: 'gauntlet_1' },
  { id: 'undead_unleashed:flamebreather', tag: 'gauntlet_2' },
  { id: 'terramity:hellrok', tag: 'gauntlet_3' },
  { id: 'luminous_beasts:the_furnace', tag: 'gauntlet_4' },
  { id: 'threateningly_mobs:terra_dragon', tag: 'gauntlet_5' }
]

const infernal_countdownSeconds = 10
const infernal_seconds = 60
const infernal_timeLimitTicks2 = 20 * infernal_seconds

let infernal_activeGauntlets = new Map() // uuid string → { round, entityId, timeoutTask, waiting, failed }
let infernal_scheduledCountdowns = new Map() // uuid string → [scheduledTask]
let infernal_gauntletSpawnPositions = new Map(); // uuid string → {x, y, z}\
let infernal_gauntletParticleTasks = new Map(); // uuid string → repeating task


ServerEvents.commandRegistry(event => {
  const { commands: Commands } = event

  event.register(
    Commands.literal('start_infernal_gauntlet')
      .requires(src => true)
      .executes(ctx => {
        const player = ctx.source.getPlayerOrException();
        const uuidStr = String(player.uuid);

        if (infernal_activeGauntlets.has(uuidStr)) {
          player.tell(Text.red("❌ You are already in a gauntlet!"));
          return 0;
        }

        const pos = player.blockPosition(); // Capture position once at command start

        infernal_activeGauntlets.set(uuidStr, {
          round: 0,
          entity: null,
          timeoutTask: null,
          waiting: false,
          failed: false,
          completed: false,
          spawnPos: pos // Store player's starting position here
        });

        infernal_startPreSpawnCountdown(player, 0);

        return 1;
      })
  );
})

function infernal_startPreSpawnCountdown(player, round) {
  const infernal_preSpawnCountdownSeconds = 10;
  // Get server command source for elevated permissions
  const server = player.server;
  const serverSource = server.createCommandSourceStack();
  
  serverSource.runCommandSilent(`title ${player.name.string} title {"text":"Infernal Gauntlet","color":"red"}`)
  serverSource.runCommandSilent(`title ${player.name.string} subtitle {"text":"Starting in ${infernal_preSpawnCountdownSeconds} seconds","color":"yellow"}`)
  const uuidStr = String(player.uuid);

  for (let i = 1; i <= infernal_preSpawnCountdownSeconds; i++) {
    let infernal_currentSecond = i;
    server.scheduleInTicks(infernal_currentSecond * 20, () => {
      let infernal_secondsLeft = infernal_preSpawnCountdownSeconds - infernal_currentSecond;
      if (infernal_secondsLeft > 0) {
        if (4 > infernal_secondsLeft > 0)
        {
          player.tell(Text.yellow(`${infernal_secondsLeft}`));
        }
      } else {
        infernal_startRound(player, round); // Start the first wave after countdown
      }
    });
  }
}

function infernal_startRound(player, round) {
  const uuidStr = String(player.uuid)

  const infernal_state = infernal_activeGauntlets.get(uuidStr)
  if (!infernal_state) {
    return // Safety check
  }

  const pos = infernal_state.spawnPos // Use stored spawn position
  const server = player.server;
  const serverSource = server.createCommandSourceStack();
  
  if (round >= infernal_mobs.length) {
    
    // Check if already completed to prevent double execution
    if (infernal_state.completed) {
      return
    }
    
    // Mark as completed immediately to prevent double execution
    infernal_state.completed = true
    infernal_activeGauntlets.set(uuidStr, infernal_state)
    
    
    // Use serverSource for titles and sounds
    try {
      serverSource.runCommandSilent(`title ${player.name.string} title {"text":"VICTORY!","color":"gold","bold":true}`)
      serverSource.runCommandSilent(`title ${player.name.string} subtitle {"text":"Gauntlet Complete!","color":"green"}`)
    } catch (e) {
    }
    
    try {
      serverSource.runCommandSilent(`playsound minecraft:entity.player.levelup master @a ${pos.x} ${pos.y} ${pos.z} 1 1`)
    } catch (e) {
      // Try alternative playsound syntax
      try {
        serverSource.runCommandSilent(`playsound minecraft:entity.player.levelup master ${player.name.string}`)
      } catch (e2) {
      }
    }
    
    // === Complete the FTB Quest ===
    let infernal_teamData = player.ftbTeamData;
    let infernal_questId = "0B18C2894DABCB9B";

    try {
      serverSource.runCommandSilent(`ftbquests change_progress ${player.name.string} complete ${infernal_questId}`);
      player.tell(Text.green("✅ Quest marked complete!"));
    } catch (e) {
      console.log(`[Gauntlet] ❌ Failed to run quest completion command: ${e}`);
    }

    
    // Add a small delay before cleanup
    server.scheduleInTicks(1, () => {
      infernal_activeGauntlets.delete(uuidStr)
    })
    return
  }

  const infernal_mobData = infernal_mobs[round]
  const infernal_level = player.level

  // Use serverSource for commands that need elevated permissions
  serverSource.runCommandSilent(`champions summonpos ${pos.x} ${pos.y} ${pos.z} ${infernal_mobData.id} 5`)
  serverSource.runCommandSilent(`playsound terramity:ultra_sniffer_teleport master @a ${pos.x} ${pos.y} ${pos.z} 1 1`)

  // Wait a tick or two to let the mob spawn
  server.scheduleInTicks(2, () => {
    const infernal_allEntities = infernal_level.getAllEntities()
    let infernal_championEntity = null

    for (const infernal_ent of infernal_allEntities) {
      if (!infernal_ent.tags) continue
      if (infernal_ent.tags.contains(infernal_mobData.tag)) continue
      if (infernal_ent.type !== infernal_mobData.id) continue

      // Use let instead of var here
      let infernal_dx = infernal_ent.x - pos.x
      let infernal_dy = infernal_ent.y - pos.y
      let infernal_dz = infernal_ent.z - pos.z
      let infernal_distance = Math.sqrt(infernal_dx * infernal_dx + infernal_dy * infernal_dy + infernal_dz * infernal_dz)
      if (infernal_distance > 5) continue

      let infernal_nbt = infernal_ent.getNbt()
      if (!infernal_nbt) continue
      let infernal_forgeSpawnType = infernal_nbt.getString('forge:spawn_type')
      if (infernal_forgeSpawnType !== 'COMMAND') continue

      infernal_championEntity = infernal_ent
      break
    }

    if (!infernal_championEntity) {
      player.tell(Text.red("❌ Failed to spawn champion mob for this wave!"))
      infernal_activeGauntlets.delete(uuidStr)
      return
    }
    
    // Use serverSource for effect command
    serverSource.runCommandSilent(`effect give ${infernal_championEntity.uuid} terramity:immunity 30 1 true`)

    infernal_championEntity.addTag(infernal_mobData.tag)
    infernal_championEntity.glowing = true
    infernal_championEntity.addTag("persistent")
    infernal_championEntity.addTag(`gauntlet_player_${uuidStr}`)
    infernal_championEntity.addTag(`gauntlet_round_${round}`)
    infernal_championEntity.customName = Text.red(`Wave ${round + 1}`)
    infernal_championEntity.customNameVisible = true

    player.tell(Text.gold(`Wave ${round + 1} has begun!!`))
    player.tell(Text.gray(`⏱ You have ${infernal_timeLimitTicks2 / 20} seconds.`))

    const infernal_timeoutTask = server.scheduleInTicks(infernal_timeLimitTicks2, () => {
      const infernal_state = infernal_activeGauntlets.get(uuidStr)
      if (!infernal_state || infernal_state.round !== round || infernal_state.waiting) return

      const infernal_allEntities = player.level.getAllEntities()
      let infernal_found = false

      // Use serverSource for title and sound commands
      serverSource.runCommandSilent(`title ${player.name.string} title {"text":"❌ YOU FAILED!","color":"red","bold":true}`)
      serverSource.runCommandSilent(`playsound terramity:fail master @a ${pos.x} ${pos.y} ${pos.z} 1 1`)
      infernal_activeGauntlets.delete(uuidStr)
      infernal_cancelCountdown(uuidStr)
      
      for (const infernal_ent of infernal_allEntities) {
        if (
          infernal_ent.tags &&
          infernal_ent.tags.contains(`gauntlet_round_${round}`) &&
          infernal_ent.tags.contains(`gauntlet_player_${uuidStr}`) &&
          !infernal_ent.isRemoved()
        ) {
          infernal_ent.discard()
          infernal_found = true
          break
        }
      }

      if (!infernal_found) {
      }
    })

    infernal_activeGauntlets.set(uuidStr, {
      round: round,
      entity: infernal_championEntity,
      timeoutTask: infernal_timeoutTask,
      waiting: false,
      failed: false,
      completed: false,
      spawnPos: pos
    })

    // Notify player when 5 seconds are left
    const infernal_warningTask = server.scheduleInTicks((infernal_timeLimitTicks2 - 100), () => {
      const infernal_state = infernal_activeGauntlets.get(uuidStr)
      if (!infernal_state || infernal_state.round !== round || infernal_state.failed || infernal_state.waiting) return

      player.tell(Text.red("5 seconds remaining!"))
      // Use serverSource for playsound
      serverSource.runCommandSilent(`playsound minecraft:block.note_block.pling master ${player.name.string} ~ ~ ~ 1 2`)
    })

  })
}

function infernal_cancelCountdown(uuidStr) {
  if (infernal_scheduledCountdowns.has(uuidStr)) {
    var infernal_tasks = infernal_scheduledCountdowns.get(uuidStr)
    if (Array.isArray(infernal_tasks)) {
      infernal_tasks.forEach(infernal_task => {
        if (infernal_task && typeof infernal_task.cancel === "function") {
          try {
            infernal_task.cancel()
          } catch (e) {
            // Ignore cancellation errors
          }
        }
      })
    }
    infernal_scheduledCountdowns.delete(uuidStr)
  }
}

function infernal_startNextRoundCountdown(player, nextRound) {
  const uuidStr = String(player.uuid)
  infernal_cancelCountdown(uuidStr)

  const infernal_currentState = infernal_activeGauntlets.get(uuidStr)
  if (infernal_currentState) {
    infernal_currentState.waiting = true
    infernal_currentState.failed = false
    if (infernal_currentState.timeoutTask && typeof infernal_currentState.timeoutTask.cancel === "function") {
      infernal_currentState.timeoutTask.cancel()
    }
    infernal_activeGauntlets.set(uuidStr, infernal_currentState)
  }

  player.tell(Text.yellow(`Next wave in ${infernal_countdownSeconds} seconds...`))

  const infernal_countdownTasks = []
  const server = player.server;
  
  for (let i = 1; i <= infernal_countdownSeconds; i++) {
    let infernal_currentSecond = i; // Capture current loop index
    var infernal_task = server.scheduleInTicks(infernal_currentSecond * 20, () => {
      const infernal_state = infernal_activeGauntlets.get(uuidStr);
      if (!infernal_state || infernal_state.failed) return;

      const infernal_secondsLeft = infernal_countdownSeconds - infernal_currentSecond;
      if (4 > infernal_secondsLeft > 1) {
        player.tell(Text.yellow(`Next wave in ${infernal_secondsLeft} seconds...`))
      }
    });

    infernal_countdownTasks.push(infernal_task);
  }

  const infernal_startTask = server.scheduleInTicks(infernal_countdownSeconds * 20, () => {
    const infernal_state = infernal_activeGauntlets.get(uuidStr)
    if (!infernal_state || infernal_state.failed) return
    infernal_state.waiting = false
    infernal_activeGauntlets.set(uuidStr, infernal_state)
    infernal_startRound(player, nextRound)
  })
  infernal_countdownTasks.push(infernal_startTask)

  infernal_scheduledCountdowns.set(uuidStr, infernal_countdownTasks)
}

EntityEvents.death(event => {
  const infernal_entity = event.entity
  
  // Check if this entity has any gauntlet round tags
  let infernal_isGauntletMob = false
  let infernal_round = -1
  
  if (infernal_entity.tags && infernal_entity.tags.contains) {
    for (let i = 0; i < infernal_mobs.length; i++) {
      if (infernal_entity.tags.contains(`gauntlet_round_${i}`)) {
        infernal_round = i
        infernal_isGauntletMob = true
        break
      }
    }
  }
  
  if (!infernal_isGauntletMob) return


  const infernal_server = infernal_entity.level.server
  const infernal_players = infernal_server.getPlayerList().getPlayers()

  for (const infernal_player of infernal_players) {
    const uuidStr = String(infernal_player.uuid)
    const infernal_state = infernal_activeGauntlets.get(uuidStr)
    
    if (infernal_state && infernal_state.round === infernal_round && !infernal_state.waiting && !infernal_state.failed && !infernal_state.completed) {
      
      infernal_player.tell(Text.green(`✅ Wave ${infernal_round + 1} complete!`))

      if (infernal_state.timeoutTask && typeof infernal_state.timeoutTask.cancel === "function") {
        infernal_state.timeoutTask.cancel()
      }

      const infernal_nextRound = infernal_round + 1
      
      // FIXED: Removed duplicate completion logic from here
      // Let startRound() handle the completion when nextRound >= mobs.length
      
      if (infernal_nextRound >= infernal_mobs.length) {
        // Just call startRound with the next round, it will handle completion
        infernal_startRound(infernal_player, infernal_nextRound)
      } else {
        infernal_startNextRoundCountdown(infernal_player, infernal_nextRound)
      }
      break
    }
  }
})

PlayerEvents.loggedOut(event => {
  const infernal_player = event.player
  const uuidStr = String(infernal_player.uuid)

  if (infernal_activeGauntlets.has(uuidStr)) {
    const infernal_entities = infernal_player.level.getAllEntities()
    infernal_entities.forEach(infernal_entity => {
      if (infernal_entity.hasTag && infernal_entity.hasTag(`gauntlet_player_${uuidStr}`)) {
        infernal_entity.kill()
      }
    })

    infernal_activeGauntlets.delete(uuidStr)
    infernal_cancelCountdown(uuidStr)
    console.log(`Cleaned up gauntlet for disconnected player: ${infernal_player.name}`)
  }
})

ServerEvents.commandRegistry(event => {
  const { commands: Commands } = event

  event.register(
    Commands.literal('stopgauntlet')
      .requires(src => src.hasPermission(2))
      .executes(ctx => {
        const infernal_player = ctx.source.getPlayerOrException()
        const uuidStr = String(infernal_player.uuid)

        if (!infernal_activeGauntlets.has(uuidStr)) {
          infernal_player.tell(Text.red("You are not in a gauntlet!"))
          return 0
        }

        const infernal_entities = infernal_player.level.getAllEntities()
        infernal_entities.forEach(infernal_entity => {
          if (infernal_entity.hasTag && infernal_entity.hasTag(`gauntlet_player_${uuidStr}`)) {
            infernal_entity.kill()
          }
        })

        infernal_activeGauntlets.delete(uuidStr)
        infernal_cancelCountdown(uuidStr)

        infernal_player.tell(Text.yellow("Gauntlet cancelled."))
        return 1
      })
  )
})