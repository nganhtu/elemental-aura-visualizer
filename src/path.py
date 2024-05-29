from icecream import ic

import os
from config import *


ROOT = f"{os.path.dirname(os.path.abspath(__file__))}/../"


ASSETS = f"{ROOT}assets/"


FONTS = f"{ASSETS}fonts/"

FONT = {lang: f"{FONTS}{lang}.ttf" for lang in OPT_FONTS}

IMAGES = f"{ASSETS}images/"

ELEMENTS = f"{IMAGES}elements/"
FAVICON = f"{IMAGES}favicon.png"


LOCALIZATIONS = f"{ASSETS}localization/"

LOCALIZATION = {lang: f"{LOCALIZATIONS}TextMap{lang}.json" for lang in OPT_LOCALIZATIONS}


SOUNDS = f"{ASSETS}sounds/"

SOUND = {sound: f"{SOUNDS}{sound}.wav" for sound in OPT_SOUNDS}
