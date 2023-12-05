import numpy as np
from utils import *
import math
from typing import Tuple

NEAR_MONSTERS_RANGE = 4
ETA_NEAR_MONSTERS_TARGET = 0.5
DISTANCE_MIN = 1
DISTANCE_MAX = 18
NEAR_MONSTER_MIN = 1
BRAVE_PLAYER = 0
MIN_HP_PLAYER = 1
MAX_HP_PLAYER = 12  #! da aggiungere come parametro nel report e in heuristics
ANGLES = [(1,30),(1,49),(20,30),(20,49)]   
TRAP_RANGE=math.pi/4 #! da definire
TRAP_DISTANCE=4 #! da definire

# class MonsterInfo
from typing import List, Tuple

class MonsterInfo:
    """
    Represents information about a monster.

    Attributes:
        position (Tuple[int, int]): The position of the monster.
        distance (int): The distance of the monster from a certain point.
        near_monsters (List[Tuple[int, int]]): A list of positions of nearby monsters.
    """

    def __init__(self, position: Tuple[int, int], distance: int, near_monsters: List[Tuple[int, int]]):
        self._position = position
        self._distance = distance
        self._near_monsters = near_monsters

    @property
    def position(self) -> Tuple[int, int]:
        return self._position

    @position.setter
    def position(self, value: Tuple[int, int]):
        self._position = value

    @property
    def distance(self) -> int:
        return self._distance

    @distance.setter
    def distance(self, value: int):
        self._distance = value

    @property
    def near_monsters(self) -> List[Tuple[int, int]]:
        return self._near_monsters

    @near_monsters.setter
    def near_monsters(self, value: List[Tuple[int, int]]):
        self._near_monsters = value




def heuristic_gg(game_map: np.ndarray, move: Tuple[int, int], end_target: Tuple[int, int], hp_player: int):

    # imposta il target uguale al target finale di default (scale della mappa)
    target = end_target

    # prende la posizione di tutti i mostri presenti nella mappa
    list_monsters = get_monster_location(game_map)
    current_position = get_player_location(game_map)


    # se la cella considerata è il target finale e ci sono mostri nella mappa, ritorna infinito (non è possibile raggiungere il target finale se ci sono mostri)
    if move == end_target and len(list_monsters)!=0:
        return math.inf
    
    info_monsters: List[MonsterInfo] = []
    for monster in list_monsters:
        info_monsters.append(
            MonsterInfo(monster, euclidean_distance(current_position, monster), near_monsters(monster,list_monsters))
        )
    # controlla se il player ha abbastanza vita per combattere un mostro
    if hp_player <= (12-BRAVE_PLAYER):
        sum = 0
        for monster in list_monsters:
            sum -= euclidean_distance(move, monster)

        sum2 = 0
        for angle in ANGLES:
            if -euclidean_distance(move, angle) < sum2:
                sum2 = -euclidean_distance(move, angle)

        #strtegia di fuga in caso l'agente è circondato dai mostri (controllare il caso in cui il player è circondato da 1 mostro nell'angolo)
        if is_trap(current_position,info_monsters):
            max_monsters_distance=0
            for angle in ANGLES:
                new_distance=0
                for monster in list_monsters:
                    new_distance+=euclidean_distance(angle, monster)
                if new_distance > max_monsters_distance:
                    max_monsters_distance=new_distance
                    target = angle
            return score(move,target,info_monsters)
        
        return sum - sum2

    
    # se ci sono mostri nella mappa, individua fra essi il target migliore
    
    if len(list_monsters) > 0:
        # crea una lista di oggetti MonsterInfo, che contengono le informazioni di ogni mostro (posizione, distanza dal player, numero di mostri vicini)


        NEAR_MONSTER_MAX = len(list_monsters)


        # scelgo il mostro con peso migliore (peso = distanza e numero di mostri vicini)
        #print("cell", current_position)
        min = math.inf
        for monster in info_monsters:
            weight = (normalize(monster.near_monsters, NEAR_MONSTER_MIN, NEAR_MONSTER_MAX) * ETA_NEAR_MONSTERS_TARGET) + normalize(monster.distance, DISTANCE_MIN, DISTANCE_MAX)

            # setta come target il mostro che minimizza (distanza e numero di mostri vicini)
            if weight < min:
                min = weight
                target = monster.position
        #print("target", target)
        #print("score", score(move,target,info_monsters))

    return score(move,target,info_monsters)



def normalize(value: int, min_val: int, max_val: int) -> float:
    """
    Normalize a value between a minimum and maximum value.

    Args:
        value (int): The value to be normalized.
        min_val (int): The minimum value of the range.
        max_val (int): The maximum value of the range.

    Returns:
        float: The normalized value.
    """
    # Controllo se il denominatore è zero
    if max_val - min_val == 0:
        return 0.0
    return (value - min_val) / (max_val - min_val)



def score(player_position:Tuple[int, int],target:Tuple[int, int], info_monsters:[MonsterInfo]) -> float:
    if len(info_monsters)==0:
        return euclidean_distance(player_position,target)
    
    sum=1
    for info_monster in info_monsters:
        if info_monster.position!=target:
            sum+=info_monster.distance

    return euclidean_distance(player_position,target) # - (sum/len(info_monsters)-1)
        



def near_monsters(cell: Tuple[int, int], list_monsters: [Tuple[int, int]]):
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

    
def is_trap(current_position: Tuple[int, int], info_monsters: List[MonsterInfo]) -> bool:
    """
    Determines if the current position is a trap based on the given information about the monsters.

    Args:
        current_position (Tuple[int, int]): The current position of the player.
        info_monsters (List[MonsterInfo]): The information about the monsters.

    Returns:
        bool: True if the current position is a trap, False otherwise.
    """
    #remove from info_mosters the monsters that are too far distance 4 from the player
    info_monsters_reduced=[]
    for monster in info_monsters:
        if monster.distance <= TRAP_DISTANCE:
            info_monsters_reduced.append(monster)
        if monster.distance==1 and current_position in ANGLES: #!da controllare
            return True
        
    # Verifica che ci siano almeno min_monsters mostri nella lista
    if len(info_monsters_reduced) < 2:
        return False
    
    # Calcola la distanza angolare tra la tua posizione e ciascun mostro
    angles = [math.atan2(monster.position[1] - current_position[1], monster.position[0] - current_position[0]) for monster in info_monsters_reduced]

    # Ordina gli angoli in senso orario
    angles.sort()

    # Verifica se ci sono almeno min_monsters non allineati entro il trap_range
    count = 0  
    for i in range(1, len(angles)):
        if abs(angles[i] - angles[i - 1]) > TRAP_RANGE:
            count += 1
        if count >= 2:
            return True

    # Controlla l'intervallo tra l'ultimo angolo e il primo
    if abs(angles[0] + 2 * math.pi - angles[-1]) > TRAP_RANGE:
        count += 1

    return count >= 2
