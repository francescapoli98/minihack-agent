import numpy as np
from utils import *
from heuristic_GG import BRAVE_PLAYER

# This is the greedy heuristic function, it gives a score to each possible move by performing a weighted sum of the distances.
# These are the weights used in the heuristic function, the higher the weight the more important is the factor.

# Default mode weights
DEF_WEAPON_WEIGHT = 10
DEF_MONSTER_WEIGHT = 5
DEF_EXIT_WEIGHT = 1

#Weapon mode weights
WEAPON_WEAPON_WEIGHT = 0
WEAPON_MONSTER_WEIGHT = 10
WEAPON_EXIT_WEIGHT = 1

# Danger mode weights
DANGER_WEAPON_WEIGHT = 0 
DANGER_MONSTER_WEIGHT = -10 # with negative weights the agent will try to avoid the monsters
DANGER_EXIT_WEIGHT = 1

# Brave thresholds
# we import the brave threshold from the tactical heuristic to have the same behaviour
DEFAULT_BRAVE_THRESHOLD = BRAVE_PLAYER
WEAPON_BRAVE_THRESHOLD = DEFAULT_BRAVE_THRESHOLD + 0.1 # the agent will be more brave when it has a weapon in hand

def heuristic_fd(game_map: np.ndarray, 
                move: Tuple[int, int], 
                end_target: Tuple[int, int], 
                hp_percent: int,
                weapon_in_hand: bool):

    # first, we retrieve the locations of the monsters, the weapon and the exit
    weapon_location = get_weapon_location(game_map) 
    monster_location = get_monster_location(game_map) 
    inf = 999 # infinity

    # if the agent is near the exit and there are still monsters in the room, it will try to kill them first
    if move == end_target and len(monster_location)!=0:
        return inf
    
    # distance from the exit
    target_distance = manhattan_distance(move, end_target)
    
    # initially we set the weights to the default values
    weight_dictionary = {
        "weapon": DEF_WEAPON_WEIGHT,
        "monster": DEF_MONSTER_WEIGHT,
        "exit": DEF_EXIT_WEIGHT
    }

    # We can use different weights depending on the agent's status, the brave threshold plays a big role in the heuristic function

    # DANGER MODE: the agent will try to avoid the monsters in order to recover hp
    if not(weapon_in_hand) and hp_percent < (1-DEFAULT_BRAVE_THRESHOLD): 
        weight_dictionary = {
            "weapon": DANGER_WEAPON_WEIGHT,
            "monster": DANGER_MONSTER_WEIGHT,
            "exit": DANGER_EXIT_WEIGHT
        }
        #print("DANGER MODE") # debug

    # WEAPON MODE: the agent will try to kill the monsters with the weapon in his hand
    elif weapon_in_hand and hp_percent > (1-DEFAULT_BRAVE_THRESHOLD): 
        weight_dictionary = {
            "weapon": WEAPON_WEAPON_WEIGHT,
            "monster": WEAPON_MONSTER_WEIGHT,
            "exit": WEAPON_EXIT_WEIGHT
        }
        #print("WEAPON MODE") # debug
    
    # DANGER WEAPON MODE: the agent will try to avoid the monsters in order to recover hp, but with a weapon in hand it will be more brave
    elif weapon_in_hand and hp_percent < (1-WEAPON_BRAVE_THRESHOLD): 
        weight_dictionary = {
            "weapon": DANGER_WEAPON_WEIGHT,
            "monster": DANGER_MONSTER_WEIGHT,
            "exit": DANGER_EXIT_WEIGHT
        }
        #print("DANGER WEAPON MODE") # debug

    # if the agent has not a weapon but has more than 1-brave_threshold hp, it will try to pick up the nearest weapon
    elif not(weapon_in_hand) and hp_percent > (1-DEFAULT_BRAVE_THRESHOLD): 
        weight_dictionary = {
            "weapon": DEF_WEAPON_WEIGHT,
            "monster": DEF_MONSTER_WEIGHT,
            "exit": DEF_EXIT_WEIGHT
        }
        #print("DEFAULT MODE") # debug
    
    # This is where the greedy approach comes into play. Note that this doesn't depend on the order in which these 
    # two blocks are written, since it depends on the weights and not on the order of the if statements.
    
    # we retrieve the distance from the nearest weapon 
    min_weapon = 0
    if weapon_location:
        min_weapon = inf
        for weapon in weapon_location:  
            if manhattan_distance(move, weapon) < min_weapon:
                min_weapon = manhattan_distance(move, weapon)

    # we retrieve the distance from the nearest monster
    # this also works in case the agent is in danger and has to run away from the monsters.
    # with negative weights the agent will try to avoid the monsters, so it maximises the distance
    # from the monsters in that case.
    min_monster = 0
    if monster_location: 
        min_monster = inf
        for monster in monster_location:
            if manhattan_distance(move, monster) < min_monster: 
                min_monster = manhattan_distance(move, monster) 

    # heuristic weighted sum of the distances, here we can see the weights in action
    weighted_heuristic = (
        weight_dictionary["weapon"] * min_weapon +
        weight_dictionary["monster"] * min_monster +
        weight_dictionary["exit"] * target_distance 
    )

    #print("Current position: ", get_player_location(game_map)) # debug
    #print("Move: ", move, "Heuristic score: ", weighted_heuristic) # debug

    return int(weighted_heuristic)