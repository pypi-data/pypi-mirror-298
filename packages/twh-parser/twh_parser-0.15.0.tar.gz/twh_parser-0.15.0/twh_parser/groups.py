"""
load_groups.py

loads patrols and other groups from file

note: this only creates the groups
load_scouts inserts the scout into the groups

depends:
none

usage:
import load_groups
load_groups.main()

"""

import csv
from flask_troop.models import (
    session,
    Group,
)

requirements_file = "data/rank_requirements.csv"


def add_group(name):
    group = Group(name=name)
    session.add(group)


def import_groups(file):
    with open(file, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for line in reader:
            if line["Patrol"] is None:
                line["Patrol"] = "No Patrol"

            if not Group.get_group(line["Patrol"]):
                add_group(line["Patrol"])
        session.commit()


def main():
    import_groups(requirements_file)


if __name__ == "__main__":
    main()
