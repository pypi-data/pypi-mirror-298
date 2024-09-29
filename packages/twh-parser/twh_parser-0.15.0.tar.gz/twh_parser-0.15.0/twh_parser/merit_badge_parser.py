import fitz
import re
import csv
import yaml


"""
merit_badge_parser.py

parses troopwebhost merit badge report

needs:
the troopwebhost uncompleted merit badge requirements by requirement report
the troopwebhost rank requirements status report (for the scout names)
the list of merit badges (included)
"""


"""
The dimensions of a US Letter page for the PDF Parser
"""
WHOLE_PAGE = [0, 0, 612, 792]


text = []


# will look for things like 09.d or 10. or 3.a. Must have digits and a dot
requirement_pat = re.compile(r"^\d+\..*$")


def find_requirement(text):
    return bool(re.match(requirement_pat, text))


with fitz.open("merit_badges.pdf") as f:
    for page in f:

        """
        Take all the strings from the PDF and split and strip them.
        """
        text.append([_.strip() for _ in page.get_textbox(WHOLE_PAGE).split("\n")])


with open("data/rank_requirements.csv") as f:
    reader = csv.DictReader(f)
    scout_names = {_["Scout"] for _ in reader}
    """
    This one is fun. You need to turn 'Last, First MI "Nickname"' into "Last, First"
    so you split it on a comma, then take the first part (last name), 
    and the first part of the second part (first name) and join them together with 
    a comma and a space. Probably could do this with a regex but this was easier. 
    Make a set with the results so you don't have repeated names.
    """
    scout_names = {
        ", ".join((_.split(", ")[0], _.split(", ")[1].split()[0])) for _ in scout_names
    }


with open("data/merit_badges_list.txt") as f:
    reader = csv.reader(f)
    merit_badges = {_[1].title() for _ in reader}


requirements = {}
with open("data/merit_badge_requirements_by_scout.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(("Badge", "Requirement", "Scout"))
    for item in text:
        for thing in item:
            if find_requirement(thing):
                requirements[item][thing] = []
                requirement = thing
            elif thing in scout_names:
                scout = thing
                requirements[item][requirement].append(scout)
                writer.writerow((item, requirement.split()[0], scout))
            elif "Merit Badge Requirements" in thing:
                ...
            elif thing.title() in merit_badges:
                requirements[thing] = {}
                badge = thing
            elif " rqmts)" in thing and any(
                [badge in thing.title() for badge in merit_badges]
            ):
                badge = thing
                requirements[thing] = {}
            else:
                ...

with open("data/merit_badge_requirements_by_badge_and_requirement.yaml", "w") as f:
    f.write(yaml.dump(requirements))
