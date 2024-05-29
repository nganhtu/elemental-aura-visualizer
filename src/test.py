import os
import path
import pygame as pg
from icecream import ic

# print(os.listdir(path.ELEMENTS))

element_pngs = []
for file_name in os.listdir(path.ELEMENTS):
    element_pngs.append(pg.image.load(path.ELEMENTS + file_name))

ic(element_pngs)
