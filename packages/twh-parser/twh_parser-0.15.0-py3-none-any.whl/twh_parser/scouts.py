import csv
import logging
from datetime import datetime
from twh_parser.utils import name_from_string, fix_code
import zipfile as Zip
from icecream import ic


logger = logging.Logger(__name__)


class Parser:
    def __init__(self, zipfile, outfile=None, file_format="yaml"):
        logger.warning("starting the parse")
        self.scouts = {}
        if not outfile:
            self.outfile = f"output.{file_format}"
        else:
            self.outfile = outfile
        self.output_type = file_format

        z = Zip.Path(zipfile)
        for file in z.iterdir():
            if "Scout Directory" in file.name:
                logger.info("processing scout directory")
                self.process_scouts(file.open(encoding="utf-8-sig"))
        for file in z.iterdir():
            if "Rank Requirements Status" in file.name:
                self.process_signoffs(file.open(encoding="utf-8-sig"))
        for file in z.iterdir():
            if "Merit Badge History" in file.name:
                self.process_merit_badges(file.open(encoding="utf-8-sig"))

    def process_scouts(self, scout_file):
        reader = csv.DictReader(scout_file)
        for line in reader:
            name, full_name = name_from_string(line.get("Name").strip())
            self.scouts[full_name] = Scout(line, name)

    def process_signoffs(self, requirement_file):
        reader = csv.DictReader(requirement_file)
        for line in reader:
            name, full_name = name_from_string(line.get("Scout").strip())
            if full_name not in self.scouts:
                print(f"scout not found while adding requirement: {line}")
                continue
            else:
                self.scouts[full_name].add_badge(line["Rank"].strip()).add_signoff(
                    line["Code"], line["Date Earned"]
                )

    def process_merit_badges(self, merit_badges_file):
        reader = csv.DictReader(merit_badges_file)
        for line in reader:
            name, full_name = name_from_string(line.get("Scout").strip())
            if full_name not in self.scouts:
                print(f"scout not found while adding requirement: {line}")
                continue
            else:
                self.scouts[full_name].add_merit_badge(
                    line["Merit Badge"].strip(), line["Earned"]
                )

    def as_data_structure(self):
        output = {}
        for scout in self.scouts.values():
            output.update(scout.as_data_structure())
        return output

    def dump(self):
        with open(self.outfile, "w") as f:
            f.write(self.dumps())

    def dumps(self):
        if self.output_type in ("yaml", "YAML", "yml"):
            import yaml

            return yaml.dump(self.as_data_structure())


class Scout:

    def __init__(self, line, name):
        self.data = {
            "Last Name": name.get("last_name"),
            "First Name": name.get("first_name"),
            "Nick Name": name.get("nick_name"),
            "Address": line.get("Mailing Address Line 1").strip(),
            "Address2": line.get("Mailing Address Line 2").strip(),
            "City": line.get("City").strip(),
            "State": line.get("State").strip(),
            "Zip Code": line.get("Zip Code").strip(),
            "Home Phone": line.get("Home Phone").strip(),
            "Cell Phone": line.get("Cell Phone").strip(),
            "Email": line.get("Email").strip(),
            "Email2": line.get("Email #2").strip(),
            "SMS": line.get("SMS").strip(),
            "Age": line.get("Age").strip(),
            "Grade": line.get("Grade").strip(),
            "Rank": line.get("Rank").strip(),
            "Patrol": line.get("Patrol")
            .removesuffix(" (M)")
            .removesuffix(" (F)")
            .strip(),
        }
        self.position = line.get("Leadership")
        self.advancement = {"Ranks": {}, "Merit Badges": {}}

    @property
    def last_name(self):
        return self.data["Last Name"]

    @property
    def first_name(self):
        return self.data["First Name"]

    def add_badge(self, badge_name):
        if badge_name not in self.advancement["Ranks"]:
            badge = Badge(badge_name.strip())
            self.advancement["Ranks"][badge_name.strip()] = badge
            return badge
        else:
            return self.advancement["Ranks"][badge_name.strip()]

    def add_merit_badge(self, badge_name, badge_date):
        if badge_name not in self.advancement["Merit Badges"]:
            badge = MeritBadge(badge_name.strip())
            badge.complete(datetime.strptime(badge_date, "%m/%d/%y").date())

            self.advancement["Merit Badges"][badge_name.strip()] = badge
            return badge
        else:
            return self.merit_badges[badge_name]

    def as_data_structure(self):
        output = {
            f"{self.last_name}, {self.first_name}": {
                "Data": self.data,
                "Leadership": self.position,
                "Advancement": {"Ranks": {}, "Merit Badges": {}},
            }
        }
        for rank in self.advancement["Ranks"].values():
            output[f"{self.last_name}, {self.first_name}"]["Advancement"][
                "Ranks"
            ].update(rank.as_data_structure())
        for merit_badge in self.advancement["Merit Badges"].values():
            output[f"{self.last_name}, {self.first_name}"]["Advancement"][
                "Merit Badges"
            ].update(merit_badge.as_data_structure())
        return output


class Badge:
    def __init__(self, name, date=None):
        self.name = name
        self.signoffs = {}
        if date:
            self.date = date
        else:
            self.date = None

    def complete(self, date):
        self.date = date

    def add_signoff(self, code, date):
        if not date:
            return
        code = fix_code(code)
        signed_date = datetime.strptime(date.strip(), "%m/%d/%y").date()
        if code not in self.signoffs:
            self.signoffs[code] = Signoff(code, signed_date)

    def as_data_structure(self):
        output = {self.name: {"Requirements": {}}}

        if self.date:
            output[self.name]["Date"] = self.date

        for signoff in self.signoffs.values():
            output[self.name]["Requirements"][signoff.code] = {"Date": signoff.date}

        return output


class MeritBadge(Badge):
    pass


class Signoff:
    def __init__(self, code, date):
        self.date = date
        self.code = code
