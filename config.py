from os import environ


class Config:
    """Set Flask configuration vars from .env file."""

    # # General Config
    # # SECRET_KEY = environ.get('SECRET_KEY')
    # FLASK_APP = environ.get('FLASK_APP')
    # FLASK_ENV = environ.get('FLASK_ENV')

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('postgresql://postgres:7fyQ2CPJWTvdYh@mesto-db-dev.c2nxiu4tdbzw.us-east-1.rds.amazonaws.com:5432/mesto-dev')
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")


