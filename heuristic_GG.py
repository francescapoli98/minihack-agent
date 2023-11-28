import numpy as np
from utils import *
import math
from typing import Tuple

NEAR_MONSTERS_RANGE = 2
ETA_DISTANCE_TARGET = 0.5


def heuristic_gg(game_map: np.ndarray, move: Tuple[int, int], end_target: Tuple[int, int], hp_player: int):

    # imposta il target uguale al target finale di default
    target = end_target

    # prende la posizione di tutti i mostri presenti nella mappa
    list_monsters = get_monster_location(game_map)

    if move == end_target and len(list_monsters)!=0:
        return math.inf
    
    # se ci sono mostri nella mappa, individua fra essi il target migliore
    if len(list_monsters) > 0:
        info_monsters = []
        for monster in list_monsters:
            info_monsters.append(
                {
                    "position": monster,
                    "distance": euclidean_distance(move, monster),
                    "near_monsters": near_monsters(game_map,monster,list_monsters)
                }
            )

        min = math.inf
        for monster in info_monsters:
            weight = monster["near_monsters"] * ( monster["distance"] * ETA_DISTANCE_TARGET )

            if weight < min:
                min = weight
                target = monster["position"]

    return score(game_map,move,target,list_monsters)



def score(game_map: np.ndarray,player_position:Tuple[int, int],target:Tuple[int, int],list_monsters:[Tuple[int, int]]):
    if len(list_monsters)==0:
        return euclidean_distance(player_position,target)
    
    sum=1
    for monster in list_monsters:
        if monster!=target:
            sum+=euclidean_distance(player_position,monster)
    return euclidean_distance(player_position,target)-(-sum/len(list_monsters)-1)
        



def near_monsters(game_map: np.ndarray, cell: Tuple[int, int], list_monsters: [Tuple[int, int]]):
    """
    Counts the number of monsters within the given range of vision.

    Parameters:
    game_map (np.ndarray): The game map.
    cell (Tuple[int, int]): The current cell coordinates.
    list_monsters ([Tuple[int, int]]): List of monster coordinates.

    Returns:
    int: The number of monsters within the range of vision.
    """
    num_monsters = 0

    for monster in list_monsters:
        if euclidean_distance(cell, monster) <= NEAR_MONSTERS_RANGE:
            num_monsters += 1

    return num_monsters






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