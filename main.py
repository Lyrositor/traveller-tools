import random
from typing import Optional

import click

from traveller.campaign.run import build_campaign_website
from traveller.worldgen.run import run_worldgen


@click.group()
def cli():
    pass


@cli.command()
@click.option("--density", default=0)
@click.option("--seed", default=None)
@click.argument("name")
@click.argument("output_file")
def worldgen(name: str, output_file: str, density: int, seed: Optional[int] = None) -> None:
    sector = run_worldgen(name, density_dm=density, r=random.Random(seed))
    with open(output_file, "w") as f:
        f.write(sector.to_t5_column_delimited_format())


@cli.command()
@click.argument("file")
@click.argument("output_dir")
@click.option("--refresh_map", default=False)
def campaign(file: str, output_dir: str, refresh_map: bool = False) -> None:
    build_campaign_website(file, output_dir, refresh_map)


if __name__ == "__main__":
    cli()
