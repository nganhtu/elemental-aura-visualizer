# Every magic numbers in this file were discovered and standardized
# by most of Genshin Impact theorycrafting communities and players.

# References:
# https://library.keqingmains.com/combat-mechanics/elemental-effects/elemental-gauge-theory
# https://library.keqingmains.com/combat-mechanics/elemental-effects/transformative-reactions
# https://bbs.nga.cn/read.php?tid=24400590
# https://bbs.nga.cn/read.php?tid=33231790
# https://nga.178.com/read.php?tid=33235924&rand=343


from icecream import ic


ANEMO, CRYO, DENDRO, ELECTRO, GEO, HYDRO, PYRO = 0, 1, 2, 3, 4, 5, 6  # do not change
BURNING, FREEZE, QUICKEN = 10, 11, 12
ELEMENTS = (ANEMO, CRYO, DENDRO, ELECTRO, GEO, HYDRO, PYRO)
AURAS = (ANEMO, CRYO, DENDRO, ELECTRO, GEO, HYDRO, PYRO, BURNING, FREEZE, QUICKEN)


AURA_TAX = 0.8
AVAILABLE_GAUGES = (1, 1.5, 2, 4, 8)
MAX_AURA_GAUGE_AVAILABLE = 6.4
MAX_COEXIST_AURAS_AVAILABLE = 3
SRP = {
    PYRO: (ELECTRO, ANEMO, HYDRO, FREEZE, CRYO, QUICKEN, DENDRO),
    HYDRO: (PYRO, BURNING, ANEMO, CRYO, QUICKEN, DENDRO, ELECTRO),
    DENDRO: (QUICKEN, ELECTRO, PYRO, HYDRO),
    ELECTRO: (QUICKEN, PYRO, BURNING, ANEMO, HYDRO, CRYO, FREEZE, DENDRO),
    CRYO: (ELECTRO, PYRO, ANEMO, HYDRO),
    ANEMO: (ELECTRO, PYRO, BURNING, HYDRO, CRYO, FREEZE),
    GEO: (FREEZE, ELECTRO, PYRO, BURNING, HYDRO, CRYO)
    # GEO: shattered, clear the Freeze Aura, and applies the attack's element afterwards
}
# BURNING: 2U, doesn't decay, reacted by HYDRO, ELECTRO, ANEMO, GEO at the same time with underlying PYRO aura
FREEZE_AURA_STARTING_DECAY_SPEED = 0.4  # U/s
FREEZE_AURA_DECAY_ACCELERATION_RATE = 0.1  # U/s^2
FREEZE_AURA_RESTORE_ACCELERATION_RATE = -0.2  # U/s^2


def decay_rate(gauge):
    if gauge in AVAILABLE_GAUGES:
        return (2.5 * gauge + 7) / (AURA_TAX * gauge)
    else:
        ic('gauge is not available!', gauge)
        return float('inf')


class Element:
    def __init__(self, type, gauge):
        self.type = type
        self.gauge = gauge


class Aura(Element):
    def __init__(self, type, gauge, decay_rate):
        super().__init__(type, gauge)
        self.decay_rate = decay_rate
        self.decay_speed = 1 / self.decay_rate

    def update(self, dt):
        if self.gauge > 0:
            self.gauge -= self.decay_speed * dt
        if self.gauge < 0:
            self.gauge = 0


class FreezeAura(Element):
    def __init__(self, gauge, starting_decay_speed):
        super().__init__(FREEZE, gauge)
        self.decay_rate = 1 / starting_decay_speed
        self.decay_speed = starting_decay_speed

    def update(self, dt):
        if self.gauge > 0:
            self.decay_speed += FREEZE_AURA_DECAY_ACCELERATION_RATE * dt
            self.gauge -= self.decay_speed * dt
            self.decay_rate = 1 / self.decay_speed
        if self.gauge < 0:
            self.gauge = 0
