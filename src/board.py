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
                ic("element clicked~", self.element, self.gauge)
                return APPLY_ELEMENT

        # check if gauge buttons being clicked
        for gauge in AVAILABLE_GAUGES:
            if SCRW - MARGIN + GPAD * GAUGE_BTN_POSITION[gauge][0] < x < \
               SCRW - MARGIN + GPAD * GAUGE_BTN_POSITION[gauge][0] + GPAD * GAUGE_BTN_SIZE_RATIO[gauge] \
               and \
               SCRH + (MARGIN + GAUB) * GAUGE_BTN_POSITION[gauge][1] < y < \
               SCRH + (MARGIN + GAUB) * GAUGE_BTN_POSITION[gauge][1] + GAUB:
                self.gauge = gauge
                ic("gauge clicked~", self.gauge)
                return SET_GAUGE

        # check if gametime button being clicked
        if SCRW - MARGIN - GPAD * TIME_LMUL < x < SCRW - MARGIN - GPAD * (TIME_RMUL - TIME_S_RATIO) \
            and SCRH - MARGIN - GAUB < y < SCRH - MARGIN:
            return FLIP_GAMETIME

    def press(self, keys):
        if keys[pg.K_SPACE]:
            return FLIP_GAMETIME
