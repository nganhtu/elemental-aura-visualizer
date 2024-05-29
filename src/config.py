from icecream import ic

# Basics
MS_IN_A_SEC = 1000


# Genshin
ANEMO, CRYO, DENDRO, ELECTRO, GEO, HYDRO, PYRO = 0, 1, 2, 3, 4, 5, 6 # alphabet order
ELEMENTS = (ANEMO, CRYO, DENDRO, ELECTRO, GEO, HYDRO, PYRO)
ELEMENTS_NUM = len(ELEMENTS)
AURA_TAX = 0.8


# Assets
OPT_FONTS = ("ja-jp", "zh-cn")
OPT_LOCALIZATIONS = ("CHS", "CHT", "DE", "EN", "ES", "FR", "ID", "IT", "JP", "KR", "PT", "RU", "TH", "TR", "VI")
OPT_SOUNDS = ("bark")


# App
CAPTION = "Elemental Reactions Visualizer"
GAME_TIME_RESET_CAP = 100 # seconds


# Return code
OK = 100
FLIP_GAMETIME = 101


# Pygame
SCRW = 1280  # screen width
SCRH = 720  # screen height
FPS = 60  # frames per second
BGRC = (37, 37, 37)  # background color
ELMS = 80  # element icon size
MARGIN = 20 # margin around screen
GAUS = 60 # gauge button size
GTIS = 60 # gametime size
GAUB = (ELMS + GAUS) / 2 # gauge button border
GPAD = 120 # gauge buttons padding
GBHR = 0.75 # gauge button hitbox ratio
TXTC = (255, 255, 255)  # text color
TXTC_SELECTED = (247, 252, 88) # selected text color
TIME_LMUL = 5.3 # left border multiplier of gauge buttons padding
TIME_RMUL = 3.7 # right border multiplier of gauge buttons padding
