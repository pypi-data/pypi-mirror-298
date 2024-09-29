"""
load_ranks.py

loads ranks from ranks.csv
prerequisites:none

usage:
import load_ranks
load_ranks.main()
"""

import csv
from flask_troop.models import (
    session,
    Rank,
)


ranks_file = "data/ranks.csv"


def add_rank(line):
    if not session.query(Rank).filter(Rank.name == line["name"]).one_or_none():
        rank = Rank(
            name=line["name"],
            rank_order=line["rank_order"],
            upper_rank=False if line["upper_rank"] == "False" else True,
            extra_rank=False if line["extra_rank"] == "False" else True,
            final_code=line["final_code"],
        )
        session.add(rank)


def import_ranks(file):
    with open(file, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for line in reader:
            add_rank(line)
        session.commit()


def main():
    import_ranks(ranks_file)


if __name__ == "__main__":
    main()
