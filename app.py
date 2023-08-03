import os
from flask import Flask

from flask_smorest import Api

# connects flask smorest extentsion to the flask app

from db import db
import models
import sqlite3

# the __XYZ__ is the default import when u dont precse

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint


def create_app(
    db_url=None,
):  # cretaing this fct to call it when needed for example testing
    app = Flask(__name__)
    # dictionary-like object in Flask used to store configuration settings for the application
    app.config[
        "PROPAGATE_EXCEPTIONS"
    ] = True  # if there is an exception propagate to main app
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"  # api standards
    app.config[
        "OPENAPI_URL_PREFIX"
    ] = "/"  # standard telling flask smorest where the root of the api is
    app.config[
        "OPENAPI_SWAGGER_UI_PATH"
    ] = "/swagger-ui"  # to tell smorest to us swagger for the documentaion
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    # we can also use for getting env varibales : os.getenv()"DATABASE_URL", "sqlite:///data.db")
    # connection string that has all necessary info to theclient, inthis case falk app is the client, includes db usernames db password where it hosted etc
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    db.init_app(
        app
    )  # it initiates the flask sqlachemy extension giving the flask app so it can connects it
    # when migraitng to postgres, we will use an environment variable, but now it doesnt exist so it uses sqlite
    api = Api(app)

    with app.app_context():
        db.create_all()  # sqlalchemy knows because we imported models

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    return app


if __name__ == "__main__":
    app = create_app()  # Create the Flask app
    app.run(debug=True)  # Start the development server with debug mode enabled
