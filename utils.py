import numpy as np
import gym
import math
import IPython.display as display
import time
import matplotlib.pyplot as plt
from matplotlib.image import AxesImage 
from typing import Callable,Tuple, List
from nle import nethack
from minihack import LevelGenerator

MOVEMENT_ACTIONS = tuple(nethack.CompassDirection)
OTHER_ACTIONS = MOVEMENT_ACTIONS + ( 
                nethack.Command.PICKUP,
                nethack.Command.WIELD,
                nethack.Command.FIRE
                )

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

def get_weapon_location(game_map: np.ndarray) -> List[Tuple[int, int]]:
    weapons_symbols = ")"
    coord_weapons = []
    for symbol in weapons_symbols:
        x, y = np.where(game_map == ord(symbol))
        coord_weapons.extend(list(zip(x, y)))
    return coord_weapons

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
                    hp_percent: int,
                    weapon_in_hand: bool
                    ) -> Tuple[int, int]: 
    moves = get_valid_moves(game_map,current_position)
    min = float('inf')
    coord = (0,0)
    for move in moves: #scelgo quella che minimizza l'euristica
        md = heuristic(game_map, move, end_target, hp_percent, weapon_in_hand)
        if md < min:
            min = md
            coord = move
    return coord

def plot_map(game_map: np.ndarray,image: AxesImage) -> np.ndarray:
    display.display(plt.gcf())
    time.sleep(0.7)
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

def pickup():
    env.step(8) # 8 = pickup the item

def wield(): # Tested and working
    obs, _, _, _ = env.step(9) # 9 = wield

    # Example message: What do you want to wield? [- abf or ?*]
    message = bytes(obs['message']).decode('utf-8').rstrip('\x00')
    #print("Message: ", message) # debug
    # split -> ['What do you want to wield? ', '- abf or ?*']
    # we get the second part (index 1), then we get the fourth char of the second part
    # in this case "f" is the dagger (index 4)
    weapon_char = message.split('[')[1][4]
    #print("Weapon char: ", weapon_char) # debug
    env.step(env.actions.index(ord(weapon_char))) # select weapon from inventory
    # New message after wielding:  f- a dagger (weapon in hand). Uncomment to see it.
    #message = bytes(obs['message']).decode('utf-8').rstrip('\x00') #debug
    #print("Message: ", message) # debug

def generate_map():
    map_layout = """
    --------------------
    |..................|
    |..................|
    |..................|
    |..................|
    |..................|
    |..................|
    |..................|
    |..................|
    |..................|
    |..................|
    |..................|
    |..................|
    |..................|
    |..................|
    |..................|
    |..................|
    |..................|
    |..................|
    --------------------
    """

    lvl_gen = LevelGenerator(map = map_layout)
    # starting position
    lvl_gen.set_start_pos((6, 2))

    # dagger position
    lvl_gen.add_object("dagger", ")", (5,8))

    # group of monster low right
    lvl_gen.add_monster("kobold", "k", (21,18))
    lvl_gen.add_monster("kobold", "k", (22,18))

    # group of monster high right
    lvl_gen.add_monster("kobold", "k", (22,1))
    lvl_gen.add_monster("kobold", "k", (22,2))

    # single monster low left
    lvl_gen.add_monster("kobold", "k", (5,18))
    lvl_gen.add_goal_pos((16,12))
    
    return lvl_gen

def generate_env():
    env =  gym.make("MiniHack-Skill-Custom-v0", 
               observation_keys=("chars", "pixel", "blstats", "message"), 
               des_file = map.get_des(),
               actions = OTHER_ACTIONS,
               autopickup = True,   
               ) 
    return env

map = generate_map()
env = generate_env()