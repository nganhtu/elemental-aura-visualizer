from icecream import ic

from genshin import *

# Basics
MS_IN_A_SEC = 1000


# Genshin
AURA_NAMES = {
    ANEMO: 'anemo',
    BURNING: 'burning',
    CRYO: 'cryo',
    DENDRO: 'dendro',
    ELECTRO: 'electro',
    FREEZE: 'freeze',
    GEO: 'geo',
    HYDRO: 'hydro',
    PYRO: 'pyro',
    QUICKEN: 'quicken'
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


# Return code
OK = 100
SET_GAUGE = 101
APPLY_ELEMENT = 102
FLIP_GAMETIME = 103


# Pygame
SCRW = 1280   # screen width
SCRH = 720   # screen height
FPS = 60   # frames per second
BGRC = (37, 37, 37)   # background color
ELMS = 80   # element icon size
MARGIN = 20  # margin around screen
GAUS = 60  # gauge button size
GTIS = 60  # gametime size
GAUB = (ELMS + GAUS) / 2  # gauge button border
GPAD = 120  # gauge buttons padding
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
TXTC = (255, 255, 255)   # text color
TXTC_SELECTED = (247, 252, 88)  # selected text color
TIME_LMUL = 5.3  # left border multiplier of gauge buttons padding
TIME_RMUL = 3.7  # right border multiplier of gauge buttons padding
TIME_S_RATIO = 0.25  # ratio of the notation 's' over gauge buttons padding
RULER_COLOR = (127, 127, 127)
RULER_LINE_RATIO = 10
RULER_W = SCRW * 0.7
RULER_H = 30
RULER_BLINE_W = 2
RULER_BLINE_H = 30
RULER_SLINE_W = 1
RULER_SLINE_H = 20
RULER_AREA_H = 0.9 * (SCRH + (MARGIN + GAUB) * GAUGE_BTN_POSITION[8][1])
RULER_PADDING_H = RULER_AREA_H / MAX_COEXIST_AURAS_AVAILABLE
ELEMENT_COLOR = {
    ANEMO: (115, 248, 206),
    GEO: (255, 203, 99),
    PYRO: (252, 156, 13),
    HYDRO: (63, 197, 255),
    ELECTRO: (220, 157, 247),
    CRYO: (152, 255, 254),
    DENDRO: (0, 158, 86)
}
REACTION_COLOR = {
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
