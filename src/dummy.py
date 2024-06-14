from icecream import ic

from config import *
import pygame as pg


class Dummy():
    def __init__(self):
        self.auras = []

    def affectedBy(self, element, gauge):
        ic('dummy is affected by~', element, gauge)
