import os
from pathlib import Path

import toml

basedir = Path(os.path.dirname(__file__))


config = toml.load(basedir / "config.toml")


class Config:
    # the troop directory is data/TROOP/
    LOG_DIR = TROOP_DIR = basedir / "data"

    OUTPUT_FORMAT = config.get("OUTPUT_FORMAT", "yaml")
    OUTPUT_TO_FILE = config.get("OUTPUT_TO_FILE", False)

    INPUT_FILES = config.get("INPUT_FILES")

    PARTIAL_MB_HEADERS = config.get("PARTIAL_MB_HEADERS")
    OA_HEADERS = config.get("OA_HEADERS")
    ACTIVITY_HEADERS = config.get("ACTIVITY_HEADERS")
    SECTION_MARKERS = config.get("SECTION_MARKERS")
    TEXT_FIELDS = config.get("TEXT_FIELDS")
    DATE_FIELDS = config.get("DATE_FIELDS")
    RANKS = config.get("RANKS")
    UPPER_RANKS = config.get("UPPER_RANKS")
    STAR = config.get("STAR")
    LIFE = config.get("LIFE")
    EAGLE = config.get("EAGLE")
    OUTPUT_RANKS = config.get("OUTPUT_RANKS")
    CSV_HEADER = config.get("CSV_HEADER")
    MB_ALTERNATE_NAMES = config.get("MB_ALTERNATE_NAMES")

    MB_NAMES = config.get("MB_NAMES")
    MB_ALTERNATE_NAMES = config.get("MB_ALTERNATE_NAMES")
