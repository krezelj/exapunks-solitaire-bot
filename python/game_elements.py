from typing import List

"""
Card encodings
"""

# SIX   = 0bxx0101
# SEVEN = 0bxx0111
# EIGHT = 0bxx1000
# NINE  = 0bxx1001
# TEN   = 0bxx1010


C_RED   = 0b010000
C_BLACK = 0b100000
C_MASK  = 0b110000 # Used to invert colours 

S_CLUBS     = 0b000001
S_DIAMONDS  = 0b000010
S_HEARTS    = 0b000011
S_SPADES    = 0b000100
S_NONE      = 0b000000

VALUE_MASK = 0b001111



class Card():

    __slots__ = ['code', 'parent_code']

    str_code_map = {
        '6R': (C_RED, 6, 0),
        '6B': (C_BLACK, 6, 0),
        '7R': (C_RED, 7, 0),
        '7B': (C_BLACK, 7, 0),
        '8R': (C_RED, 8, 0),
        '8B': (C_BLACK, 8, 0),
        '9R': (C_RED, 9, 0),
        '9B': (C_BLACK, 9, 0),
        '10R': (C_RED, 10, 0),
        '10B': (C_BLACK, 10, 0),
        'C': (0, 0, S_CLUBS),
        'D': (0, 0, S_DIAMONDS),
        'H': (0, 0, S_HEARTS),
        'S': (0, 0, S_SPADES),
    }

    def __init__(self, value=0, colour=0, suit=0, str_code=None):
        if str_code is not None:
            colour, value, suit = self.str_code_map[str_code]

        self.code = colour | value | suit

        if suit == 0:
            self.parent_code = (colour ^ C_MASK) | (value + 1)
        else:
            self.parent_code = suit


    def accepts(self, other):
        return other.parent_code == self.code

    
    def __str__(self):
        c = 'r' if self.code & C_MASK == 16 else ('b' if self.code & C_MASK == 32 else '')
        s = f"{c}{self.code & (~C_MASK)}"
        return s


class Rank():

    __slots__ = ['size', 'is_empty', 'is_finished', 'is_empty_or_finished', 'stack_size', 'cards']

    def __init__(self, cards):
        self.cards = cards
        self.update()


    def accepts(self, card):
        return self.cards[-1].accepts(card)


    def update(self):
        self.size = len(self.cards)
        self.is_empty = len(self.cards) == 0
        self.stack_size = self.__get_stack_size()
        self.is_finished = self.__check_is_finished()
        self.is_empty_or_finished = self.is_empty | self.is_finished


    def __get_stack_size(self):
        if self.is_empty:
            return 0
        size = 1
        for i in range(self.size - 2, -1, -1):
            if self.cards[i].accepts(self.cards[i+1]): 
                size += 1
            else: 
                return size
        return size

    def __check_in_order(self):
        for upper, lower in zip(self.cards[:-1], self.cards[1:]):
            if not upper.accepts(lower): return False
        return True


    def __check_is_finished(self):
        if self.is_empty:
            return True
        if not self.__check_in_order():
            return False
        if (self.cards[0].code & VALUE_MASK) == 10:
            return True
        if (self.size == 4) and (self.cards[0].code & VALUE_MASK) < 5:
            return True
        return False


class Board():

    __slots__ = ['ranks', 'slot']

    def __init__(self, ranks, slot=None) -> None:
        self.ranks = ranks
        self.slot = slot
    
    def slot_is_empty(self):
        return self.slot is None


    def get_hash(self):
        hash_string = ""
        for rank in self.ranks:
            for card in rank.cards:
                hash_string += str(card)
            hash_string += "|"
        if self.slot is not None:
            hash_string += str(self.slot)
        
        return hash_string



# BoardState = List[Rank]