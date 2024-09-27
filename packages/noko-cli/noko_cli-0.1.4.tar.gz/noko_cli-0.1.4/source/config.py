"""Configuration file for the Noko CLI."""

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

from source.constants import SAVE_DIRECTORY
from source.utilities import read_file

load_dotenv()


@dataclass(frozen=True)
class Config:
    api_key: str
    user_id: str
    default_noko_project: str = field(default="")
    default_noko_tag: str = field(default="")
    google_cal_id: str = field(default="")
    scopes: list[str] = field(default_factory=lambda: ["https://www.googleapis.com/auth/calendar.events.readonly"])
    keep_event_types: list[str] = field(default_factory=lambda: ["default"])


CONFIG: Config = Config(**read_file(os.path.join(SAVE_DIRECTORY, "config.json")))
CREDENTIALS: dict = read_file(os.path.join(SAVE_DIRECTORY, "credentials.json"))
