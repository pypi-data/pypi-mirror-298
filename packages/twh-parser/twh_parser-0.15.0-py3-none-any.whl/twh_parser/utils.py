import re
from icecream import ic

# Matches "Perkins, Michael "Mike""
pat1 = re.compile(r'^(.*), (.*?)( "(.*)")?$')

# Matches "Michael Perkins"
pat2 = re.compile(r"^(.*) (.*)$")


def name_from_string(text):
    if m := pat1.match(text.strip()):
        last_name = m.group(1).strip()
        first_name = m.group(2).strip()
        nick_name = m.group(4).strip() if m.group(4) else None

    elif m := pat2.match(text.strip()):
        last_name = m.group(2).strip()
        first_name = m.group(1).strip()
        nick_name = None

    else:
        last_name = text.strip()

    return {
        "last_name": last_name,
        "first_name": first_name,
        "nick_name": nick_name,
    }, f"{last_name.strip()}, {first_name.strip()}"


def fix_code(string):

    REMOVE_PERIOD = str.maketrans("", "", ".")

    """takes format codes formatted like scoutbook has them and returns them normalized"""
    # 1.a -> 1a
    string = string.translate(REMOVE_PERIOD).strip()

    if string.isdigit() and len(string) == 1:
        # 1, 4 -> 01, 04
        return "0" + string
    elif string.isdigit() and len(string) == 2:
        # 10, 11, 12 -> 10, 11, 12
        return string
    elif len(string) == 2:
        # 1a, 1c, 5a -> 01a, 01c, 05a
        return "0" + string
    elif len(string) == 3:
        # 10a, 11c -> 10a, 11c
        return string
    else:
        raise TypeError(f"poorly formatted rank requirement code: {string}")


assert name_from_string('Perkins, Michael "Mike"') == (
    {
        "last_name": "Perkins",
        "first_name": "Michael",
        "nick_name": "Mike",
    },
    "Perkins, Michael",
)

assert name_from_string("Aramayo, Leo ") == (
    {
        "last_name": "Aramayo",
        "first_name": "Leo",
        "nick_name": None,
    },
    "Aramayo, Leo",
)


assert name_from_string("Star Perkins") == (
    {
        "last_name": "Perkins",
        "first_name": "Star",
        "nick_name": None,
    },
    "Perkins, Star",
)


assert fix_code("4.") == "04"

assert fix_code("14.") == "14"
assert fix_code("4.a.") == "04a"
assert fix_code("1c") == "01c"
assert fix_code("11c") == "11c"
