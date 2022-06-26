from dataclasses import dataclass

from traveller.worldgen.models import TradeCode


@dataclass
class TradeGood:
    id: int
    name: str
    purchase_dms: dict[TradeCode, int]
    sale_dms: dict[TradeCode, int]


TRADE_GOODS = {
    11: TradeGood(
        id=11,
        name="Common Electronics",
        purchase_dms={TradeCode.INDUSTRIAL: 2, TradeCode.HIGH_TECH: 3, TradeCode.RICH: 1},
        sale_dms={TradeCode.NON_INDUSTRIAL: 2, TradeCode.LOW_TECH: 1, TradeCode.POOR: 1},
    ),
    12: TradeGood(
        id=12,
        name="Common Industrial Goods",
        purchase_dms={TradeCode.NON_AGRICULTURAL: 2, TradeCode.INDUSTRIAL: 5},
        sale_dms={TradeCode.NON_INDUSTRIAL: 3, TradeCode.AGRICULTURAL: 2},
    ),
    13: TradeGood(
        id=13,
        name="Common Manufactured Goods",
        purchase_dms={TradeCode.NON_AGRICULTURAL: 2, TradeCode.INDUSTRIAL: 5},
        sale_dms={TradeCode.NON_INDUSTRIAL: 3, TradeCode.HIGH_POPULATION: 2},
    ),
    14: TradeGood(
        id=14,
        name="Common Raw Materials",
        purchase_dms={TradeCode.AGRICULTURAL: 3, TradeCode.GARDEN: 2},
        sale_dms={TradeCode.INDUSTRIAL: 2, TradeCode.POOR: 2},
    ),
    15: TradeGood(
        id=15,
        name="Common Consumables",
        purchase_dms={TradeCode.AGRICULTURAL: 3, TradeCode.WATERWORLD: 2, TradeCode.GARDEN: 1, TradeCode.ASTEROID: -4},
        sale_dms={TradeCode.ASTEROID: 1, TradeCode.FLUID_OCEANS: 1, TradeCode.ICE_CAPPED: 1, TradeCode.HIGH_POPULATION: 1},
    ),
    16: TradeGood(
        id=16,
        name="Common Ore",
        purchase_dms={TradeCode.ASTEROID: 4},
        sale_dms={TradeCode.INDUSTRIAL: 3, TradeCode.NON_INDUSTRIAL: 1},
    ),
    21: TradeGood(
        id=21,
        name="Advanced Electronics",
        purchase_dms={TradeCode.INDUSTRIAL: 2, TradeCode.HIGH_TECH: 3},
        sale_dms={TradeCode.NON_INDUSTRIAL: 1, TradeCode.RICH: 2, TradeCode.ASTEROID: 3},
    ),
    22: TradeGood(
        id=22,
        name="Advanced Machine Parts",
        purchase_dms={TradeCode.INDUSTRIAL: 2, TradeCode.HIGH_TECH: 1},
        sale_dms={TradeCode.ASTEROID: 2, TradeCode.NON_INDUSTRIAL: 1},
    ),
    23: TradeGood(
        id=23,
        name="Advanced Manufactured Goods",
        purchase_dms={TradeCode.INDUSTRIAL: 1},
        sale_dms={TradeCode.HIGH_POPULATION: 1, TradeCode.RICH: 2},
    ),
    24: TradeGood(
        id=24,
        name="Advanced Weapons",
        purchase_dms={TradeCode.HIGH_TECH: 2},
        sale_dms={TradeCode.POOR: 1},
    ),
    25: TradeGood(
        id=25,
        name="Advanced Vehicles",
        purchase_dms={TradeCode.HIGH_TECH: 2},
        sale_dms={TradeCode.ASTEROID: 2, TradeCode.RICH: 2},
    ),
    26: TradeGood(
        id=26,
        name="Biochemicals",
        purchase_dms={TradeCode.AGRICULTURAL: 1, TradeCode.WATERWORLD: 2},
        sale_dms={TradeCode.INDUSTRIAL: 2},
    ),
    31: TradeGood(
        id=31,
        name="Crystals & Gems",
        purchase_dms={TradeCode.ASTEROID: 2, TradeCode.DESERT: 1, TradeCode.ICE_CAPPED: 1},
        sale_dms={TradeCode.INDUSTRIAL: 3, TradeCode.RICH: 2},
    ),
    32: TradeGood(
        id=32,
        name="Cybernetics",
        purchase_dms={TradeCode.HIGH_TECH: 1},
        sale_dms={TradeCode.ASTEROID: 1, TradeCode.ICE_CAPPED: 1, TradeCode.RICH: 2},
    ),
    33: TradeGood(
        id=33,
        name="Live Animals",
        purchase_dms={TradeCode.AGRICULTURAL: 2},
        sale_dms={TradeCode.LOW_POPULATION: 3},
    ),
    34: TradeGood(
        id=34,
        name="Luxury Consumables",
        purchase_dms={TradeCode.AGRICULTURAL: 2, TradeCode.WATERWORLD: 1},
        sale_dms={TradeCode.RICH: 2, TradeCode.HIGH_POPULATION: 2},
    ),
    35: TradeGood(
        id=35,
        name="Luxury Goods",
        purchase_dms={TradeCode.HIGH_POPULATION: 1},
        sale_dms={TradeCode.RICH: 4},
    ),
    36: TradeGood(
        id=36,
        name="Medical Supplies",
        purchase_dms={TradeCode.HIGH_TECH: 2},
        sale_dms={TradeCode.INDUSTRIAL: 2, TradeCode.POOR: 1, TradeCode.RICH: 1},
    ),
    41: TradeGood(
        id=41,
        name="Petrochemicals",
        purchase_dms={TradeCode.DESERT: 2},
        sale_dms={TradeCode.INDUSTRIAL: 2, TradeCode.AGRICULTURAL: 1, TradeCode.LOW_TECH: 2},
    ),
    42: TradeGood(
        id=42,
        name="Pharmaceuticals",
        purchase_dms={TradeCode.ASTEROID: 2, TradeCode.HIGH_POPULATION: 1},
        sale_dms={TradeCode.RICH: 2, TradeCode.LOW_TECH: 1},
    ),
    43: TradeGood(
        id=43,
        name="Polymers",
        purchase_dms={TradeCode.INDUSTRIAL: 1},
        sale_dms={TradeCode.RICH: 2, TradeCode.NON_INDUSTRIAL: 1},
    ),
    44: TradeGood(
        id=44,
        name="Precious Metals",
        purchase_dms={TradeCode.ASTEROID: 3, TradeCode.DESERT: 1, TradeCode.ICE_CAPPED: 2},
        sale_dms={TradeCode.RICH: 3, TradeCode.INDUSTRIAL: 2, TradeCode.HIGH_TECH: 1},
    ),
    45: TradeGood(
        id=45,
        name="Radioactives",
        purchase_dms={TradeCode.ASTEROID: 2, TradeCode.LOW_POPULATION: 2},
        sale_dms={TradeCode.INDUSTRIAL: 3, TradeCode.HIGH_TECH: 1, TradeCode.NON_INDUSTRIAL: -2, TradeCode.AGRICULTURAL: -3},
    ),
    46: TradeGood(
        id=46,
        name="Robots",
        purchase_dms={TradeCode.INDUSTRIAL: 1},
        sale_dms={TradeCode.AGRICULTURAL: 2, TradeCode.HIGH_TECH: 1},
    ),
    51: TradeGood(
        id=51,
        name="Spices",
        purchase_dms={TradeCode.DESERT: 2},
        sale_dms={TradeCode.HIGH_POPULATION: 2, TradeCode.RICH: 3, TradeCode.POOR: 3},
    ),
    52: TradeGood(
        id=52,
        name="Textiles",
        purchase_dms={TradeCode.AGRICULTURAL: 7},
        sale_dms={TradeCode.HIGH_POPULATION: 3, TradeCode.NON_AGRICULTURAL: 2},
    ),
    53: TradeGood(
        id=53,
        name="Uncommon Ore",
        purchase_dms={TradeCode.ASTEROID: 4},
        sale_dms={TradeCode.INDUSTRIAL: 3, TradeCode.NON_INDUSTRIAL: 1},
    ),
    54: TradeGood(
        id=54,
        name="Uncommon Raw Materials",
        purchase_dms={TradeCode.AGRICULTURAL: 2, TradeCode.WATERWORLD: 1},
        sale_dms={TradeCode.INDUSTRIAL: 2, TradeCode.HIGH_TECH: 1},
    ),
    55: TradeGood(
        id=55,
        name="Wood",
        purchase_dms={TradeCode.AGRICULTURAL: 6},
        sale_dms={TradeCode.RICH: 2, TradeCode.INDUSTRIAL: 1},
    ),
    56: TradeGood(
        id=56,
        name="Vehicles",
        purchase_dms={TradeCode.INDUSTRIAL: 2, TradeCode.HIGH_TECH: 1},
        sale_dms={TradeCode.NON_INDUSTRIAL: 2, TradeCode.HIGH_POPULATION: 1},
    ),
    61: TradeGood(
        id=61,
        name="Illegal Biochemicals",
        purchase_dms={TradeCode.WATERWORLD: 2},
        sale_dms={TradeCode.INDUSTRIAL: 6},
    ),
    62: TradeGood(
        id=62,
        name="Cybernetics, Illegal",
        purchase_dms={TradeCode.HIGH_TECH: 1},
        sale_dms={TradeCode.ASTEROID: 4, TradeCode.ICE_CAPPED: 4, TradeCode.RICH: 8},
    ),
    63: TradeGood(
        id=63,
        name="Drugs, Illegal",
        purchase_dms={TradeCode.ASTEROID: 1, TradeCode.DESERT: 1, TradeCode.GARDEN: 1, TradeCode.WATERWORLD: 1},
        sale_dms={TradeCode.RICH: 6, TradeCode.HIGH_POPULATION: 6},
    ),
    64: TradeGood(
        id=64,
        name="Luxuries, Illegal",
        purchase_dms={TradeCode.AGRICULTURAL: 2, TradeCode.WATERWORLD: 1},
        sale_dms={TradeCode.RICH: 6, TradeCode.HIGH_POPULATION: 4},
    ),
    65: TradeGood(
        id=65,
        name="Weapons, Illegal",
        purchase_dms={TradeCode.HIGH_TECH: 2},
        sale_dms={TradeCode.POOR: 6},
    ),
}
