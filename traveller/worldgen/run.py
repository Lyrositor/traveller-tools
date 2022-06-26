from random import Random
from typing import Iterable

from traveller.utils import roll_d6, roll_2d6
from traveller.worldgen.models import Sector, Subsector, Hex, StarportQuality, TravelZone, Base, TradeCode

NUM_SUBSECTORS = 16
SECTOR_SIDE = 4
MIN_X = 0x1
MAX_X = 0x8
MIN_Y = 0x1
MAX_Y = 0xA

TEMPERATURE_ATMOSPHERE_DMS = {
    0: 0,
    1: 0,
    2: -2,
    3: -2,
    4: -1,
    5: -1,
    0xE: -1,
    6: 0,
    7: 0,
    8: 1,
    9: 1,
    0xA: 2,
    0xD: 2,
    0xF: 2,
    0xB: 6,
    0xC: 6
}
STARPORT_CLASSES = {
    2: StarportQuality.NONE,
    3: StarportQuality.FRONTIER,
    4: StarportQuality.FRONTIER,
    5: StarportQuality.POOR,
    6: StarportQuality.POOR,
    7: StarportQuality.ROUTINE,
    8: StarportQuality.ROUTINE,
    9: StarportQuality.GOOD,
    10: StarportQuality.GOOD,
    11: StarportQuality.EXCELLENT
}
BASES_DIFFICULITES_BY_STARPORT_QUALITY = {
    StarportQuality.EXCELLENT: {Base.MILITARY: 8, Base.NAVAL: 8, Base.SCOUT: 10},
    StarportQuality.GOOD: {Base.MILITARY: 8, Base.NAVAL: 8, Base.SCOUT: 9},
    StarportQuality.ROUTINE: {Base.MILITARY: 10, Base.SCOUT: 9},
    StarportQuality.POOR: {Base.SCOUT: 8, Base.CORSAIR: 12},
    StarportQuality.FRONTIER: {Base.CORSAIR: 10},
    StarportQuality.NONE: {Base.CORSAIR: 10},
}
TECH_LEVELS_STARPORT_DMS = {
    StarportQuality.EXCELLENT: 6,
    StarportQuality.GOOD: 4,
    StarportQuality.ROUTINE: 2,
    StarportQuality.NONE: -4
}


def run_worldgen(name: str, density_dm: int, r: Random) -> Sector:
    sector = Sector(name=name)
    for index in range(NUM_SUBSECTORS):
        sector.subsectors.append(generate_subsector(sector, index, density_dm, r))
    return sector


def generate_subsector(sector: Sector, index: int, density_dm: int, r: Random) -> Subsector:
    min_x = MIN_X + (index % SECTOR_SIDE) * MAX_X
    max_x = min_x + MAX_X
    min_y = MIN_Y + (index // SECTOR_SIDE) * MAX_Y
    max_y = min_y + MAX_Y
    subsector = Subsector(name=f"Subsector {index}", index=index)
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            world_occurrence = roll_d6(density_dm, r=r)
            if world_occurrence < 4:
                # No worlds here
                continue

            num_gas_giants = (12 - roll_2d6(r=r)) // 3
            size = roll_2d6(-2, r=r)
            atmosphere = roll_2d6(-7 + size, 0x0, 0xF, r=r)
            temperature = roll_2d6(TEMPERATURE_ATMOSPHERE_DMS[atmosphere], r=r)

            if size <= 1:
                hydrographics = 0
            else:
                atmosphere_dm = -4 if atmosphere <= 0x1 or atmosphere >= 0xA else atmosphere
                temperature_dm = 0
                if atmosphere not in (0xD, 0xF):
                    if 10 <= temperature <= 11:
                        temperature_dm = -2
                    elif 12 <= temperature:
                        temperature_dm = -6
                hydrographics = roll_2d6(-7 + atmosphere_dm + temperature_dm, 0x0, 0xA, r=r)

            population = roll_2d6(-2, r=r)

            if 8 <= population <= 9:
                starport_dm = 1
            elif population >= 10:
                starport_dm = 2
            elif 3 <= population <= 4:
                starport_dm = -1
            elif population <= 2:
                starport_dm = -2
            else:
                starport_dm = 0
            starport_quality = STARPORT_CLASSES[roll_2d6(starport_dm, 2, 11, r=r)]

            if population == 0:
                government = law = tech = 0
            else:
                government = roll_2d6(-7 + population, 0x0, 0xF, r=r)
                law = roll_2d6(-7 + government, 0x0, 0xF, r=r)
                tech = calculate_tech_level(
                    starport=starport_quality,
                    size=size,
                    atmosphere=atmosphere,
                    hydrographics=hydrographics,
                    population=population,
                    government=government,
                    r=r
                )

            bases = []
            for base, difficulty in BASES_DIFFICULITES_BY_STARPORT_QUALITY[starport_quality].items():
                dm = 0
                if base == Base.CORSAIR:
                    if law == 0:
                        dm += 2
                    elif law >= 2:
                        dm = -2
                if roll_2d6(dm, r=r) >= difficulty:
                    bases.append(base)

            zone = TravelZone.GREEN
            if atmosphere >= 0xA or government in (0x0, 0x7, 0xA) or law == 0x0 or law >= 0x9:
                zone = TravelZone.AMBER

            trade_codes = list(get_trade_codes(
                size=size,
                atmosphere=atmosphere,
                hydrographics=hydrographics,
                population=population,
                government=government,
                law=law,
                tech=tech
            ))

            sector.hexes.append(
                Hex(
                    x=x,
                    y=y,
                    name="???",
                    starport_quality=starport_quality,
                    size=size,
                    atmosphere=atmosphere,
                    hydrographics=hydrographics,
                    population=population,
                    government=government,
                    law=law,
                    tech=tech,
                    population_multiplier=1,
                    planetoid_belts=1,
                    gas_giants=num_gas_giants,
                    zone=zone,
                    bases=bases,
                    trade_codes=trade_codes,
                )
            )
    return subsector


def calculate_tech_level(
    starport: StarportQuality,
    size: int,
    atmosphere: int,
    hydrographics: int,
    population: int,
    government: int,
    r: Random
) -> int:
    dm = TECH_LEVELS_STARPORT_DMS.get(starport, 0)
    if size <= 0x1:
        dm += 2
    elif size <= 0x4:
        dm += 1
    if atmosphere <= 0x3 or atmosphere >= 0xA:
        dm += 1
    if hydrographics == 0x0 or hydrographics == 0x9:
        dm += 1
    elif hydrographics == 0xA:
        dm += 2
    if 1 <= population <= 5 or population == 8:
        dm += 1
    elif population == 0x9:
        dm += 2
    elif population == 0xA:
        dm += 4
    if government in (0x0, 0x5):
        dm += 1
    elif government == 0x7:
        dm += 2
    elif government in (0xD, 0xE):
        dm -= 2
    return roll_d6(dm, 0, r=r)


def get_trade_codes(
    size: int, atmosphere: int, hydrographics: int, population: int, government: int, law: int, tech: int
) -> Iterable[TradeCode]:
    if 0x4 <= atmosphere <= 0x9 and 0x4 <= hydrographics <= 0x8 and 0x5 <= population <= 0x7:
        yield TradeCode.AGRICULTURAL
    if size == 0x0 and atmosphere == 0x0 and hydrographics == 0x0:
        yield TradeCode.ASTEROID
    if population == 0x0 and government == 0x0 and law == 0x0:
        yield TradeCode.BARREN
    if 0x2 <= atmosphere <= 0x9 and hydrographics == 0x0:
        yield TradeCode.DESERT
    if 0xA <= atmosphere and 0x1 <= hydrographics:
        yield TradeCode.FLUID_OCEANS
    if 0x6 <= size <= 0x8 and atmosphere in (0x5, 0x6, 0x8) and 0x5 <= hydrographics <= 0x7:
        yield TradeCode.GARDEN
    if 0x9 <= population:
        yield TradeCode.HIGH_POPULATION
    if 0xC <= tech:
        yield TradeCode.HIGH_TECH
    if atmosphere <= 0x1 and 0x1 <= hydrographics:
        yield TradeCode.ICE_CAPPED
    if atmosphere in (0x0, 0x1, 0x2, 0x4, 0x7, 0x9, 0xA, 0xB, 0xC) and 0x9 <= population:
        yield TradeCode.INDUSTRIAL
    if 0x1 <= population <= 0x3:
        yield TradeCode.LOW_POPULATION
    if 0x1 <= population and tech <= 0x5:
        yield TradeCode.LOW_TECH
    if atmosphere <= 0x3 and hydrographics <= 0x3 and population >= 0x6:
        yield TradeCode.NON_AGRICULTURAL
    if 0x4 <= population <= 0x6:
        yield TradeCode.NON_INDUSTRIAL
    if 0x2 <= atmosphere <= 0x5 and hydrographics <= 0x3:
        yield TradeCode.POOR
    if atmosphere in (0x6, 0x8) and 0x6 <= population <= 0x8 and 0x4 <= government <= 0x9:
        yield TradeCode.RICH
    if atmosphere == 0x0:
        yield TradeCode.VACUUM
    if (0x3 <= atmosphere <= 0x9 or 0xD <= atmosphere) and 0xA <= hydrographics:
        yield TradeCode.WATERWORLD
