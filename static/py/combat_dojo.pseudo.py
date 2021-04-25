#   COMBAT DOJO
#   A turn-based combat game.
#
#
#   ***CLIENT INTERFACE***
#   ***HOME
#   Begin game on home page, with game logo and PLAY button. Player clicks and enters the INFO screen.
#
#   ***INFO
#   Present player with rules of the game and gameplay mechanics.
#   QUIT button to return to HOME screen.
#
#   ***SELECT
#   Load table with 8 tiles, one for each fighter.
#   Each tile displays fighter image and attributes.
#   Effects on tile for HOVER and CLICK.
#   "?" tile for CPU to choose player's fighter.
#   Player chooses CPU fighter or selects random option.
#   UNDO button reverts player or CPU fighter selection.
#   BACK button to return to INFO screen.
#   QUIT button to return to HOME screen.
#   FIGHT button to enter FIGHT screen.
#
#   ***FIGHT
#   Tile for each fighter, revered left or right depending on position.
#   HEALTH BAR to indicate remaining fighter health.
#   First to attack generated randomly.
#   Player selects one of three move types, whether they are on attack or defense.
#   GO button to launch turn.
#   Results of battle round shown in FIGHT LOG between fighters.
#   QUIT button to return to HOME screen
#   When one fighter runs out of health, player taken to RESULT screen.
#
#   ***RESULT
#   Tile with image of winning fighter under a "Winner" banner.
#   PLAY AGAIN button to return to SELECT screen.
#   QUIT button to return to HOME screen.
#
#
#   ***LOGIC***
#   ***ATTRIBUTE-DRIVEN COMBAT
#   Each fighter is rated across six metrics on a scale of 1-20 to obtain their FIGHTING PROFILE.
#       PWR: Power - the strength of an attack, a factor in total damage inflicted if the attack succeeds.
#       SPD: Speed - the speed of an attack or defense, a factor in the success of each.
#       AGL: Agility - the fighter's agility, a factor in how well the fighter can avoid attacks.
#       ATT: Attack - the overall quality of a fighter's attack, like accuracy. Largest factor in the success of attacks.
#       DEF: Defense - the overall quality of a fighter's defense. Largest factor in the success of defenses.
#       RCV: Recovery - the rate at which a fighter recovers health during a fight if an attack is defended successfully.
#   Each turn pits one fighter's MODIFIED ATTACK VALUE versus the opponent's MODIFIED DEFENSE VALUE. A RANDOM GENERATOR is used to determine a winner.
#       (Example - For the next turn, Attacker has a modified value of 25, Defender has a modified value of 17. This gives the attacker a 60.1% chance [(ATT + DEF) / ATT] to win the round.)
#   If an attack is successful, the damage is calculated by factoring the modified attack value against the BASE DAMAGE VALUE.
#   If a defense is successful, the recovery is calculated factoring the modified defense value against the BASE RECOVERY VALUE
#   If an attack MISSES, it's considered a neutral event and no damage or recovery occurs.
#       The chance of an attack missing is calculated by factoring the attack type against the BASE MISS VALUE.
#   Each fighter starts with a health rating of 100. The fight is over after one fighter drops below 0, or whoever has the highest health level after 40 rounds.
#
#   ***FIGHT TECHNIQUES AND MODIFIERS
#   Fighters have one of three options to choose from for their attack or defense:
#       - Attacks can be QUICK, NORMAL or STRONG.
#       - Defenses can be DODGE, BLOCK or COUNTER.
#   These techniques modify the fighter's base fighting profile in order to create a MODIFIED VALUE for the round. (ALL INTEGER VALUES ARE CEILING ROUNDED)
#       Attacks:
#           Quick -  5% of PWR + 45% of  SPD + 50% of ATT = MODIFIED ATTACK VALUE.
#           Normal -  20% of PWR + 20% of  SPD + 60% of ATT = MODIFIED ATTACK VALUE.
#           Strong -  45% of PWR + 15% of  SPD + 40% of ATT = MODIFIED ATTACK VALUE.
#       Attack techniques also modify the fighter's base levels of miss probability and damage:
#           Quick -  Inflicts 20% of  that fighter's BASE DAMAGE VALUE. It also reduces the BASE MISS VALUE by 50%.
#           Normal -  Inflicts 100% of  that fighter's BASE DAMAGE VALUE and has no effect on the BASE MISS VALUE.
#           Strong -  Inflicts 200% of  that fighter's BASE DAMAGE VALUE. It also increases the BASE MISS VALUE by 100%
#       Defenses:
#           Dodge -  15% of SPD + 45% of  AGL + 40% of DEF = MODIFIED DEFENSE VALUE
#           Normal -  35% of SPD + 5% of  AGL + 60% of DEF = MODIFIED DEFENSE VALUE
#           Counter -  30% of SPD + 20% of  AGL + 50% of DEF = MODIFIED DEFENSE VALUE
#       Defense techniques also modify the fighter's base levels of recovery:
#           Dodge - Grants 60% of the fighter's BASE RECOVERY VALUE after a successful defense.
#           Block - Grants 100% of the fighter's BASE RECOVERY VALUE after a successful defense.
#           Counter - Grants 20% of the fighter's BASE RECOVERY VALUE after a successful defense, and also inflicts a PARRY DAMAGE to the opponent.
#
#   ***BASE VALUES
#   Base Recovery Value:
#       Set to a default of 5. Each fighter's unique value is calculated by factoring the default base by the fighter's RCV rating / 20 (the MAX rating value).
#           (Example: A fighter successfully defends with a DODGE. Their RCV rating is 10. For the round, the fighter will recover 60% of their base value of 50% of 5, which equates to a recovery of 2 Health.
#   Base Miss Value:
#       Set to a default of 30%. Attack techniques determine the modified value for the round.
#           (Example: A fighter uses a STRONG attack. The chances of the attack failing are 200% of the base miss value of 30%, which equates to a miss probability of 60%).
#   Base Damage Value:
#       Set to a default of 10. Each fighter's unique value is calculated by factoring the default base by the fighter's PWR rating / 20 (the MAX rating value).
#           (Example: A fighter successfully attacks with a NORMAL attack. Their PWR rating is 12. For the round, the fighter will inflict a damage value of 100% of their base value of 60% of 10, which equates to a damage value of 6).
#   Parry Damage Value:
#       If a fighter successfully counters an attack, they will inflict a damage value of 50% of their own base damage value based on the attack technique used by the attacker.
#           (Example: A fighter uses a STRONG attack. The defender counters successfully and has a PWR rating of 10. The defender will inflict a damage value of 50% of  200% of their base damage value of 5, which equates to a damage value of 5).
#
#
#   ***MODELS, FUNCTIONS AND ALGOS***
#   ***GAME SESSION
#   FIGHT button POST from SELECT screen flips session GAME LOOP to True
#   Fighter type selected by player = Fighter1
#   Fighter type selected for CPU = Fighter2
#   Create HEALTH Session for Fighter1 and Figher2  = 100
#   Create round counter session = 0
#   ***FIGHT START
#   While Game Loop is True
#   Fighter1 ATT * .35 + SPD * .35 + AGL * .30 = First Attack Value.
#   Fighter2 ATT * .35 + SPD * .35 + AGL * .30 = First Attack Value.
#       Random number between Fighter1 + Fighter2 values.
#           (Example: Fighter1 value = 31. Fighter2 value = 24. Random number generated between 1 and 55. Fighter1 is 1-31, Fighter2 is 26-55. Winning number goes on attack first.)
#   (Lets say Fighter1 won) First Attacker - Fighter1
#   ***FIGHT TURN
#   While round counter < 41
#       round counter ++
#           if counter session value is  odd - First Attacker
#               Else Other Fighter
#       Fighter1.attack = NORMAL (from POST)
#       Fighter2.defense = DODGE (from POST)
#           ***MISS CHECK
#       miss prob = (miss base * fighter1 attack) * 100
#       random number = 1-100
#           If random number not miss prob (miss prob is first x numbers from 1-100)
#               return "attack missed"
#           Else:
#               mod attack value = fighter1.attack.base * 100
#               mod defense value = fighter2.type.base * 100
#               random number = between 1 and mod attack value + mod defense value
#               round winner = random number from 1 to mod attack + mod defense (attack is 1 through its value)
#               if attacker wins
#                   damage value = attack.type * fighter.base damage
#                   session health defender - damage value
#                   return "attack success, damage value"
#               elif Fighter2.defense = COUNTER
#                   recovery value = fighter2 defense type * fighter recovery base
#                   damage value = fighter2.fighter1 attack.type * fighter2 base damage *.5
#                    session health defender + recoveryvalue
#                    session health attacker - damage value
#                   return "counter successful, recovery value and damage value"
#               else
#                   recovery value = fighter2 defense type * fighter recovery base
#                    session health defender + recovery value
#                   return "attack defended, recovery value"
#       If Fighter1.health <= 0
#           flip session game loop to False
#           return "Fighter 2 wins"
#           return redirect to RESULTS screen
#           Elif Fighter2.health <=0
#               flip session game loop to False
#               return "Fighter 1 wins"
#               return redirect to RESULTS screen
#           Else
#               return redirect to FIGHT screen
#   If Fighter1.health > Fighter2.health
#       flip session game loop to False
#       return "fighter1 wins"
#       return redirect to RESULTS screen
#       Elif figher2.health > fighter1.health
#           flip session game loop to False
#           return "fighter2 wins"
#           return redirect to RESULTS screen
#       Else
#           return "Fight ends in a draw"
#           flip session game loop to False
#           return redirect to RESULTS screen
