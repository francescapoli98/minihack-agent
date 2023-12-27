import numpy as np
from utils import *

#get_monster_location, get_weapon_location, Tuple, manhattan_distance

# This heuristic gives priority to the weapons first, then to the monsters
# The agent will try to pick up the weapons first, then it will try to kill the monsters
# then, he will try to reach the exit only if there are no weapons and no monsters in the room

# TODO: use different weights configurations for the heuristic based on the agent's hp

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
DEFAULT_BRAVE_THRESHOLD = 0.8
WEAPON_BRAVE_THRESHOLD = DEFAULT_BRAVE_THRESHOLD

def heuristic_fd(game_map: np.ndarray, 
                move: Tuple[int, int], 
                end_target: Tuple[int, int], 
                hp_percent: int,
                weapon_in_hand: bool):

    weapon_location = get_weapon_location(game_map) 
    monster_location = get_monster_location(game_map) 
    inf = 999 # infinity

    if move == end_target and len(monster_location)!=0:
        return inf
    
    # distance from the exit
    target_distance = manhattan_distance(move, end_target)
    
    weight_dictionary = {
        "weapon": DEF_WEAPON_WEIGHT,
        "monster": DEF_MONSTER_WEIGHT,
        "exit": DEF_EXIT_WEIGHT
    }

    if not(weapon_in_hand) and hp_percent < (1-DEFAULT_BRAVE_THRESHOLD): #if the agent has not a weapon and has less than 50% hp
        weight_dictionary = {
            "weapon": DANGER_WEAPON_WEIGHT,
            "monster": DANGER_MONSTER_WEIGHT,
            "exit": DANGER_EXIT_WEIGHT
        }
        #print("DANGER MODE") # debug
    elif weapon_in_hand and hp_percent > (1-DEFAULT_BRAVE_THRESHOLD): #if the agent has more than half hp
        weight_dictionary = {
            "weapon": WEAPON_WEAPON_WEIGHT,
            "monster": WEAPON_MONSTER_WEIGHT,
            "exit": WEAPON_EXIT_WEIGHT
        }
        #print("WEAPON MODE") # debug
    elif weapon_in_hand and hp_percent < (1-WEAPON_BRAVE_THRESHOLD): #if the agent has a weapon but has less than 40% hp
        weight_dictionary = {
            "weapon": DANGER_WEAPON_WEIGHT,
            "monster": DANGER_MONSTER_WEIGHT,
            "exit": DANGER_EXIT_WEIGHT
        }
        #print("DANGER WEAPON MODE") # debug
    elif not(weapon_in_hand) and hp_percent > (1-DEFAULT_BRAVE_THRESHOLD): #if the agent has not a weapon but has more than half hp
        weight_dictionary = {
            "weapon": DEF_WEAPON_WEIGHT,
            "monster": DEF_MONSTER_WEIGHT,
            "exit": DEF_EXIT_WEIGHT
        }
        #print("DEFAULT MODE") # debug
    
    # distance from the weapon, the agents will try to pick up the nearest weapon
    min_weapon = 0
    if weapon_location:
        min_weapon = inf
        for weapon in weapon_location:  
            if manhattan_distance(move, weapon) < min_weapon:
                min_weapon = manhattan_distance(move, weapon)

    # the agent will try to kill the nearest monster first.
    # this also works in case the agent is in danger and has to run away from the monsters.
    # with negative weights the agent will try to avoid the monsters, so it maximises the distance
    # from the monsters
    min_monster = 0
    if monster_location: #if there are monsters in the room
        min_monster = inf
        for monster in monster_location: #for each monster in the room
            if manhattan_distance(move, monster) < min_monster: 
                min_monster = manhattan_distance(move, monster) 

    # heuristic weighted sum of the distances
    weighted_heuristic = (
        weight_dictionary["weapon"] * min_weapon +
        weight_dictionary["monster"] * min_monster +
        weight_dictionary["exit"] * target_distance 
    )

    #print("Current position: ", get_player_location(game_map)) # debug
    #print("Move: ", move, "Heuristic score: ", weighted_heuristic) # debug

    return int(weighted_heuristic)