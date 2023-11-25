import numpy as np
import math
import IPython.display as display
import time
import matplotlib.pyplot as plt
from matplotlib.image import AxesImage 
from typing import Callable,Tuple, List

def get_player_location(game_map: np.ndarray, symbol : str = "@") -> Tuple[int, int]:
    x, y = np.where(game_map == ord(symbol))
    return (x[0], y[0])

def get_target_location(game_map: np.ndarray, symbol : str = ">") -> Tuple[int, int]:
    x, y = np.where(game_map == ord(symbol))
    return (x[0], y[0])

def get_monster_location(game_map: np.ndarray) -> List[Tuple[int, int]]:
    symbols_monster = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWQXYZ':;&~_]"
    coord_monsters = []
    for symbol in symbols_monster:
        x, y = np.where(game_map == ord(symbol))
        coord_monsters.extend(list(zip(x, y)))
    return coord_monsters

def is_wall(position_element: int) -> bool:
    obstacles = "|- "
    return chr(position_element) in obstacles

def get_valid_moves(game_map: np.ndarray, current_position: Tuple[int, int]) -> List[Tuple[int, int]]:
    x_limit, y_limit = game_map.shape
    valid = []
    x, y = current_position    
    # North
    if y - 1 > 0 and not is_wall(game_map[x, y-1]):
        valid.append((x, y-1)) 
    # East
    if x + 1 < x_limit and not is_wall(game_map[x+1, y]):
        valid.append((x+1, y)) 
    # South
    if y + 1 < y_limit and not is_wall(game_map[x, y+1]):
        valid.append((x, y+1)) 
    # West
    if x - 1 > 0 and not is_wall(game_map[x-1, y]):
        valid.append((x-1, y))

    if x - 1 > 0 and y - 1 > 0 and not is_wall(game_map[x-1, y-1]):
        valid.append((x-1, y-1))

    if x + 1 > 0 and y + 1 > 0 and not is_wall(game_map[x+1, y+1]):
        valid.append((x+1, y+1))

    if x + 1 > 0 and y - 1 > 0 and not is_wall(game_map[x+1, y-1]):
        valid.append((x+1, y-1))

    if x - 1 > 0 and y + 1 > 0 and not is_wall(game_map[x-1, y+1]):
        valid.append((x-1, y+1))

    return valid

def actions_from_path(start: Tuple[int, int], path: List[Tuple[int, int]]) -> List[int]:
    action_map = {
        "N": 0,
        "E": 1,
        "S": 2,
        "W": 3,
        "NE": 4,
        "SE": 5,
        "SW": 6,
        "NW": 7
    }
    actions = []
    x_s, y_s = start
    for (x, y) in path:
        if x_s == x:
            if y_s > y:
                actions.append(action_map["W"])
            else: actions.append(action_map["E"])
        elif y_s == y:
            if x_s > x:
                actions.append(action_map["N"])
            else: actions.append(action_map["S"])
        elif x_s > x and y_s < y:
            actions.append(action_map["NE"])
        elif x_s < x and y_s < y:
            actions.append(action_map["SE"])
        elif x_s < x and y_s > y:
            actions.append(action_map["SW"])
        elif x_s > x and y_s > y:
            actions.append(action_map["NW"])
        else:
            raise Exception("Error")
        x_s = x
        y_s = y
    
    return actions

def get_best_move(game_map: np.ndarray, 
                  current_position: Tuple[int, int],
                  end_target: Tuple[int, int],
                  heuristic: Callable[[Tuple[int, int], Tuple[int, int]], int],
                 ) -> Tuple[int, int]: 
    moves = get_valid_moves(game_map,current_position)
    min = float('inf')
    coord = (0,0)
    for move in moves: #scelgo quella che minimizza l'euristica
        md = heuristic(move, end_target)      # deve prendere come parametri: (game_map, move, end_target, hp_player)
        if md < min:
            min = md
            coord = move
    return coord

def plot_map(game_map: np.ndarray,image: AxesImage) -> np.ndarray:
    display.display(plt.gcf())
    time.sleep(0.5)
    display.clear_output(wait=True)
    image.set_data(game_map['pixel'][:, 300:975])      
    #fine stampa
    #aggiorno game_map
    return game_map["chars"]

def euclidean_distance(point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def manhattan_distance(point1: Tuple[int, int], point2: Tuple[int, int]) -> int:
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)

    
