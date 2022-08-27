import pygetwindow as gw
import PIL.ImageGrab
import numpy as np
import time
import game_elements as ge

BOARD_LEFT_EDGE = 365
BOARD_UPPER_EDGE = 460
BOARD_RIGHT_EDGE = 1465
BOARD_LOWER_EDGE = 580

BOARD_WIDTH = BOARD_RIGHT_EDGE - BOARD_LEFT_EDGE
BOARD_HEIGHT = BOARD_LOWER_EDGE - BOARD_UPPER_EDGE

CARD_WIDTH = 134
CARD_HEIGHT = 30
LEFT_OFFSET = 10
UPPER_OFFSET = 10

RANKS = 9
CARDS_PER_RANK = 4


def get_screenshot():
    exapunk_window = gw.getWindowsWithTitle('EXAPUNKS')[0]
    exapunk_window.moveTo(0, 0)
    exapunk_window.minimize()
    exapunk_window.restore()
    time.sleep(0.5)
    screenshot = PIL.ImageGrab.grab().crop((BOARD_LEFT_EDGE, BOARD_UPPER_EDGE, BOARD_RIGHT_EDGE, BOARD_LOWER_EDGE))
    return screenshot


def get_boardstate_from_screenshot(screenshot : PIL.ImageGrab.Image):
    str_codes = ['6R', '6B', '7R', '7B', '8R', '8B', '9R', '9B', '10R', '10B', 'C', 'D', 'H', 'S']
    template = np.array([128.,   40.,    209.,   191.,   117.,   18.,    157.,
                94.,    162.,   102.,   187.,   110.,   111.,   6.])
    data = np.array(screenshot.getdata()).reshape((BOARD_HEIGHT, BOARD_WIDTH, 3))
    data = np.mean(data, axis=2)

    ranks = []
    for rank in range(RANKS):
        cards = []
        for row in range(CARDS_PER_RANK):
            card_pixel = data[UPPER_OFFSET + (row * CARD_HEIGHT), LEFT_OFFSET + (rank * CARD_WIDTH)]
            difference = np.abs(card_pixel - template)
            str_code = str_codes[np.argmin(difference)]
            cards.append(ge.Card(str_code=str_code))
        
        ranks.append(ge.Rank(cards))

    return ge.Board(ranks)


def get_boardstate():
    return get_boardstate_from_screenshot(get_screenshot())



def main():
    board_state = get_boardstate()
    a = 0


if __name__ == '__main__':
    main()
        
