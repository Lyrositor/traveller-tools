# traveller-tools

*A collection of utilities for running **Mongoose Traveller 2nd Edition** (a.k.a. MgT2) campaigns.*

This is a rough collection of tools we use to run our Mongoose Traveller campaign. It's not especially polished, and some aspects are very opinionated where the rules are unclear, but with some work it should be adaptable to your particular setup.

**License:** Creative Commons CC0 1.0 Universal

## Installation

You'll need to download [Poetry](https://python-poetry.org/) and create a virtual environment for `traveller-tools`.

Then, from within that virtual environment, you can install all the dependencies:

```bash
poetry run
```

## Usage

The `main.py` file is the entrypoint for the program. You can use it to generate the Traveller campaign website for the example campaign by running:

```bash
python main.py campaign examples/campaign.yaml example_campaign/
```

The world generator uses the name of the campaign as a seed for world generation. This means that changing the campaign name or the world generation code will lead to dramatic changes in the generated map, so this should be avoided (future versions of this tool may support saving the world to an intermediary YAML file to avoid this issue).

The map is generated using the [Traveller Map API](https://travellermap.com/doc/api) which, though it is mainly designed for other Traveller systems, works well enough with MgT2. In order to avoid making too many requests, the map is only generated once (on first run) by default; you can pass the `--refresh_map` argument to force regeneration.
