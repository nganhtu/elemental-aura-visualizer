from icecream import ic

from config import *


class Dummy:
    def __init__(self):
        self.time = 0
        self.auras = []
        self.freeze_aura = None
        self.freeze_aura_decay_speed = FREEZE_AURA_STARTING_DECAY_SPEED

    def is_frozen(self):
        return self.freeze_aura is not None

    def update_freeze_decay_speed(self, dt):
        if self.is_frozen():
            self.freeze_aura_decay_speed = self.freeze_aura.decay_speed
        else:
            if self.freeze_aura_decay_speed > FREEZE_AURA_STARTING_DECAY_SPEED:
                self.freeze_aura_decay_speed += FREEZE_AURA_RESTORE_ACCELERATION_RATE * dt  # < 0
            if self.freeze_aura_decay_speed < FREEZE_AURA_STARTING_DECAY_SPEED:
                self.freeze_aura_decay_speed = FREEZE_AURA_STARTING_DECAY_SPEED

    def update(self, dt):
        for aura in self.auras:
            aura.update(dt)
            if aura.gauge == 0:
                ic('aura will be removed~')
                self.auras.remove(aura)
        if self.is_frozen():
            self.freeze_aura.update(dt)
            if self.freeze_aura.gauge == 0:
                ic('freeze aura will be removed~')
                self.freeze_aura = None
        self.update_freeze_decay_speed(dt)

    def affected_by(self, element):
        for aura in SRP[element.type]:
            if aura in self.auras:
                # react(element, aura)
                if element.gauge <= 0:
                    break
            # TODO react with freeze aura
            # TODO extend same type aura that already exist
        if element.gauge > 0:
            new_aura = Aura(element.type, AURA_TAX * element.gauge, decay_rate(element.gauge))
            self.auras.append(new_aura)
