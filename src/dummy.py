from icecream import ic

from config import *


class Dummy:
    def __init__(self):
        self.time = 0
        self.auras = []
        self.freeze_aura = None
        self.freeze_aura_decay_speed = FREEZE_AURA_STARTING_DECAY_SPEED
        self.is_electro_charged = False
        self.last_ec_tick_timestamp = None

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

    def electro_charged_occur(self, happen_time):
        electro = None
        hydro = None
        for aura in self.auras:
            if aura.type == ELECTRO:
                electro = aura
            elif aura.type == HYDRO:
                hydro = aura
        if electro is not None and hydro is not None:
            log = electro_charged_tick(electro, hydro)
        else:  # EC final tick
            log = Log(LOG_ELECTRO_CHARGED, 0)
        self.last_ec_tick_timestamp = happen_time
        log.happen_time = happen_time
        return log

    def electro_charged_update(self):
        log = None
        aura_types = [aura.type for aura in self.auras]
        if ELECTRO not in aura_types or HYDRO not in aura_types:
            if self.is_electro_charged:
                if self.time - self.last_ec_tick_timestamp >= EC_FINAL_TICK_ICD:
                    log = self.electro_charged_occur(self.time)
                self.is_electro_charged = False
            return log
        # new EC occurred should ignore EC_FINAL_TICK_ICD
        if not self.is_electro_charged:
            log = self.electro_charged_occur(self.time)
        else:
            internal_time = self.time - self.last_ec_tick_timestamp
            if internal_time >= EC_TICK_ICD:
                log = self.electro_charged_occur(self.last_ec_tick_timestamp + EC_TICK_ICD)
        self.is_electro_charged = True
        return log

    def update(self, gametime_clock, dt):
        logs = []
        self.time = gametime_clock
        log = self.electro_charged_update()
        if log is not None:
            logs.append(log)
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
        return logs

    def affected_by(self, element):
        logs = []
        original_decay_rate = decay_rate(element.gauge)
        can_apply_element = True

        for aura_type in SIMULTANEOUS_REACTION_PRIORITY[element.type]:
            for aura in self.auras:
                if aura.type == aura_type:
                    reaction_notation = get_reaction_notation(element.type, aura.type)
                    if reaction_notation not in POST_REACT_AURA_APPLICABLE_REACTIONS:
                        can_apply_element = False
                    element, aura, result_aura, log = react(element, aura)
                    if aura.gauge <= 0:
                        self.auras.remove(aura)
                    if result_aura is not None:
                        # TODO check with Freeze and Burning situations
                        # Quicken evidences : https://youtu.be/Hjf08ZHavgA, https://youtu.be/bKN0e0w-O0g
                        # Assume that Quicken aura extension worked the same way as Pyro; cannot confirm yet
                        old_aura_found = False
                        for old_aura in self.auras:
                            if not old_aura_found and old_aura.type == result_aura.type:
                                old_aura_found = True
                                if old_aura.gauge < result_aura.gauge:
                                    self.auras.remove(old_aura)
                                    self.auras.append(result_aura)
                        if not old_aura_found:
                            self.auras.append(result_aura)
                    if log is not None:
                        logs.append(log)
                    if element.gauge <= 0:
                        break
            if element.gauge <= 0:
                break
            # TODO react with freeze aura

        if can_apply_element and element.gauge > 0 and element.type not in [ANEMO, GEO]:
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

        for log in logs:
            log.happen_time = self.time
        return logs
