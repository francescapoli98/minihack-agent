import numpy as np
from utils import *

# This heuristic gives priority to the weapons first, then to the monsters
# The agent will try to pick up the weapons first, then it will try to kill the monsters
# The agent will try to reach the exit only if there are no weapons and no monsters in the room
def heuristic_fd(game_map: np.ndarray, current_position: Tuple[int, int], end_target: Tuple[int, int], hp_player: int):
    
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

'''
def get_best_move_euclidean(game_map: np.ndarray, 
                  current_position: Tuple[int, int],
                  end_target: Tuple[int, int]
                 ) -> Tuple[int, int]: 
    moves = get_valid_moves(game_map,current_position)
    min = float('inf')
    coord = (0,0)
    for move in moves:
        md = euclidean_distance(move, end_target)
        if md < min:
            min = md
            coord = move
    return coord
'''
