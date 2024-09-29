"""
load_signoffs.py

loads signoffs from rank_requirements file
prerequisites
load_ranks
load_scouts
load_requirements
"""

import csv
from flask_troop.models import (
    session,
    Scout,
    Signoff,
    Requirement,
    Rank,
)

from flask_troop import (
    parse_code,
    parse_scout,
    get_date_earned,
)

requirements_file = "data/rank_requirements.csv"


def add_signoff(scout, requirement, date):
    if (
        signoff := session.query(Signoff)
        .filter(Signoff.scout_id == scout.id)
        .filter(Signoff.rank == requirement.rank_name)
        .filter(Signoff.code == requirement.code)
        .one_or_none()
    ):
        signoff.date = date
    else:
        signoff = Signoff(
            scout=scout, rank=requirement.rank.name, code=requirement.code, date=date
        )
        session.add(signoff)


def import_signoffs(file):
    with open(file, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for line in reader:
            rank = Rank.get_rank(line["Rank"])
            code = parse_code(line["Code"])
            r = Requirement.get(rank=rank, code=code)
            s = Scout.get_scout(parse_scout(line["Scout"]))
            date = get_date_earned(line["Date Earned"])
            add_signoff(s, r, date)
        session.commit()


def main():
    import_signoffs(requirements_file)


if __name__ == "__main__":
    main()
