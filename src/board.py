from icecream import ic

import pygame as pg
from config import *


class Board:
    def __init__(self):
        self.element = None
        self.gauge = None

    def click(self, x, y):
        # check if element buttons being clicked
        for element in range(len(ELEMENTS)):
            if MARGIN + ELEMENT_ICON_SIZE * element < x < MARGIN + ELEMENT_ICON_SIZE * (element + 1) \
                    and SCREEN_HEIGHT - MARGIN - ELEMENT_ICON_SIZE < y < SCREEN_HEIGHT - MARGIN:
                self.element = element
                ic("element clicked~", self.element, self.gauge)
                return APPLY_ELEMENT

        # check if gauge buttons being clicked
        for gauge in AVAILABLE_GAUGES:
            if SCREEN_WIDTH - MARGIN + GAUGE_BTN_PADDING * GAUGE_BTN_POSITION[gauge][0] < x < \
                    SCREEN_WIDTH - MARGIN + GAUGE_BTN_PADDING * GAUGE_BTN_POSITION[gauge][0] \
                    + GAUGE_BTN_PADDING * GAUGE_BTN_SIZE_RATIO[gauge] \
                    and \
                    SCREEN_HEIGHT + (MARGIN + GAUGE_BTN_BORDER) * GAUGE_BTN_POSITION[gauge][1] < y < \
                    SCREEN_HEIGHT + (MARGIN + GAUGE_BTN_BORDER) * GAUGE_BTN_POSITION[gauge][1] + GAUGE_BTN_BORDER:
                self.gauge = gauge
                ic("gauge clicked~", self.gauge)
                return SET_GAUGE

        # check if gametime button being clicked
        if SCREEN_WIDTH - MARGIN - GAUGE_BTN_PADDING * TIME_L_MULT < x < \
                SCREEN_WIDTH - MARGIN - GAUGE_BTN_PADDING * (TIME_R_MULT - TIME_S_RATIO) \
                and SCREEN_HEIGHT - MARGIN - GAUGE_BTN_BORDER < y < SCREEN_HEIGHT - MARGIN:
            return FLIP_GAMETIME

        return PURPOSE_NOT_DETECTED

    def press(self, keys):
        if keys[pg.K_SPACE]:
            return FLIP_GAMETIME
        if keys[pg.K_LEFT]:
            self.gauge = 1
            return SET_GAUGE
        if keys[pg.K_DOWN]:
            self.gauge = 2
            return SET_GAUGE
        if keys[pg.K_RIGHT]:
            self.gauge = 4
            return SET_GAUGE
        if keys[pg.K_UP]:
            self.gauge = 8
            return SET_GAUGE
        if keys[pg.K_q]:
            self.element = ANEMO
            return APPLY_ELEMENT
        if keys[pg.K_w]:
            self.element = CRYO
            return APPLY_ELEMENT
        if keys[pg.K_e]:
            self.element = DENDRO
            return APPLY_ELEMENT
        if keys[pg.K_r]:
            self.element = ELECTRO
            return APPLY_ELEMENT
        if keys[pg.K_s]:
            self.element = GEO
            return APPLY_ELEMENT
        if keys[pg.K_d]:
            self.element = HYDRO
            return APPLY_ELEMENT
        if keys[pg.K_f]:
            self.element = PYRO
            return APPLY_ELEMENT
        return PURPOSE_NOT_DETECTED
