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
        original_decay_rate = decay_rate(element.gauge)

        for aura_type in SRP[element.type]:
            for aura in self.auras:
                if aura_type == aura.type:
                    # (element, aura, new_aura) = react(element, aura)
                    if element.gauge <= 0:
                        break
                # TODO react with freeze aura
            if element.gauge < 0:
                break

        if element.gauge > 0:
            # Aura gauge extension
            cannot_find_the_same_aura = True
            for aura in self.auras:
                if element.type == aura.type:
                    # Pyro does not have decay rate inheritance
                    if element.type == PYRO and AURA_TAX * element.gauge > aura.gauge:
                        aura.decay_rate = original_decay_rate
                    aura.gauge = max(aura.gauge, AURA_TAX * element.gauge)
                    cannot_find_the_same_aura = False
                    break
            # Apply new aura
            if cannot_find_the_same_aura:
                new_aura = Aura(element.type, AURA_TAX * element.gauge, decay_rate(element.gauge))
                self.auras.append(new_aura)
