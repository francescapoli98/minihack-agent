import gym
import minihack
import numpy as np
import matplotlib.pyplot as plt
import IPython.display as display
import time
from utils import *

#use a weapon: w
#pick up an object: ,

# 1. controls if there are weapons in the room and picks them before fighting, then kills the monsters and exits

#add_object(name='random', symbol='%', place=None, cursestate=None)

#check if there's a dagger 
def get_weapon_location(game_map: np.ndarray) -> List[Tuple[int, int]]:
    weapons_symbols = "|/)["
    coord_weapons = []
    for symbol in weapons_symbols:
        x, y = np.where(game_map == ord(symbol))
        coord_weapons.extend(list(zip(x, y)))
    return coord_weapons

#def equip_weapon(weapon_position: Tuple[int, int]):
    
    

    
