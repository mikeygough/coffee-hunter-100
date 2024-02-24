"""Initialize Config class to access environment variables."""
from dotenv import load_dotenv
import os

load_dotenv()


class Config(object):
    """Set environment variables."""

    SQLALCHEMY_DATABASE_URI = os.getenv("CH_100_APP_DB_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
