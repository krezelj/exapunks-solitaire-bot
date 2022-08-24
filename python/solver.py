
import numpy as np
from game_elements import *
import os


"""
How is the board encoded?

We have an array of size ten where first 9 elements represent each rank and the last element represents the empty slot

"""

def deapply_move(board_state, move):
    source, target, size = move
    reversed_move = target, source, size
    apply_move(board_state, reversed_move)


def apply_move(board_state, move):
    source, target, size = move

    # get gards
    if source != -1:
        rank = board_state.ranks[source]
        moved_cards = rank.cards[-size:]
        rank.cards = rank.cards[:-size]
        rank.update()
    else:
        moved_cards = [board_state.slot]
        board_state.slot = None

    # move cards
    if target != -1:
        rank = board_state.ranks[target]
        rank.cards.extend(moved_cards)
        rank.update()
    else:
        board_state.slot = moved_cards[0]


def check_win_condition(board_state : Board):
    if not board_state.slot_is_empty():
        return False
    for rank in board_state.ranks:
        if not rank.is_empty_or_finished:
            return False
    return True


def sort_moves(move_list):
    return sorted(move_list, key = lambda x: (x[2], x[1] != -1, x[0] != -1))


def get_moves(board_state : Board, can_remove_from_slot=True):
    move_list = []

    for i, rank in enumerate(board_state.ranks):
        if rank.is_empty_or_finished:
            continue

        stack_head = rank.cards[-rank.stack_size]

        # moves to other ranks
        for j, other_rank in enumerate(board_state.ranks):
            if i == j:
                continue # skip same rank
            if rank.stack_size == rank.size and other_rank.is_empty:
                continue # skip stupid moves

            if other_rank.is_empty or other_rank.accepts(stack_head):
                move_list.append((i, j, rank.stack_size))

        # move to the empty slot
        if rank.stack_size == 1 and board_state.slot_is_empty():
            move_list.append((i, -1, rank.stack_size))

    # move from empty slot only if allowed and possible
    if not board_state.slot_is_empty() and can_remove_from_slot:
        for i, rank in enumerate(board_state.ranks):
            if rank.is_empty or rank.accepts(board_state.slot):
                move_list.append((-1, i, 1))

    return sort_moves(move_list)


def solve(board_state):
    all_hashes = set()
    hash_omits = 0

    move_stack = []
    branch_size_stack = []
    current_move_list = []

    new_moves = get_moves(board_state)
    branch_size_stack.append(len(new_moves))
    move_stack.extend(new_moves)

    moves_evaluated = 0
    while len(move_stack) > 0:
        os.system('cls')
        print(f"Moves evaluated:\t{moves_evaluated}")
        print(f"Moves ommited:\t{hash_omits}")
        moves_evaluated += 1

        current_move = move_stack.pop()
        current_move_list.append(current_move)
        apply_move(board_state, current_move)

        board_hash = board_state.get_hash()
        if board_hash in all_hashes:
            # if exact same board was already visited it couldn't have led to a winning position
            # so it doesn't make sense to visit it again
            # the hash doesn't differentiate between same coloured value cards
            hash_omits += 1
            deapply_move(board_state, current_move_list.pop())
            branch_size_stack[-1] -= 1
        else:
            all_hashes.add(board_hash)
            if (check_win_condition(board_state)):
                return current_move_list

            can_remove_from_slot = current_move[1] != -1
            new_moves = get_moves(board_state, can_remove_from_slot)
            move_stack.extend(new_moves)
            branch_size_stack.append(len(new_moves))

        while (branch_size_stack[-1] == 0):
            deapply_move(board_state, current_move_list.pop())
            branch_size_stack.pop()
            if (len(branch_size_stack) == 0):
                return current_move_list # empty list ?

            branch_size_stack[-1] -= 1

    return current_move_list # empty list




def main():
    card_dict = {
        'r6': Card(value=6, colour=C_RED),
        'b6': Card(value=6, colour=C_BLACK),
        'r7': Card(value=7, colour=C_RED),
        'b7': Card(value=7, colour=C_BLACK),
        'r8': Card(value=8, colour=C_RED),
        'b8': Card(value=8, colour=C_BLACK),
        'r9': Card(value=9, colour=C_RED),
        'b9': Card(value=9, colour=C_BLACK),
        'r10': Card(value=10, colour=C_RED),
        'b10': Card(value=10, colour=C_BLACK),
        'c': Card(suit=1),
        'd': Card(suit=2),
        'h': Card(suit=3),
        's': Card(suit=4),
    }
    ranks = [
        Rank(cards=[*map(card_dict.get, ['b10',   'c',   'h',    'h'])]),
        Rank(cards=[*map(card_dict.get, ['r6',   'r10',   'd',   'r8'])]),
        Rank(cards=[*map(card_dict.get, ['b8',   'h',   'h',    's'])]),
        Rank(cards=[*map(card_dict.get, ['r7',   'c',  'r10',   'r7'])]),
        Rank(cards=[*map(card_dict.get, ['r6',  'r9',   'r9',   'd'])]),
        Rank(cards=[*map(card_dict.get, ['b9',   's',    'b10',    'c'])]),
        Rank(cards=[*map(card_dict.get, ['b9',  'd',    'c',   'b6'])]),
        Rank(cards=[*map(card_dict.get, ['b7',  'r8',  's',   'b8'])]),
        Rank(cards=[*map(card_dict.get, ['b7',  'd',   'b6',    's'])]),
    ]
    board_state = Board(ranks)
    moves = solve(board_state)
    for move in moves:
        print(f"{'slot' if move[0] == -1 else move[0]}\t-->\t{'slot' if move[1] == -1 else move[1]} ({move[2]})")
    


if __name__ == '__main__':
    main()