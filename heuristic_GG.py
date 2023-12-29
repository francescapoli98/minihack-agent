import numpy as np
from utils import *
import math
from typing import Tuple
from typing import List, Tuple


# ------------------------------ CONSTANT ------------------------------
NEAR_MONSTERS_RANGE = 4                     # range to consider a monster dangerous
ETA_NEAR_MONSTERS_TARGET = 0.5              # weight of near monsters   
DISTANCE_MIN = 1                            # minimum distance
DISTANCE_MAX = 18                           # maximum distance
NEAR_MONSTER_MIN = 1                        # minimum number of monster
BRAVE_PLAYER = 0.6                          # brave of the player (value between 0 and 1)
ANGLES = [(1,33),(18,33),(1,50),(18,50)]    # position of angles in the map
TRAP_RANGE=math.pi/4                        # range to consider a trap
TRAP_DISTANCE=4                             # distance to consider monsters
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



# heuristic function that return a score for the move
def heuristic_gg(game_map: np.ndarray, move: Tuple[int, int], end_target: Tuple[int, int], hp_rate: int, weapon_in_hand: bool) -> float:
    # initial target is the end target
    target = end_target

    # get the position of the monsters, the player and the weapons
    monsters_position: List[Tuple[int, int]]= get_monster_location(game_map)
    player_position: Tuple[int, int] = get_player_location(game_map)
    weapons: List[Tuple[int, int]] = get_weapon_location(game_map)

    # if the player is in the end target and there are monsters, the score is infinite
    if move == end_target and len(monsters_position)!=0:
        return math.inf
    
    # list with information about the monsters
    info_monsters: List[MonsterInfo] = Heuristic_utils.get_info_monsters(player_position, monsters_position)

    # if the player is not brave and there are monsters, the player will escape
    if BRAVE_PLAYER <= (1-hp_rate) and len(monsters_position) > 0:
        
        # check if the player is in a trap
        if Heuristic_utils.is_trap(player_position,info_monsters):
            return Heuristic_utils.escape_trap(move,info_monsters)        
                
        # check if there is a monster near the player
        nearest_monster = Heuristic_utils.nearest_monster(info_monsters)
        if nearest_monster.distance < 3:
            return Heuristic_utils.escape_near_monster(move, nearest_monster, info_monsters)

        # default strategy to escape from the monsters
        return Heuristic_utils.default_escape(monsters_position, player_position, move)

    
    # if the player brave and there are monsters, the player will fight
    if len(monsters_position) > 0:
        # the player go to the weapon
        if not weapon_in_hand and len(weapons) > 0:
            target = Heuristic_utils.best_weapon(player_position, weapons)

        # the player fight the monsters
        else:
            # select the best monster target to fight
            target = Heuristic_utils.best_monster_to_fight(info_monsters)

    #  the player go to the target
    return Heuristic_utils.score(move,target,info_monsters)




# ------------------------------ Heurstic UTILS ------------------------------
class Heuristic_utils:
    @staticmethod
    def nearest_monster(info_monsters: [MonsterInfo]) -> MonsterInfo: 
        """
            Finds the nearest monster from a list of monster information.

            Args:
                info_monsters (list): A list of MonsterInfo objects representing the information of each monster.

            Returns:
                MonsterInfo: The MonsterInfo object representing the nearest monster.
        """
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
        """
        Calculates the score for a given move based on the target position and information about monsters.

        Parameters:
        move (Tuple[int, int]): The coordinates of the move.
        target (Tuple[int, int]): The coordinates of the target position.
        info_monsters ([MonsterInfo]): A list of MonsterInfo objects containing information about the monsters.

        Returns:
        float: The calculated score for the move.
        """
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
            
        # check if there are at least 2 monsters
        if len(info_monsters_reduced) < 2:
            return False
        
        # calculate the angle between the player and the monsters
        angles = [math.atan2(monster.position[1] - player_position[1], monster.position[0] - player_position[0]) for monster in info_monsters_reduced]

        # sort the angles
        angles.sort()

        # check the interval between the angles
        count = 0  
        for i in range(1, len(angles)):
            if abs(angles[i] - angles[i - 1]) > TRAP_RANGE:
                count += 1
            if count >= 2:
                # return trap
                return True

        # check the interval between the first and the last angle
        if abs(angles[0] + 2 * math.pi - angles[-1]) > TRAP_RANGE:
            count += 1
            
        # return True if there are at least 2 intervals
        return count >= 2

    @staticmethod
    def get_info_monsters(player_position:Tuple[int,int],monsters_position:List[Tuple[int,int]]) -> List[MonsterInfo]: 
        """
        Get information about monsters.

        Args:
            player_position (Tuple[int, int]): The position of the player.
            monsters_position (List[Tuple[int, int]]): The positions of the monsters.

        Returns:
            List[MonsterInfo]: A list of MonsterInfo objects containing information about each monster.
        """
        info_monsters: List[MonsterInfo] = []
        for monster in monsters_position:
            info_monsters.append(
                MonsterInfo(monster, euclidean_distance(player_position, monster), Heuristic_utils.near_monsters(monster,monsters_position))
            )
        return info_monsters
    
    @staticmethod
    def best_weapon(player_position:Tuple[int, int], weapons:[Tuple[int, int]]):
        """
        Finds the best weapon for the player based on the player's position and the available weapons.

        Args:
            player_position (Tuple[int, int]): The position of the player.
            weapons ([Tuple[int, int]]): A list of weapon positions.

        Returns:
            Tuple[int, int]: The position of the best weapon.
        """
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
        """
        Calculates the heuristic score for escaping a trap.

        Args:
            move (Tuple[int,int]): The move to evaluate.
            info_monsters (List[MonsterInfo]): List of information about the monsters.

        Returns:
            float: The heuristic score for the move.
        """
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
        """
        Calculates the escape score for a given move based on the distance from the nearest monster and the positions of other monsters.

        Args:
            move (Tuple[int, int]): The move to evaluate.
            near_monster (Tuple[int, int]): The position of the nearest monster.
            info_monsters (List[MonsterInfo]): A list of MonsterInfo objects containing information about other monsters.

        Returns:
            float: The escape score for the move.
        """
        if move in ANGLES:
            return math.inf
        sum=1
        for info_monster in info_monsters:
            sum+=(DISTANCE_MAX-euclidean_distance(move,info_monster.position))
        return -math.ceil(euclidean_distance(move,near_monster.position)) + (Heuristic_utils.normalize(sum,0,(DISTANCE_MAX-1)*len(info_monsters)))
    
    @staticmethod
    def default_escape(monsters_position:List[Tuple[int,int]], player_position:Tuple[int,int], move:Tuple[int,int]):
        """
        Calculates the escape score for a given move based on the positions of monsters and the player.

        Parameters:
        monsters_position (List[Tuple[int,int]]): A list of tuples representing the positions of monsters.
        player_position (Tuple[int,int]): A tuple representing the position of the player.
        move (Tuple[int,int]): A tuple representing the move to be evaluated.

        Returns:
        int: The escape score for the move.
        """
        sum = 0
        for monster in monsters_position:
            sum -= euclidean_distance(move, monster) * ((DISTANCE_MAX - euclidean_distance(player_position, monster)))
        return sum 
    
    @staticmethod
    def best_monster_to_fight(info_monsters:List[MonsterInfo]):
        """
        Finds the best monster to fight based on a heuristic calculation.

        Args:
            info_monsters (List[MonsterInfo]): A list of MonsterInfo objects containing information about each monster.

        Returns:
            Tuple[int, int]: The position of the best monster to fight.
        """
        NEAR_MONSTER_MAX = len(info_monsters)
        min = math.inf
        for monster in info_monsters:
            weight = (Heuristic_utils.normalize(monster.near_monsters, NEAR_MONSTER_MIN, NEAR_MONSTER_MAX) * ETA_NEAR_MONSTERS_TARGET) + Heuristic_utils.normalize(monster.distance, DISTANCE_MIN, DISTANCE_MAX)

            if weight < min:
                min = weight
                target = monster.position
        return target
