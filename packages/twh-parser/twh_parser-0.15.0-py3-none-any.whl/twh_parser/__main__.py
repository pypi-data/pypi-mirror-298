"""
parser.py

from a troopmaster scout individual history report of all items, parse out
all kinds of scout information
"""

import click

from twh_parser.scouts import Parser
from objexplore import explore as objexplore

version = "0.15.0"


@click.command()
@click.option(
    "-z",
    "--zipfile",
    help="a zip file containing scouts, adults, rank_requirements, merit_badges, merit_badge_requirements files",
)
@click.option("-o", "--outfile", help='output filename, default is "output')
@click.option("-e", "--explore", is_flag=True, help="open object explorer")
def main(
    outfile=None,
    zipfile=None,
    explore=False,
):
    """takes INFILE and outputs troopmaster data converted to standard out or to OUTFILE"""
    if not outfile:
        output_type = "yaml"
    elif outfile.endswith("json"):
        output_type = "json"
    elif outfile.endswith("toml"):
        output_type = "toml"

    parser = Parser(
        zipfile=zipfile,
        outfile=outfile,
        file_format=output_type,
    )

    if explore:
        objexplore(parser.as_data_structure())
    elif outfile:
        parser.dump()
    else:
        print(parser.dumps())


if __name__ == "__main__":
    main()
