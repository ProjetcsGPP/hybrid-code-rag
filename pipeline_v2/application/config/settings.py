# pipeline_v2/application/config/settings.py

import os

from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[3]

ENV_PATH = BASE_DIR / ".env"

# print("ENV_PATH:", ENV_PATH)

# print("ENV_EXISTS:", ENV_PATH.exists())

load_dotenv(ENV_PATH)


class Settings:

    DB_NAME = os.getenv("DB_NAME")

    DB_USER = os.getenv("DB_USER")

    DB_PASSWORD = os.getenv("DB_PASSWORD")

    DB_HOST = os.getenv("DB_HOST", "localhost")

    DB_PORT = int(os.getenv("DB_PORT", 5432))


# print("BASE_DIR:", repr(BASE_DIR))
# print("DB_NAME:", repr(Settings.DB_NAME))
# print("DB_USER:", repr(Settings.DB_USER))
# print("RAW PASSWORD:", repr(Settings.DB_PASSWORD))
# print("DB_HOST:", repr(Settings.DB_HOST))
# print("DB_PORT:", repr(Settings.DB_PORT))
