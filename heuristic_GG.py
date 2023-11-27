import numpy as np
from utils import *
import math
from typing import Tuple


RAGGIO_DI_VISIONE = 4
ETA_DISTANCE_TARGET = 0.1
ETA_DISTANCE_PLAYER = 0.1


def heuristic_gg(game_map: np.ndarray, move: Tuple[int, int], end_target: Tuple[int, int], hp_player: int):
    if move == end_target:
        return math.inf

    # imposta il target uguale al target finale di default
    target = end_target

    # prende la posizione di tutti i mostri presenti nella mappa
    list_monsters = get_monster_location(game_map)

    # se ci sono mostri nella mappa, individua fra essi il target migliore
    if len(list_monsters) > 0:
        info_monsters = []
        for monster in list_monsters:
            info_monsters.append(
                {
                    "position": monster,
                    "distance": euclidean_distance(move, monster),
                    "path_activated_monsters": path_activated_monsters(game_map, move, monster, list_monsters)
                }
            )

        min = math.inf
        for monster in info_monsters:
            weight = monster["path_activated_monsters"] * ( monster["distance"] * ETA_DISTANCE_TARGET )

            if weight < min:
                min = weight
                target = monster["position"]

    return euclidean_distance(move, target)




def activated_monsters(game_map: np.ndarray, cell: Tuple[int, int], list_monsters: [Tuple[int, int]]):
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
        if euclidean_distance(cell, monster) <= RAGGIO_DI_VISIONE:
            num_monsters += 1

    return num_monsters


def path_activated_monsters(game_map: np.ndarray, cell: Tuple[int, int], target: Tuple[int, int], list_monsters: [Tuple[int, int]], distance: int =1):
    if cell==target:
        return 0
    
    next_cell = get_best_move_euclidean(game_map, cell, target)

    return path_activated_monsters(game_map, next_cell, target, list_monsters, (distance+ETA_DISTANCE_TARGET)) + (activated_monsters(game_map, cell, list_monsters) / distance)




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