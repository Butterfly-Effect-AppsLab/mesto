from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

db = SQLAlchemy()
api = Api(app)


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')

    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:7fyQ2CPJWTvdYh@mesto-db-dev.c2nxiu4tdbzw.us-east-1.rds.amazonaws.com:5432/mesto-dev'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        # Imports
        from . import routes

        # Create tables for our models
        db.create_all()

        return app
