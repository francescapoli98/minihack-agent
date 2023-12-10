import numpy as np
from utils import *

# This heuristic gives priority to the weapons first, then to the monsters
# The agent will try to pick up the weapons first, then it will try to kill the monsters
# then, he will try to reach the exit only if there are no weapons and no monsters in the room

# TODO: use different weights configurations for the heuristic based on the agent's hp

# Default mode weights
DEF_WEAPON_WEIGHT = 10
DEF_MONSTER_WEIGHT = 5
DEF_EXIT_WEIGHT = 1

# Danger mode weights
DANGER_WEAPON_WEIGHT = 10 
DANGER_MONSTER_WEIGHT = -10 # with negative weights the agent will try to avoid the monsters
DANGER_EXIT_WEIGHT = 1

def heuristic_fd(game_map: np.ndarray, move: Tuple[int, int], end_target: Tuple[int, int], hp: int):
    """
    Calcola un'euristica personalizzata tenendo conto della sequenza di azioni: raccogliere l'arma, uccidere i mostri e raggiungere l'uscita.

    Args:
    - game_map: Lista di tuple rappresentante la griglia con informazioni su mostri, armi, giocatore e uscita.
    - move: Tupla (x, y) rappresentante le coordinate della prossima mossa.
    - goal: Tupla (x, y) rappresentante le coordinate dell'obiettivo (uscita).

    Returns:
    - int: Valore dell'euristica come intero.
    """

    weapon_location = get_weapon_location(game_map) 
    monster_location = get_monster_location(game_map) 
    inf = 999999999 # infinity
    
    # distance from the exit
    target_distance = manhattan_distance(move, end_target)

    # if the next move is the target but there are monsters alive, the agent cannot exit the room
    if monster_location and move == end_target:
        return inf
    
    if hp<8: #if the agent has less then half hp, danger mode is activated
        weight_dictionary = {
            "weapon": DANGER_WEAPON_WEIGHT,
            "monster": DANGER_MONSTER_WEIGHT,
            "exit": DANGER_EXIT_WEIGHT
        }
        #print("DANGER MODE") # debug
    else: # normal mode if the agent has more than half hp
        weight_dictionary = {
            "weapon": DEF_WEAPON_WEIGHT,
            "monster": DEF_MONSTER_WEIGHT,
            "exit": DEF_EXIT_WEIGHT
        }
        #print("NORMAL MODE") # debug
    
    # distance from the weapon, the agents will try to pick up the nearest weapon
    min_weapon = inf
    if weapon_location: #if there are weapons in the room
        for weapon in weapon_location:  
            if manhattan_distance(move, weapon) < min_weapon:
                min_weapon = manhattan_distance(move, weapon)

    # the agent will try to kill the nearest monster first.
    # this also works in case the agent is in danger and has to run away from the monsters.
    # with negative weights the agent will try to avoid the monsters, so it maximises the distance
    # from the monsters
    min_monster = inf
    if monster_location: #if there are monsters in the room
        for monster in monster_location: #for each monster in the room
            if manhattan_distance(move, monster) < min_monster: 
                min_monster = manhattan_distance(move, monster) 

    # heuristic weighted sum of the distances
    weighted_heuristic = (
        weight_dictionary["weapon"] * min_weapon +
        weight_dictionary["monster"] * min_monster +
        weight_dictionary["exit"] * target_distance 
    )

    return int(weighted_heuristic)