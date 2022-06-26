import os
from dataclasses import asdict
from random import Random
from shutil import copyfile

import yaml
from jinja2 import Environment, PackageLoader
from yaml import Loader

from traveller.api.maps import render_sector_poster_svg
from traveller.campaign.models import Campaign, MissionStatus
from traveller.constants import TRADE_GOODS
from traveller.utils import subsector_code
from traveller.worldgen.models import Route, Sector, Border, Hex
from traveller.worldgen.run import run_worldgen

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
TEMPLATE_FILES = ("index.html", "new_port_checklist.html", "common.js")
STATIC_FILES = ("index.js", "new_port_checklist.js", "main.css")

env = Environment(loader=PackageLoader("traveller"))


def build_campaign_website(campaign_file_path: str, output_dir: str, refresh_map: bool) -> None:
    with open(campaign_file_path, encoding="utf-8") as f:
        data = yaml.load(f, Loader=Loader)
    campaign = Campaign(**data)
    start_date = get_date(campaign.start_date)
    current_date = get_date(campaign.current_date)
    sector = get_campaign_sector(campaign)
    os.makedirs(output_dir, exist_ok=True)

    sector_data = sector.to_t5_column_delimited_format()
    with open(os.path.join(output_dir, "sector.txt"), "w", encoding="utf-8") as f:
        f.write(sector_data)

    sector_metadata_file_path = os.path.join(output_dir, "sector_metadata.xml")
    sector_metadata_tree = sector.to_xml_metadata()
    sector_metadata_tree.write(sector_metadata_file_path, encoding="utf-8", xml_declaration=True)
    sector_metadata = open(sector_metadata_file_path, encoding="utf-8").read()

    if refresh_map or not os.path.exists("map.svg"):
        poster = render_sector_poster_svg(sector_data, metadata=sector_metadata, subsector=campaign.map_subsector)
        with open(os.path.join(output_dir, "map.svg"), "w", encoding="utf-8") as f:
            f.write(poster)
    else:
        poster = open(os.path.join(output_dir, "map.svg"), "r", encoding="utf-8").read()

    for template_file_name in TEMPLATE_FILES:
        index_template = env.get_template(template_file_name)
        with open(os.path.join(output_dir, template_file_name), "w", encoding="utf-8") as f:
            f.write(
                index_template.render(
                    campaign_name=campaign.name,
                    start_date=start_date,
                    date=f"{current_date[0]}-{current_date[1]:02d}-{current_date[2]}",
                    year=current_date[0],
                    week=current_date[1],
                    day=current_date[2],
                    ship_name=campaign.ship_name,
                    missions_ongoing=[mission for mission in campaign.missions if mission.status == MissionStatus.ONGOING],
                    missions_new=[mission for mission in campaign.missions if mission.status == MissionStatus.NEW],
                    missions_completed=[
                        mission for mission in campaign.missions if mission.status == MissionStatus.COMPLETED
                    ],
                    hexes=sector.hexes,
                    hexes_by_coords={h.coords: asdict(h) for h in sector.hexes},
                    trade_goods={key: asdict(info) for key, info in TRADE_GOODS.items()},
                    svg=poster.split("\n", maxsplit=1)[1],
                )
            )

    for static_file_name in STATIC_FILES:
        copyfile(os.path.join(TEMPLATE_DIR, static_file_name), os.path.join(output_dir, static_file_name))


def get_campaign_sector(campaign: Campaign) -> Sector:
    sector = run_worldgen(
        name=campaign.sector_name, density_dm=campaign.sector_density_dm, r=Random(campaign.sector_name)
    )

    for subsector in sector.subsectors:
        code = subsector_code(subsector.index)
        if subsector_name := campaign.subsectors.get(code):
            subsector.name = subsector_name

    for route_def in campaign.routes:
        start_x, start_y = get_coords(route_def.start)
        end_x, end_y = get_coords(route_def.end)
        sector.routes.append(
            Route(
                start_x=start_x,
                start_y=start_y,
                start_offset_x=route_def.start_offset_x,
                start_offset_y=route_def.start_offset_y,
                end_x=end_x,
                end_y=end_y,
                end_offset_x=route_def.end_offset_x,
                end_offset_y=route_def.end_offset_y,
                type=route_def.type,
            )
        )

    for border_def in campaign.borders:
        sector.borders.append(
            Border(
                allegiance=border_def.allegiance,
                coordinates=[get_coords(coords) for coords in border_def.coordinates],
                color=border_def.color
            )
        )

    for code, name in campaign.allegiances.items():
        sector.allegiances[code] = name

    hexes_by_code = {h.coords: h for h in sector.hexes}
    for hex_code, hex_def in campaign.map.items():
        existing_hex = hexes_by_code.get(hex_code)
        if hex_def.world_occurrence is False:
            if existing_hex:
                sector.hexes.remove(existing_hex)
                continue
        elif hex_def.world_occurrence is True and not existing_hex:
            x, y = get_coords(hex_code)
            existing_hex = Hex(x=x, y=y)
            sector.hexes.append(existing_hex)

        if not existing_hex:
            continue

        if hex_def.name is not None:
            existing_hex.name = hex_def.name
        if hex_def.num_gas_giants is not None:
            existing_hex.gas_giants = hex_def.num_gas_giants
        if hex_def.size is not None:
            existing_hex.size = hex_def.size
        if hex_def.atmosphere is not None:
            existing_hex.atmosphere = hex_def.atmosphere
        if hex_def.hydrographics is not None:
            existing_hex.hydrographics = hex_def.hydrographics
        if hex_def.population is not None:
            existing_hex.population = hex_def.population
        if hex_def.starport_quality is not None:
            existing_hex.starport_quality = hex_def.starport_quality
        if hex_def.government is not None:
            existing_hex.government = hex_def.government
        if hex_def.law is not None:
            existing_hex.law = hex_def.law
        if hex_def.tech is not None:
            existing_hex.tech = hex_def.tech
        if hex_def.bases is not None:
            existing_hex.bases = hex_def.bases
        if hex_def.allegiance is not None:
            existing_hex.allegiance = hex_def.allegiance
        if hex_def.zone is not None:
            existing_hex.zone = hex_def.zone
        if hex_def.trade_codes is not None:
            existing_hex.trade_codes = hex_def.trade_codes

    return sector


def get_coords(str_coords: str) -> tuple[int, int]:
    return int(str_coords[:2]), int(str_coords[2:])


def get_date(date_str: str) -> tuple[int, int, int]:
    year, week, day = (int(d) for d in date_str.split("-", maxsplit=2))
    return year, week, day
