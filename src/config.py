from icecream import ic

import pygame as pg

from genshin import *

# Basics
MILLISECOND_TO_SECOND = 0.001


# Genshin
AURA_NAMES = {
    ANEMO: 'Anemo',
    BURNING: 'Burning',
    CRYO: 'Cryo',
    DENDRO: 'Dendro',
    ELECTRO: 'Electro',
    FREEZE: 'Freeze',
    GEO: 'Geo',
    HYDRO: 'Hydro',
    PYRO: 'Pyro',
    QUICKEN: 'Quicken'
}
ELEMENT_NAMES = {key: AURA_NAMES[key] for key in AURA_NAMES if key in ELEMENTS}


# Assets
OPT_FONTS = ("ja-jp", "zh-cn")
OPT_LOCALIZATIONS = ("CHS", "CHT", "DE", "EN", "ES", "FR", "ID", "IT", "JP", "KR", "PT", "RU", "TH", "TR", "VI")
OPT_SOUNDS = ("bark.wav",)
OPT_AUDIO = ("close_win.mp3", "open_win.mp3", "switch_task.mp3", "switch_type.mp3")


# App
CAPTION = "Elemental Reactions Visualizer"
GAME_TIME_RESET_CAP = 100  # seconds
ACTIVE_KEYS = (pg.K_SPACE, pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT,
               pg.K_q, pg.K_w, pg.K_e, pg.K_r, pg.K_s, pg.K_d, pg.K_f)

# Return code
PURPOSE_NOT_DETECTED = 100
SET_GAUGE = 101
APPLY_ELEMENT = 102
FLIP_GAMETIME = 103
RES_CODES_BOARD = (PURPOSE_NOT_DETECTED, SET_GAUGE, APPLY_ELEMENT, FLIP_GAMETIME)


# Pygame
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
BACKGROUND_COLOR = (37, 37, 37)
ELEMENT_ICON_SIZE = 80
MARGIN = 20  # margin around screen
GAMETIME_BTN_SIZE = 60
GAUGE_BTN_SIZE = 60
GAUGE_BTN_BORDER = (ELEMENT_ICON_SIZE + GAUGE_BTN_SIZE) / 2
GAUGE_BTN_PADDING = 120
GAUGE_BTN_POSITION = {
    1: (-3, -1),
    1.5: (-3, -2),
    2: (-2, -1),
    4: (-1, -1),
    8: (-1, -2)
}  # (0, 0) is the bottom-most right-most corner of the screen
GAUGE_BTN_SIZE_RATIO = {
    1: 0.6,
    1.5: 1.1,
    2: 0.74,
    4: 0.78,
    8: 0.75
}  # ratio over gauge buttons padding
TEXT_COLOR = (255, 255, 255)
SELECTED_TEXT_COLOR = (247, 252, 88)
TIME_L_MULT = 5.3  # left border multiplier of gauge buttons padding
TIME_R_MULT = 3.7  # right border multiplier of gauge buttons padding
TIME_S_RATIO = 0.25  # ratio of the notation 's' over gauge buttons padding
RULER_COLOR = BACKGROUND_COLOR
RULER_LINE_RATIO = 10
RULER_W = SCREEN_WIDTH * 0.7
RULER_H = 30
RULER_BIG_LINE_W = 2
RULER_BIG_LINE_H = 30
RULER_SMALL_LINE_W = 1
RULER_SMALL_LINE_H = 20
RULER_AREA_H = 0.9 * (SCREEN_HEIGHT + (MARGIN + GAUGE_BTN_BORDER) * GAUGE_BTN_POSITION[8][1])
RULER_PADDING_H = RULER_AREA_H / MAX_COEXIST_AURAS_AVAILABLE
AURA_COLORS = {
    ANEMO: (115, 248, 206),
    GEO: (255, 203, 99),
    PYRO: (252, 156, 13),
    HYDRO: (63, 197, 255),
    ELECTRO: (220, 157, 247),
    CRYO: (152, 255, 254),
    DENDRO: (0, 158, 86)
}
REACTION_COLORS = {
    'Swirl': (115, 248, 206),
    'Crystallize': (255, 155, 0),
    'Vaporize': (238, 202, 129),
    'Overload': (248, 138, 155),
    'Melt': (255, 202, 96),
    'Electro-Charged': (220, 157, 247),
    'Frozen': (156, 255, 255),
    'Superconduct': (187, 180, 255),
    'Burning': (252, 156, 13),
    'Bloom': (0, 231, 75),
    'Quicken': (0, 231, 86)
}
