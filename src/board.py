from icecream import ic

from config import *
import pygame as pg


class Board():
    def __init__(self):
        self.ACTIVE_KEYS = [pg.K_SPACE]
        self.element = None
        self.gauge = None

    def click(self, x, y):
        # check if element buttons being clicked
        for element in range(ELEMENTS_NUM):
            if MARGIN + ELMS * element < x < MARGIN + ELMS * (element + 1) \
                and SCRH - MARGIN - ELMS < y < SCRH - MARGIN:
                self.element = element
                ic("element clicked~", self.element, self.gauge) # TODO apply element

        # check if gauge buttons being clicked
        for i in range(3):
            if SCRW - MARGIN - GPAD * (3 - i) < x < SCRW - MARGIN - GPAD * (3 - i - GBHR) \
                and SCRH - MARGIN - GAUB < y < SCRH - MARGIN:
                self.gauge = 2 ** i
                ic("gauge clicked~", self.gauge)

        # check if gametime button being clicked
        if SCRW - MARGIN - GPAD * TIME_LMUL < x < SCRW - MARGIN - GPAD * (TIME_RMUL - 1 + GBHR) \
            and SCRH - MARGIN - GAUB < y < SCRH - MARGIN:
            return FLIP_GAMETIME

    def press(self, keys):
        if keys[pg.K_SPACE]:
            return FLIP_GAMETIME
