from icecream import ic

# Basics
MS_IN_A_SEC = 1000


# Genshin
ANEMO, CRYO, DENDRO, ELECTRO, GEO, HYDRO, PYRO = 0, 1, 2, 3, 4, 5, 6  # use to draw btns, don't change
BURNING, FREEZE, QUICKEN = 10, 11, 12
ELEMENTS = (ANEMO, CRYO, DENDRO, ELECTRO, GEO, HYDRO, PYRO)
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
OPT_SOUNDS = ("bark")


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
