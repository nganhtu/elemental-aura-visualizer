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
            # TODO Electro-Charged
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
        logs = []
        original_decay_rate = decay_rate(element.gauge)
        reaction_occured = False

        for aura_type in SIMULTANEOUS_REACTION_PRIORITY[element.type]:
            for aura in self.auras:
                if aura_type == aura.type:
                    reaction_occured = True
                    element, aura, result_aura, log = react(element, aura)
                    if aura.gauge <= 0:
                        self.auras.remove(aura)
                    if result_aura is not None:
                        self.auras.append(result_aura)
                    if log is not None:
                        logs.append(log)
                    if element.gauge <= 0:
                        break
            if element.gauge <= 0:
                break
            # TODO react with freeze aura

        if not reaction_occured and element.gauge > 0 and element.type not in [ANEMO, GEO]:
            # Aura gauge extension
            cannot_find_the_same_aura = True
            for aura in self.auras:
                if element.type == aura.type:
                    if aura.gauge < AURA_TAX * element.gauge:
                        aura.gauge = AURA_TAX * element.gauge
                        logs.append(Log(LOG_EXTEND_AURA, aura.gauge))
                        # Pyro does not have decay rate inheritance
                        if element.type == PYRO:
                            aura.decay_rate = original_decay_rate
                    cannot_find_the_same_aura = False
                    break
            # Apply new aura
            if cannot_find_the_same_aura:
                new_aura = Aura(element.type, AURA_TAX * element.gauge, decay_rate(element.gauge))
                self.auras.append(new_aura)
                logs.append(Log(LOG_APPLY_AURA, new_aura.gauge))

        return logs
