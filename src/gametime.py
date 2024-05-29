from icecream import ic

from config import *


class Gametime():
    def __init__(self, clock_starting_time = 0, starting_state_is_paused = False):
        self.clock = clock_starting_time
        self.paused = starting_state_is_paused

    def update(self, dt):
        if not self.paused:
            self.clock = (self.clock + dt) % GAME_TIME_RESET_CAP
