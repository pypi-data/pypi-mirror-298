import csv
from flask_troop.models import (
    session,
    engine,
    Base,
    MBRequirement,
    MBReqNeed,
)

from load_database import add_scout

Base.metadata.create_all(engine)

mb_requirements_file = "data/merit_badge_requirements_by_scout.csv"


def add_mb_requirement(line):
    if (
        r := session.query(MBRequirement)
        .filter(MBRequirement.badge_name == line["Badge"])
        .filter(MBRequirement.code == line["Requirement"])
        .one_or_none()
    ):
        pass
    else:
        r = MBRequirement(
            badge_name=line["Badge"],
            code=line["Requirement"],
        )
    return r


def add_requirement_need(scout, requirement):
    if (
        mb_req_need := session.query(MBReqNeed)
        .filter(MBReqNeed.scout_id == scout.id)
        .filter(MBReqNeed.requirement_id == requirement.id)
        .one_or_none()
    ):
        ...
    else:
        mb_req_need = MBReqNeed(scout=scout, requirement=requirement)
        session.add(mb_req_need)
    mb_req_need.need = True


def import_merit_badges(file):
    with open(file, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for line in reader:
            s = add_scout(line)
            r = add_mb_requirement(line)
            add_requirement_need(s, r)


def main():
    import_merit_badges(mb_requirements_file)
    session.commit()


if __name__ == "__main__":
    main()
