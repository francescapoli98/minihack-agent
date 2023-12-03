import numpy as np
from utils import *

# This heuristic gives priority to the weapons first, then to the monsters
# The agent will try to pick up the weapons first, then it will try to kill the monsters
# The agent will try to reach the exit only if there are no weapons and no monsters in the room
def old_heuristic(game_map: np.ndarray, current_position: Tuple[int, int], end_target: Tuple[int, int], hp_player: int):
    
    coord_weapons = get_weapon_location(game_map) #get the coordinates of the weapons
    coord_monsters = get_monster_location(game_map) #get the coordinates of the monsters

    target = end_target #target is the exit by default

    if len(coord_weapons)!= 0 and current_position == coord_weapons[0]:
        pickup() #pick up the weapon
        #weapons_in_inventory += 1 #increase the number of weapons in inventory
        #wield() #NOT WORKING
        #weapons_in_hand += 1
        #coord = get_best_move(game_map, current_position, target, euclidean_distance)

    if len(coord_weapons)!=0: #if the agent has no weapons and there are weapons in the room
        target = coord_weapons[0] #the target is the weapon
    elif len(coord_monsters)!=0: #if there are monsters in the room and i have a weapon
        target = coord_monsters[0] #the target is the monster

    score = euclidean_distance(current_position, target) #score is the euclidean distance between the current position and the target
    return score

def heuristic_fd(game_map, move, end_target, hp):
    """
    Calcola un'euristica personalizzata tenendo conto della sequenza di azioni: raccogliere l'arma, uccidere i mostri e raggiungere l'uscita.

    Args:
    - game_map: Lista di tuple rappresentante la griglia con informazioni su mostri, armi, giocatore e uscita.
    - move: Tupla (x, y) rappresentante le coordinate della prossima mossa.
    - goal: Tupla (x, y) rappresentante le coordinate dell'obiettivo (uscita).

    Returns:
    - int: Valore dell'euristica come intero.
    """
    # get the coordinates of the weapons and the monsters
    weapon_location = get_weapon_location(game_map) 
    monster_location = get_monster_location(game_map) 

    # weights: the higher the weight, the higher the priority, we can tune them as we want
    weapon_weight = 10
    monster_weight = 5
    exit_weight = 1

    inf = 999999999 # infinity

    # distance from the exit
    target_distance = manhattan_distance(move, end_target)

    # distance from the weapon, the agents will try to pick up the nearest weapon
    # weapon_distance = manhattan_distance(move, weapon_location[0]) if weapon_location else inf
    min_weapon = 0
    if weapon_location: #if there are weapons in the room
        for weapon in weapon_location:  
            if manhattan_distance(move, weapon) < min_weapon:
                min_weapon = manhattan_distance(move, weapon)
                weapon_distance = min_weapon
            else:
                weapon_distance = manhattan_distance(move, weapon)
    else: #if there are no weapons in the room
        weapon_distance = inf

    # distance from the monster, the agents will try to kill the nearest monster first
    min_monster = 0
    if monster_location: #if there are monsters in the room
        for monster in monster_location: #for each monster in the room
            if manhattan_distance(move, monster) < min_monster: 
                min_monster = manhattan_distance(move, monster) 
                monster_distance = min_monster
            else:
                monster_distance = manhattan_distance(move, monster)
    else: #if there are no monsters in the room
        monster_distance = inf

    # heuristic weighted sum of the distances
    weighted_heuristic = (
        weapon_weight * weapon_distance +
        monster_weight * monster_distance +
        exit_weight * target_distance 
    )

    # we can scale the heuristic as we want
    #scaled_heuristic = int(weighted_heuristic * 0.1)  # 0.1 is the scale factor

    return int(weighted_heuristic) 