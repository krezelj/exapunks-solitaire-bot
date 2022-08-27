import pyautogui as gui
import time

gui.FAILSAFE = False

BOARD_X_OFFSET = 380
BOARD_Y_OFFSET = 470

RANKS = 9
CARDS_PER_RANK = 4

CARD_WIDTH = 134
CARD_HEIGHT = 30

SLOT_X = BOARD_X_OFFSET + 8 * CARD_WIDTH
SLOT_Y = BOARD_Y_OFFSET - 8 * CARD_HEIGHT

def start_new_game():
    gui.moveTo(x=1400, y=900)
    gui.mouseDown(button='left')
    gui.mouseUp(button='left')


def position_mouse_on_card(rank, row):
    if rank == -1:
        x_pos = SLOT_X
        y_pos = SLOT_Y
    else:
        x_pos = rank * CARD_WIDTH + BOARD_X_OFFSET
        y_pos = row * CARD_HEIGHT + BOARD_Y_OFFSET
    gui.moveTo(x=x_pos, y=y_pos)


def apply_move(source, target):
    source, target
    if source == -1:
        y_offset = BOARD_Y_OFFSET - SLOT_Y 
        source = 8
    elif target == -1:
        y_offset = SLOT_Y - BOARD_Y_OFFSET
        target = 8 
    else:
        y_offset = 0

    x_offset = (target - source) * CARD_WIDTH
    # print(gui.position())
    pos = gui.position()
    x_pos = pos.x + x_offset
    y_pos = pos.y + y_offset
    gui.mouseDown()
    gui.dragTo(x=x_pos, y=y_pos, duration=0.0, mouseDownUp=False, button='left')
    gui.mouseUp()



def apply_all_moves(move_list):
    card_count = [CARDS_PER_RANK for _ in range(RANKS)]
    for move in move_list:
        source, target, size = move

        rank = source
        row = -1 if source == -1 else card_count[source] - size
        position_mouse_on_card(rank, row)
        apply_move(source, target)
        
        # update card count
        if source != -1:
            card_count[source] -= size
        if target != -1:
            card_count[target] += size


def main():
    time.sleep(3)
    start_new_game()



if __name__ == '__main__':
    main()