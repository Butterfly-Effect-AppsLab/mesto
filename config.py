from os import environ


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    # SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    DEBUG = True

    # Database
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:7fyQ2CPJWTvdYh@mesto-db-dev.c2nxiu4tdbzw.us-east-1.rds.amazonaws.com:5432/mesto-dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
