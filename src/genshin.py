# Every magic numbers in this file were discovered and standardized
# by most of Genshin Impact theorycrafting communities and players.

# References:
# https://library.keqingmains.com/combat-mechanics/elemental-effects/elemental-gauge-theory
# https://library.keqingmains.com/combat-mechanics/elemental-effects/transformative-reactions
# https://bbs.nga.cn/read.php?tid=24400590
# https://bbs.nga.cn/read.php?tid=33231790
# https://nga.178.com/read.php?tid=33235924&rand=343


from icecream import ic

from log import Log


ANEMO, CRYO, DENDRO, ELECTRO, GEO, HYDRO, PYRO = 0, 1, 2, 3, 4, 5, 6  # do not change
BURNING, FREEZE, QUICKEN = 10, 11, 12  # keep order when change
ELEMENTS = (ANEMO, CRYO, DENDRO, ELECTRO, GEO, HYDRO, PYRO)
AURAS = (ANEMO, CRYO, DENDRO, ELECTRO, GEO, HYDRO, PYRO, BURNING, FREEZE, QUICKEN)


AURA_TAX = 0.8
AVAILABLE_GAUGES = (1, 1.5, 2, 4, 8)  # U
MAX_AURA_GAUGE_AVAILABLE = max(AVAILABLE_GAUGES) * AURA_TAX
MAX_COEXIST_AURAS_AVAILABLE = 3
SIMULTANEOUS_REACTION_PRIORITY = {
    ANEMO: (ELECTRO, PYRO, BURNING, HYDRO, CRYO, FREEZE),
    CRYO: (ELECTRO, PYRO, ANEMO, HYDRO),
    DENDRO: (QUICKEN, ELECTRO, PYRO, HYDRO),
    ELECTRO: (QUICKEN, PYRO, BURNING, ANEMO, HYDRO, CRYO, FREEZE, DENDRO),
    GEO: (FREEZE, ELECTRO, PYRO, BURNING, HYDRO, CRYO),
    HYDRO: (PYRO, BURNING, ANEMO, CRYO, QUICKEN, DENDRO, ELECTRO),
    PYRO: (ELECTRO, ANEMO, HYDRO, FREEZE, CRYO, QUICKEN, DENDRO)
    # GEO: shattered, clear the Freeze Aura, and applies the attack's element afterwards
}
# BURNING: 2U, doesn't decay, reacted by HYDRO, ELECTRO, ANEMO, GEO at the same time with underlying PYRO aura
FREEZE_AURA_STARTING_DECAY_SPEED = 0.4  # U/s
FREEZE_AURA_DECAY_ACCELERATION_RATE = 0.1  # U/s^2
FREEZE_AURA_RESTORE_ACCELERATION_RATE = -0.2  # U/s^2
EC_GAUGE_DECAY = 0.4  # U
EC_TICK_ICD = 1  # s
EC_FINAL_TICK_ICD = 0.5  # s


def decay_rate(gauge):
    if gauge in AVAILABLE_GAUGES:
        return (2.5 * gauge + 7) / (AURA_TAX * gauge)
    else:
        # for debug purpose
        # still there should be nothing may apply a gauge out of AVAILABLE_GAUGES
        ic('gauge is not available!', gauge)
        return float('inf')


def quicken_decay_rate(quicken_gauge):
    return 5 * quicken_gauge + 6


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
        self.decay_speed = 1 / self.decay_rate
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


REACT_MULT = 100  # "bigger number" element's multiplicator


def get_reaction_notation(aura1, aura2):
    return aura1 * REACT_MULT + aura2 if aura1 > aura2 else aura2 * REACT_MULT + aura1


SPREAD = get_reaction_notation(QUICKEN, DENDRO)
AGGRAVATE = get_reaction_notation(QUICKEN, ELECTRO)
Q_BLOOM = get_reaction_notation(QUICKEN, HYDRO)
Q_BURNING = get_reaction_notation(QUICKEN, PYRO)
F_SWIRL = get_reaction_notation(FREEZE, ANEMO)
F_SUPERCONDUCT = get_reaction_notation(FREEZE, ELECTRO)
SHATTER = get_reaction_notation(FREEZE, GEO)
F_MELT = get_reaction_notation(FREEZE, PYRO)
B_SWIRL = get_reaction_notation(BURNING, ANEMO)
B_OVERLOADED = get_reaction_notation(BURNING, ELECTRO)
B_CRYSTALLIZE = get_reaction_notation(BURNING, GEO)
B_VAPORIZE = get_reaction_notation(BURNING, HYDRO)
P_SWIRL = get_reaction_notation(PYRO, ANEMO)
MELT = get_reaction_notation(PYRO, CRYO)
REACTION_BURNING = get_reaction_notation(PYRO, DENDRO)
OVERLOADED = get_reaction_notation(PYRO, ELECTRO)
P_CRYSTALLIZE = get_reaction_notation(PYRO, GEO)
VAPORIZE = get_reaction_notation(PYRO, HYDRO)
H_SWIRL = get_reaction_notation(HYDRO, ANEMO)
REACTION_FROZEN = get_reaction_notation(HYDRO, CRYO)
BLOOM = get_reaction_notation(HYDRO, DENDRO)
ELECTRO_CHARGED = get_reaction_notation(HYDRO, ELECTRO)
H_CRYSTALLIZE = get_reaction_notation(HYDRO, GEO)
C_CRYSTALLIZE = get_reaction_notation(GEO, CRYO)
E_CRYSTALLIZE = get_reaction_notation(GEO, ELECTRO)
E_SWIRL = get_reaction_notation(ELECTRO, ANEMO)
SUPERCONDUCT = get_reaction_notation(ELECTRO, CRYO)
REACTION_QUICKEN = get_reaction_notation(ELECTRO, DENDRO)
C_SWIRL = get_reaction_notation(CRYO, ANEMO)
ELEMENTAL_REACTIONS = (SPREAD, AGGRAVATE, Q_BLOOM, Q_BURNING, F_SWIRL, F_SUPERCONDUCT, SHATTER,
                       F_MELT, B_SWIRL, B_OVERLOADED, B_CRYSTALLIZE, B_VAPORIZE, P_SWIRL, MELT,
                       REACTION_BURNING, OVERLOADED, P_CRYSTALLIZE, VAPORIZE, H_SWIRL,
                       REACTION_FROZEN, BLOOM, ELECTRO_CHARGED, H_CRYSTALLIZE, C_CRYSTALLIZE,
                       E_CRYSTALLIZE, E_SWIRL, SUPERCONDUCT, REACTION_QUICKEN, C_SWIRL)
POST_REACT_AURA_APPLIABLE_REACTIONS = (ELECTRO_CHARGED, SPREAD, AGGRAVATE)


# The following constants should have opposite sign to the above
LOG_CODES_COUNTER = 11
LOG_CODES = (-i - 1 for i in range(LOG_CODES_COUNTER))
LOG_EXTEND_AURA, LOG_APPLY_AURA, LOG_SWIRL, LOG_CRYSTALLIZE, LOG_MELT, LOG_OVERLOADED, LOG_VAPORIZE, \
LOG_BLOOM, LOG_SUPERCONDUCT, LOG_ELECTRO_CHARGED, LOG_QUICKEN = LOG_CODES


def react(element, aura):
    reaction = get_reaction_notation(element.type, aura.type)
    # 6
    if reaction in [F_SWIRL, B_SWIRL, P_SWIRL, H_SWIRL, E_SWIRL, C_SWIRL]:
        return swirl(element, aura)
    # 1
    if reaction in [B_CRYSTALLIZE, P_CRYSTALLIZE, H_CRYSTALLIZE, C_CRYSTALLIZE, E_CRYSTALLIZE]:
        return crystallize(element, aura)
    # 1
    if reaction == MELT:
        return melt(element, aura)
    # 1
    if reaction == OVERLOADED:
        return overloaded(element, aura)
    # 1
    if reaction == VAPORIZE:
        return vaporize(element, aura)
    # 1
    if reaction == BLOOM:
        return bloom(element, aura)
    # 1
    if reaction == SUPERCONDUCT:
        return superconduct(element, aura)
    if reaction == REACTION_QUICKEN:
        return quicken(element, aura)

    return element, aura, None, None


def swirl(element, aura):
    if element.type == ANEMO:
        anemo = element
        another = aura
    else:
        anemo = aura
        another = element
    react_gauge = min(anemo.gauge / 2, another.gauge)
    anemo.gauge -= react_gauge * 2
    another.gauge -= react_gauge
    return element, aura, None, Log(LOG_SWIRL, react_gauge)


def crystallize(element, aura):
    if element.type == GEO:
        geo = element
        another = aura
    else:
        geo = aura
        another = element
    react_gauge = min(geo.gauge / 2, another.gauge)
    geo.gauge -= react_gauge * 2
    another.gauge -= react_gauge
    return element, aura, None, Log(LOG_CRYSTALLIZE, react_gauge)


def melt(element, aura):
    if element.type == CRYO:
        cryo = element
        pyro = aura
    else:
        cryo = aura
        pyro = element
    react_gauge = min(cryo.gauge / 2, pyro.gauge)
    cryo.gauge -= react_gauge * 2
    pyro.gauge -= react_gauge
    return element, aura, None, Log(LOG_MELT, react_gauge)


def overloaded(element, aura):
    react_gauge = min(element.gauge, aura.gauge)
    element.gauge -= react_gauge
    aura.gauge -= react_gauge
    return element, aura, None, Log(LOG_OVERLOADED, react_gauge)


def vaporize(element, aura):
    if element.type == PYRO:
        pyro = element
        hydro = aura
    else:
        pyro = aura
        hydro = element
    react_gauge = min(pyro.gauge / 2, hydro.gauge)
    pyro.gauge -= react_gauge * 2
    hydro.gauge -= react_gauge
    return element, aura, None, Log(LOG_VAPORIZE, react_gauge)


def bloom(element, aura):
    if element.type == HYDRO:
        hydro = element
        dendro = aura
    else:
        hydro = aura
        dendro = element
    react_gauge = min(hydro.gauge / 2, dendro.gauge)
    hydro.gauge -= react_gauge * 2
    dendro.gauge -= react_gauge
    return element, aura, None, Log(LOG_BLOOM, react_gauge)


def superconduct(element, aura):
    react_gauge = min(element.gauge, aura.gauge)
    element.gauge -= react_gauge
    aura.gauge -= react_gauge
    return element, aura, None, Log(LOG_SUPERCONDUCT, react_gauge)


def electro_charged_tick(electro, hydro):
    react_gauge = min(electro.gauge, hydro.gauge, EC_GAUGE_DECAY)
    electro.gauge -= react_gauge
    hydro.gauge -= react_gauge
    return Log(LOG_ELECTRO_CHARGED, react_gauge)


def quicken(element, aura):
    react_gauge = min(element.gauge, aura.gauge)
    element.gauge -= react_gauge
    aura.gauge -= react_gauge
    quicken_aura = Aura(QUICKEN, react_gauge, quicken_decay_rate(react_gauge))
    return element, aura, quicken_aura, Log(LOG_QUICKEN, react_gauge)
