import numpy as np
import matplotlib.pyplot as plt
from utils import *
from heuristic_FD import heuristic_fd
from heuristic_GG import heuristic_gg, BRAVE_PLAYER

def game():
    print("Executing heuristic_fd...")
    hp_history_fd, moves_history_fd = start_game(heuristic_fd)

    print("Executing heuristic_gg...")
    hp_history_gg, moves_history_gg = start_game(heuristic_gg)

    # plot hp history
    hp_plots(hp_history_fd, moves_history_fd, hp_history_gg, moves_history_gg, round(1-BRAVE_PLAYER,1))
    
def start_game(heuristic: Callable[[np.ndarray, Tuple[int, int], Tuple[int, int], int, bool], int]):
    state = env.reset()
    #env.render() 
    #print(env.actions)

    game_map = state['chars']
    game = state['pixel']
    #plt.imshow(state['pixel'])

    start = get_player_location(game_map)
    end_target = get_target_location(game_map)
    weapons = get_weapon_location(game_map)
    print("Agent position:", start)
    print("Target position:", end_target)
    print("Monster position:", get_monster_location(game_map), end="\n\n")

    player_moves = [start]
    image = plt.imshow(game[:, 300:975])

    #finchè non arriviamo alla soluzione
    end_state=False
    hp_rate = 1
    weapon_in_hand = False

    total_moves = 0 # total moves

    hp_history = np.array([]) # hp history
    moves_history = np.array([]) # moves history, 1 move = 1 time unit

    while not end_state:
        # sceglie la cella migliore in base al valore calcolato sulla cella dall'euristica
        current_position=get_player_location(game_map)
        coord=get_best_move(game_map, current_position, end_target, heuristic, hp_rate, weapon_in_hand)
        #print('hp_player: ', hp)

        # raccoglie l'arma se si trova sopra di essa
        if len(weapons)>0 and not(weapon_in_hand) and current_position in weapons: # if i'm on a weapon
            pickup() # pick up the weapon
            wield()  # wield it
            weapon_in_hand = True
        
        #stampa e aggiornamento passo
        game_map, x, end_state, y = env.step(actions_from_path(current_position,[coord])[0])
        hp=game_map["blstats"][10]
        max_hp=game_map["blstats"][11]
        if hp>0:
            hp_rate = (hp/max_hp)
        #print("[" + "*" * hp + "-" * (max_hp-hp) + "]")
        game_map=plot_map(game_map,image)
        player_moves.append(coord)
        total_moves += 1
        
        # for plots
        moves_history = np.append(moves_history, total_moves)
        hp_history= np.append(hp_history, hp_rate)
        #print("HP history: ", hp_history) # debug

    #print("Total moves:", total_moves) # debug

    return hp_history, moves_history
    
