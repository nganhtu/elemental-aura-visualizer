from icecream import ic

from config import *
from genshin import *


class Dummy():
    def __init__(self):
        self.time = 0
        self.auras = []
        self.freeze_aura = None
        self.freeze_aura_decay_speed = FREEZE_AURA_STARTING_DECAY_SPEED

    def isFrozen(self):
        return self.freeze_aura is not None

    def update_freeze_params(self, dt):
        if self.isFrozen():
            self.freeze_aura_decay_speed = self.freeze_aura.decay_speed
        else:
            if self.freeze_aura_decay_speed > FREEZE_AURA_STARTING_DECAY_SPEED:
                self.freeze_aura_decay_speed += FREEZE_AURA_RESTORE_ACCELERATION_RATE * dt # < 0
            if self.freeze_aura_decay_speed < FREEZE_AURA_STARTING_DECAY_SPEED:
                self.freeze_aura_decay_speed = FREEZE_AURA_STARTING_DECAY_SPEED

    def affectedBy(self, element, gauge):
        ic('dummy is affected by~', element, gauge)
