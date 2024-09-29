"""load_all.py
used to load all ranks, requirements, scouts, groups, signoffs from text files

usage:
import load_all

load_all.main()
"""

from flask_troop.models import Base, engine
import load_ranks
import load_requirements
import load_groups
import load_scouts
import load_signoffs


def main():

    Base.metadata.create_all(engine)
    print("loading ranks . . . ")
    load_ranks.main()
    print("done!")

    print("loading requirements . . . ")
    load_requirements.main()
    print("done!")

    print("loading groups . . . ")
    load_groups.main()
    print("done!")

    print("loading scouts . . . ")
    load_scouts.main()
    print("done!")

    print("loading signoffs . . . ")
    load_signoffs.main()
    print("done!")


if __name__ == "__main__":
    main()
