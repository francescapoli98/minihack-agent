def heuristic_fd(game_map: np.ndarray, move: Tuple[int, int], end_target: Tuple[int, int], hp_player: int):
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


##########################################

    #initialising the target based off the map
    # target = end_target #target is the exit by default
    # if len(weapon_location)!=0: #if the agent has no weapons and there are weapons in the room
    #     target = weapon_location[0] #the target is the weapon
    # elif (len(weapon_location)==0 && len(monster_location)!=0): #if there are monsters in the room and i have a weapon
    #     target = monster_location[0] #the target is the monster
        
##########################################
    # distance from the exit
    target_distance = manhattan_distance(move, end_target)

    # if the next move is the target but there are monsters alive, the agent cannot exit the room
    if move == end_target and len(monster_location)!=0:
        return inf
    
    # distance from the weapon, the agents will try to pick up the nearest weapon
    # weapon_distance = manhattan_distance(move, weapon_location[0]) if weapon_location else inf
    min_weapon = inf
    if weapon_location: #if there are weapons in the room
        for weapon in weapon_location:  
            if manhattan_distance(move, weapon) < min_weapon:
                min_weapon = manhattan_distance(move, weapon)
    
    # distance from the monster, the agents will try to kill the nearest monster first
    min_monster = inf
    if monster_location: #if there are monsters in the room
        for monster in monster_location: #for each monster in the room
            if manhattan_distance(move, monster) < min_monster: 
                min_monster = manhattan_distance(move, monster) 
    
    # heuristic weighted sum of the distances
    weighted_heuristic = (
        weapon_weight * min_weapon +
        monster_weight * min_monster +
        exit_weight * target_distance 
    )

    # we can scale the heuristic as we want
    #scaled_heuristic = int(weighted_heuristic * 0.1)  # 0.1 is the scale factor

    return int(weighted_heuristic)