from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from xml.etree.ElementTree import ElementTree, Element, SubElement

from traveller.utils import e_hex, subsector_code, to_coords

T5_COLUMN_DELIMITED_FORMAT_ORDER = (
    "Hex", "Name", "UWP", "Remarks", "{Ix}", "(Ex)", "[Cx]", "N", "B", "Z", "PBG", "W", "A", "Stellar"
)


class StarportQuality(str, Enum):
    EXCELLENT = "A"
    GOOD = "B"
    ROUTINE = "C"
    POOR = "D"
    FRONTIER = "E"
    NONE = "X"


class Base(str, Enum):
    CORSAIR = "C"
    DEPOT = "D"
    MILITARY = "M"
    NAVAL = "N"
    SCOUT = "S"
    WAY_STATION = "W"


class RouteType(str, Enum):
    TRADE = "trade"


class TradeCode(str, Enum):
    AGRICULTURAL = "Ag"
    ASTEROID = "As"
    BARREN = "Ba"
    DESERT = "De"
    FLUID_OCEANS = "Fl"
    GARDEN = "Ga"
    HIGH_POPULATION = "Hi"
    HIGH_TECH = "Ht"
    ICE_CAPPED = "Ic"
    INDUSTRIAL = "In"
    LOW_POPULATION = "Lo"
    LOW_TECH = "Lt"
    NON_AGRICULTURAL = "Na"
    NON_INDUSTRIAL = "Ni"
    POOR = "Po"
    RICH = "Ri"
    VACUUM = "Va"
    WATERWORLD = "Wa"


class TravelZone(str, Enum):
    AMBER = "A"
    GREEN = "-"
    RED = "R"


STARPORT_QUALITY_LABELS = {
    StarportQuality.EXCELLENT: "Excellent",
    StarportQuality.GOOD: "Good",
    StarportQuality.ROUTINE: "Routine",
    StarportQuality.POOR: "Poor",
    StarportQuality.FRONTIER: "Frontier",
    StarportQuality.NONE: "None",
}

SIZE_LABELS = {
    0x0: "Less than 1000km (e.g. asteroid, orbital complex)",
    0x1: "1,600km (e.g. Triton)",
    0x2: "3,200km (e.g. Luna, Europa)",
    0x3: "4,800km (e.g. Mercury, Ganymede)",
    0x4: "6,400km (e.g. Mars)",
    0x5: "8,000km",
    0x6: "9,600km",
    0x7: "11,200km",
    0x8: "12,800km (e.g. Earth)",
    0x9: "14,400km",
    0xA: "16,000km",
}

ATMOSPHERE_LABELS = {
    0x0: "None",
    0x1: "Trace",
    0x2: "Very Thin, Tainted",
    0x3: "Very Thin",
    0x4: "Thin, Tainted",
    0x5: "Thin",
    0x6: "Standard",
    0x7: "Standard, Tainted",
    0x8: "Dense",
    0x9: "Dense, tainted",
    0xA: "Exotic",
    0xB: "Corrosive",
    0xC: "Insidious",
    0xD: "Very Dense",
    0xE: "Low",
    0xF: "unusual",
}

HYDROGRAPHICS_LABELS = {
    0x0: "Desert world",
    0x1: "Dry world",
    0x2: "A few small seas",
    0x3: "Small seas and oceans",
    0x4: "Wet world",
    0x5: "A large ocean",
    0x6: "Large oceans",
    0x7: "Earth-like world",
    0x8: "Only a few islands and archipelagos",
    0x9: "Almost entirely water",
    0xA: "Waterworld",
}

GOVERNMENT_LABELS = {
    0x0: "None",
    0x1: "Company/Corporation",
    0x2: "Participating Democracy",
    0x3: "Self-Perpetuating Democracy",
    0x4: "Representative Democracy",
    0x5: "Feudal Technocracy",
    0x6: "Captive Government",
    0x7: "Balkanisation",
    0x8: "Civil Service Bureaucracy",
    0x9: "Impersonal Bureaucracy",
    0xA: "Charismatic Dictator",
    0xB: "Non-Charismatic Leader",
    0xC: "Charismatic Oligarchy",
    0xD: "Religious Dictatorship",
    0xE: "Religious Autocracy",
    0xF: "Totalitarian Oligarchy",
}

BASE_LABELS = {
    Base.CORSAIR: "Corsair Base",
    Base.DEPOT: "Depot",
    Base.MILITARY: "Military Base",
    Base.NAVAL: "Naval",
    Base.SCOUT: "Scout",
    Base.WAY_STATION: "Way Station",
}

TRADE_CODE_LABELS = {
    TradeCode.AGRICULTURAL: "Agricultural",
    TradeCode.ASTEROID: "Asteroid",
    TradeCode.BARREN: "Barren",
    TradeCode.DESERT: "Desert",
    TradeCode.FLUID_OCEANS: "Fluid Oceans",
    TradeCode.GARDEN: "Garden",
    TradeCode.HIGH_POPULATION: "High Population",
    TradeCode.HIGH_TECH: "High Tech",
    TradeCode.ICE_CAPPED: "Ice-Capped",
    TradeCode.INDUSTRIAL: "Industrial",
    TradeCode.LOW_POPULATION: "Low Population",
    TradeCode.LOW_TECH: "Low Tech",
    TradeCode.NON_AGRICULTURAL: "Non-Agricultural",
    TradeCode.NON_INDUSTRIAL: "Non-Industrial",
    TradeCode.POOR: "Poor",
    TradeCode.RICH: "Rich",
    TradeCode.VACUUM: "Vacuum",
    TradeCode.WATERWORLD: "Waterworld",
}


@dataclass
class Hex:
    # Position
    x: int
    y: int

    # Name
    name: str = "???"

    # UWP
    starport_quality: StarportQuality = StarportQuality.ROUTINE
    size: int = 0
    atmosphere: int = 0
    hydrographics: int = 0
    population: int = 0
    government: int = 0
    law: int = 0
    tech: int = 0

    # PBG
    population_multiplier: int = 1
    planetoid_belts: int = 0
    gas_giants: int = 0

    allegiance: Optional[str] = None
    zone: TravelZone = TravelZone.GREEN

    bases: list[Base] = field(default_factory=list)
    trade_codes: list[TradeCode] = field(default_factory=list)

    @property
    def coords(self) -> str:
        return to_coords(self.x, self.y)

    @property
    def uwp(self) -> str:
        return (
            f"{self.starport_quality.value}{e_hex(self.size)}{e_hex(self.atmosphere)}{e_hex(self.hydrographics)}"
            f"{e_hex(self.population)}{e_hex(self.government)}{e_hex(self.law)}-{e_hex(self.tech)}"
        )

    @property
    def base_codes(self) -> str:
        return "".join(sorted(v.value for v in self.bases))

    @property
    def uwp_extended(self) -> str:
        base_codes = f" {self.base_codes}" if self.bases else ""
        trade_codes = f" {' '.join(v.value.upper() for v in self.trade_codes)}" if self.trade_codes else ""
        travel_zone = f" {self.zone.value}" if self.zone != TravelZone.GREEN else ""
        return f"{self.name.upper()} {self.coords} {self.uwp}{base_codes}{trade_codes}{travel_zone}"

    @property
    def starport_label(self) -> str:
        return STARPORT_QUALITY_LABELS[self.starport_quality]

    @property
    def size_label(self) -> str:
        return SIZE_LABELS[self.size]

    @property
    def atmosphere_label(self) -> str:
        return ATMOSPHERE_LABELS[self.atmosphere]

    @property
    def hydrographics_label(self) -> str:
        return HYDROGRAPHICS_LABELS[self.hydrographics]

    @property
    def population_label(self) -> str:
        return f"{self.population_multiplier * (10 ** self.population):,}+"

    @property
    def government_label(self) -> str:
        return GOVERNMENT_LABELS[self.government]

    @property
    def law_label(self) -> str:
        return str(self.law)

    @property
    def tech_label(self) -> str:
        return str(self.tech)

    @property
    def base_label(self) -> str:
        return ", ".join(BASE_LABELS[b] for b in self.bases)

    @property
    def trade_codes_label(self) -> str:
        return ", ".join(TRADE_CODE_LABELS[t] for t in self.trade_codes)

    def get_t5_column_delimited_format(self) -> dict[str, str]:
        return {
            "Hex": self.coords,
            "Name": self.name,
            "UWP": self.uwp,
            "Remarks": f"{' '.join(v.value for v in self.trade_codes)}",
            "{Ix}": "",
            "(Ex)": "",
            "[Cx]": "",
            "N": "",
            "B": self.base_codes,
            "Z": self.zone.value,
            "PBG": f"{e_hex(self.population_multiplier)}{e_hex(self.planetoid_belts)}{e_hex(self.gas_giants)}",
            "W": "",
            "A": self.allegiance if self.allegiance else "",
            "Stellar": "G2 V"  # Dummy value, unused in Mongoose 2E
        }


@dataclass
class Subsector:
    name: str
    index: int


@dataclass
class Route:
    start_x: int
    start_y: int
    start_offset_x: int
    start_offset_y: int
    end_x: int
    end_y: int
    end_offset_x: int
    end_offset_y: int
    type: Optional[RouteType] = None


@dataclass
class Border:
    coordinates: list[tuple[int, int]]
    allegiance: Optional[str]
    color: Optional[str]


@dataclass
class Sector:
    name: str
    hexes: list[Hex] = field(default_factory=list)
    subsectors: list[Subsector] = field(default_factory=list)
    routes: list[Route] = field(default_factory=list)
    borders: list[Border] = field(default_factory=list)
    allegiances: dict[str, str] = field(default_factory=dict)

    def to_xml_metadata(self) -> ElementTree:
        root = Element("Sector")
        SubElement(root, "Name").text = self.name

        subsectors_element = SubElement(root, "Subsectors")
        for subsector in self.subsectors:
            subsector_element = SubElement(subsectors_element, "Subsector")
            subsector_element.set("Index", subsector_code(subsector.index))
            subsector_element.text = subsector.name

        routes_element = SubElement(root, "Routes")
        for route in self.routes:
            route_element = SubElement(routes_element, "Route")
            route_element.set("Start", to_coords(route.start_x, route.start_y))
            route_element.set("End", to_coords(route.end_x, route.end_y))
            if route.start_offset_x is not None:
                route_element.set("StartOffsetX", str(route.start_offset_x))
            if route.start_offset_y is not None:
                route_element.set("StartOffsetY", str(route.start_offset_y))
            if route.end_offset_x is not None:
                route_element.set("EndOffsetX", str(route.end_offset_x))
            if route.end_offset_y is not None:
                route_element.set("EndOffsetY", str(route.end_offset_y))
            if route.type is not None:
                route_element.set("Type", route.type.value)

        borders_element = SubElement(root, "Borders")
        for border in self.borders:
            border_element = SubElement(borders_element, "Border")
            border_element.text = " ".join(to_coords(x, y) for x, y in border.coordinates)
            if border.allegiance is not None:
                border_element.set("Allegiance", border.allegiance)
            if border.color is not None:
                border_element.set("Color", border.color)

        allegiances_element = SubElement(root, "Allegiances")
        for code, name in self.allegiances.items():
            allegiance_element = SubElement(allegiances_element, "Allegiance")
            allegiance_element.text = name
            allegiance_element.set("Code", code)

        return ElementTree(root)

    def to_t5_column_delimited_format(self) -> str:
        column_sizes = {}
        rows = []
        for sector_hex in self.hexes:
            row = sector_hex.get_t5_column_delimited_format()
            for column, value in row.items():
                column_sizes[column] = max(column_sizes.get(column, len(column)), len(value))
            rows.append(row)

        header = ""
        header_subtitle = ""
        for column in T5_COLUMN_DELIMITED_FORMAT_ORDER:
            padding = column_sizes.get(column, len(column) + 1)
            header += column.ljust(padding + 1)
            header_subtitle += "-" * padding + " "
        header = header[:-1]
        header_subtitle = header_subtitle[:-1]

        output = f"{header}\n{header_subtitle}"
        for row in rows:
            output += "\n" + " ".join(
                row[column].ljust(column_sizes[column]) for column in T5_COLUMN_DELIMITED_FORMAT_ORDER
            )

        return output
