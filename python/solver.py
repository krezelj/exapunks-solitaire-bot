
from game_elements import *
import time

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


def solve(board_state, stop_at_iterations=-1):
    move_stack = []
    branch_size_stack = []
    current_move_list = []
    all_hashes = set()

    new_moves = get_moves(board_state)
    branch_size_stack.append(len(new_moves))
    move_stack.extend(new_moves)

    # stat variables
    moves_evaluated = 0
    hash_omits = 0
    while len(move_stack) > 0:
        if (moves_evaluated == stop_at_iterations): 
            return [], moves_evaluated, hash_omits
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
                return current_move_list, moves_evaluated, hash_omits

            can_remove_from_slot = current_move[1] != -1
            new_moves = get_moves(board_state, can_remove_from_slot)
            move_stack.extend(new_moves)
            branch_size_stack.append(len(new_moves))

        while (branch_size_stack[-1] == 0):
            if (len(current_move_list) == 0):
                return current_move_list, moves_evaluated, hash_omits
            deapply_move(board_state, current_move_list.pop())
            branch_size_stack.pop()
            if (len(branch_size_stack) == 0):
                return current_move_list, moves_evaluated, hash_omits

            branch_size_stack[-1] -= 1

    return current_move_list, moves_evaluated, hash_omits


def main():
    import cProfile
    cProfile.run("benchmark()")
    

if __name__ == '__main__':
    main()