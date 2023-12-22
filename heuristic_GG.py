import numpy as np
from utils import *
import math
from typing import Tuple
from typing import List, Tuple


# ------------------------------ CONSTANT ------------------------------
NEAR_MONSTERS_RANGE = 4
ETA_NEAR_MONSTERS_TARGET = 0.5
DISTANCE_MIN = 1
DISTANCE_MAX = 18
NEAR_MONSTER_MIN = 1
# valore compreso tra 0 e 1 (percentuale di vita minima per cui il player è disposto a combattere un mostro)
BRAVE_PLAYER = 0.2
# posizioni degli angoli della mappa  
ANGLES = [(1,33),(18,33),(1,50),(18,50)]
# range angolare per cui si considera che il player è circondato
TRAP_RANGE=math.pi/4 
# distanza massima per cui si considerano i mostri attorno al player
TRAP_DISTANCE=4 
# ------------------------------ ---------- ------------------------------



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




def heuristic_gg(game_map: np.ndarray, move: Tuple[int, int], end_target: Tuple[int, int], hp_rate: int, weapon_in_hand: bool) -> float:

    # imposta il target uguale al target finale di default (scale della mappa)
    target = end_target

    # prende la posizione di tutti i mostri presenti nella mappa
    monsters_position: List[Tuple[int, int]]= get_monster_location(game_map)
    player_position: Tuple[int, int] = get_player_location(game_map)
    weapons: List[Tuple[int, int]] = get_weapon_location(game_map)


    # se la cella considerata è il target finale e ci sono mostri nella mappa, ritorna infinito (non è possibile raggiungere il target finale se ci sono mostri)
    if move == end_target and len(monsters_position)!=0:
        return math.inf
    
    # per ongi mostro calcola le seguenti informazioni: distanza dal player e numero mostri vicini
    info_monsters: List[MonsterInfo] = Heuristic_utils.get_info_monsters(player_position, monsters_position)


    # verifica se il player è abbastanza coraggio per affrontare un combattimento
    if BRAVE_PLAYER <= (1-hp_rate) and len(monsters_position) > 0:

        #strategia di fuga in caso l'agente è circondato dai mostri (controllare il caso in cui il player è circondato da 1 mostro nell'angolo)
        if Heuristic_utils.is_trap(player_position,info_monsters):
            return Heuristic_utils.escape_trap(move,info_monsters)        
                
        #se c'è un mostro molto vicino (prossimo ad accatare il player) scappa da quel mostro
        nearest_monster = Heuristic_utils.nearest_monster(info_monsters)
        if nearest_monster.distance < 3:
            return Heuristic_utils.escape_near_monster(move, nearest_monster, info_monsters)

        # cerca di scappare dai mostri (da peso maggiore ai mostri più vicini)
        return Heuristic_utils.default_escape(monsters_position, player_position, move)

    
    # se ci sono mostri nella mappa, individua fra essi il target migliore
    if len(monsters_position) > 0:
        # caso in cui prende l'arma
        if not weapon_in_hand and len(weapons) > 0:
            target = Heuristic_utils.best_weapon(player_position, weapons)

        # caso in cui combatte i mostri
        else:
            # seleziona fra tutti i mostri quello con cui ingaggiare un combattimento
            target = Heuristic_utils.best_monster_to_fight(info_monsters)


    return Heuristic_utils.score(move,target,info_monsters)





class Heuristic_utils:
    @staticmethod
    def nearest_monster(info_monsters: [MonsterInfo]) -> MonsterInfo: 
        min = math.inf
        near_monster = None
        for info_monster in info_monsters:
            if info_monster.distance < min:
                min = info_monster.distance
                near_monster = info_monster

        return near_monster

    @staticmethod
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

    
    @staticmethod
    def score(move:Tuple[int, int],target:Tuple[int, int], info_monsters:[MonsterInfo]) -> float:
        if len(info_monsters)==0:
            return euclidean_distance(move,target)
        
        sum=1
        count=0
        for info_monster in info_monsters:
            if info_monster.position!=target:
                sum+=(DISTANCE_MAX-euclidean_distance(move,info_monster.position))
                count+=1

        return math.ceil(euclidean_distance(move,target)) + (Heuristic_utils.normalize(sum,0,(DISTANCE_MAX-1)*count))                        

    @staticmethod
    def near_monsters(cell: Tuple[int, int], monsters_position: [Tuple[int, int]]):
        """
        Counts the number of monsters within the given range of vision.

        Parameters:
        game_map (np.ndarray): The game map.
        cell (Tuple[int, int]): The current cell coordinates.
        monsters_position ([Tuple[int, int]]): List of monster coordinates.

        Returns:
        int: The number of monsters within the range of vision.
        """
        num_monsters = 0

        for monster in monsters_position:
            if euclidean_distance(cell, monster) <= NEAR_MONSTERS_RANGE:
                num_monsters += 1

        return num_monsters

    @staticmethod
    def is_trap(player_position: Tuple[int, int], info_monsters: List[MonsterInfo]) -> bool:
        """
        Determines if the current position is a trap based on the given information about the monsters.

        Args:
            player_position (Tuple[int, int]): The current position of the player.
            info_monsters (List[MonsterInfo]): The information about the monsters.

        Returns:
            bool: True if the current position is a trap, False otherwise.
        """
        #remove from info_mosters the monsters that are too far distance 4 from the player
        info_monsters_reduced=[]
        for monster in info_monsters:
            if monster.distance <= TRAP_DISTANCE:
                info_monsters_reduced.append(monster)
            
        # Verifica che ci siano almeno min_monsters mostri nella lista
        if len(info_monsters_reduced) < 2:
            return False
        
        # Calcola la distanza angolare tra la tua posizione e ciascun mostro
        angles = [math.atan2(monster.position[1] - player_position[1], monster.position[0] - player_position[0]) for monster in info_monsters_reduced]

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

    @staticmethod
    def get_info_monsters(player_position:Tuple[int,int],monsters_position:List[Tuple[int,int]]) -> List[MonsterInfo]: 
        info_monsters: List[MonsterInfo] = []
        for monster in monsters_position:
            info_monsters.append(
                MonsterInfo(monster, euclidean_distance(player_position, monster), Heuristic_utils.near_monsters(monster,monsters_position))
            )
        return info_monsters
    
    @staticmethod
    def best_weapon(player_position:Tuple[int, int], weapons:[Tuple[int, int]]):
        min = math.inf
        best_weapon = weapons[0]
        for weapon in weapons:
            distance = euclidean_distance(player_position, weapon)
            if distance < min:
                min = distance
                best_weapon = weapon

        return best_weapon
    
    
    @staticmethod
    def escape_trap(move:Tuple[int,int], info_monsters:List[MonsterInfo]):
        if move in ANGLES:
            return math.inf
        max_monster_distance=0
        for angle in ANGLES:
            new_distance=0
            for monster in info_monsters:
                new_distance+=euclidean_distance(angle, monster.position)
            if new_distance > max_monster_distance:
                max_monster_distance=new_distance
                target = angle

        return Heuristic_utils.score(move,target,info_monsters)
    
    @staticmethod
    def escape_near_monster(move:Tuple[int,int], near_monster:Tuple[int,int], info_monsters:List[MonsterInfo]):
        if move in ANGLES:
            return math.inf
        sum=1
        for info_monster in info_monsters:
            sum+=(DISTANCE_MAX-euclidean_distance(move,info_monster.position))
        return -math.ceil(euclidean_distance(move,near_monster.position)) + (Heuristic_utils.normalize(sum,0,(DISTANCE_MAX-1)*len(info_monsters)))
    
    @staticmethod
    def default_escape(monsters_position:List[Tuple[int,int]], player_position:Tuple[int,int], move:Tuple[int,int]):
        sum = 0
        for monster in monsters_position:
            sum -= euclidean_distance(move, monster) * ((DISTANCE_MAX - euclidean_distance(player_position, monster)))
        return sum 
    
    @staticmethod
    def best_monster_to_fight(info_monsters:List[MonsterInfo]):
        NEAR_MONSTER_MAX = len(info_monsters)
        min = math.inf
        for monster in info_monsters:
            weight = (Heuristic_utils.normalize(monster.near_monsters, NEAR_MONSTER_MIN, NEAR_MONSTER_MAX) * ETA_NEAR_MONSTERS_TARGET) + Heuristic_utils.normalize(monster.distance, DISTANCE_MIN, DISTANCE_MAX)

            # setta come target il mostro che minimizza (distanza e numero di mostri vicini)
            if weight < min:
                min = weight
                target = monster.position
        return target
