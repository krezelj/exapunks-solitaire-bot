from solver import solve
from detector import  get_boardstate
from auto_player import apply_all_moves, start_new_game

import time

def print_formatted_moves(move_list):
    for move in move_list:
        print(f"{'slot' if move[0] == -1 else move[0] + 1}\t-->\t{'slot' if move[1] == -1 else move[1] + 1}\t({move[2]})")



def main():
    time.sleep(1)
    i = 0
    n_iterations = 10
    while i < n_iterations:
        start_new_game()
        time.sleep(5)
        
        result = solve(get_boardstate())
        move_list = result[0]
        if len(move_list) == 0:
            continue
        i += 1
        apply_all_moves(move_list)
        time.sleep(0.1)


if __name__ == '__main__':
    main()