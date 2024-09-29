import csv
from pprint import pprint
from twh_parser.utils import name_from_string


def main(file):
    reader = csv.DictReader(file)
    return [
        {
            f"{name_from_string(adult.get('Name')).get('last_name').strip()}, {name_from_string(adult.get('Name')).get('first_name').strip()}": {
                "Data": {
                    "Last Name": name_from_string(adult.get("Name"))
                    .get("last_name")
                    .strip(),
                    "First Name": name_from_string(adult.get("Name"))
                    .get("first_name")
                    .strip(),
                    "Address": adult.get("Mailing Address Line 1").strip(),
                    "Address2": adult.get("Mailing Address Line 2").strip(),
                    "City": adult.get("City").strip(),
                    "State": adult.get("State").strip(),
                    "Zip Code": adult.get("Zip Code").strip(),
                    "Home Phone": adult.get("Home Phone").strip(),
                    "Cell Phone": adult.get("Cell Phone").strip(),
                    "Business Phone": adult.get("Business Phone").strip(),
                    "Email": adult.get("Email").strip(),
                    "Email2": adult.get("Email #2").strip(),
                    "SMS": adult.get("SMS").strip(),
                    "Position": adult.get("Leadership"),
                }
            }
        }
        for adult in reader
    ]


if __name__ == "__main__":
    with open("adults.csv", encoding="utf-8-sig") as f:
        pprint(main(f))
