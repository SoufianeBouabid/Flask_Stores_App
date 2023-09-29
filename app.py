import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask import Flask, session
from flask_session import Session
# from flask_jwt import jwt_required, JWT
from datetime import timedelta
from flask import Response,request

# connects flask smorest extentsion to the flask app

from db import db
from blocklist import BLOCKLIST
import models
import sqlite3
import logging
# the __XYZ__ is the default import when u dont precse

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from resources.cookie import blp as CookieBlueprint


# cretaing this fct to call it when needed for example testing
app = Flask(__name__)
CORS(app)

# db_url="postgres://afysjadp:tGRwEncguWTxO-_chc6rA7Ghiu6j2Nqd@trumpet.db.elephantsql.com/afysjadp"
app.secret_key = "96649321673240285422287757096837466547"  # same as jwt secret key

# @app.before_request
# def authorize_token():
#     if request.endpoint == '*':
#         try:
#             if request.method != 'OPTIONS':  # <-- required
#                 auth_header = request.headers.get("Authorization")
#                 if "Bearer" in auth_header:
#                     token = auth_header.split(' ')[1]
#                     return "ok",200
#         except Exception as e:
#             return "401 Unauthorized\n{}\n\n".format(e), 401

# @app.after_request
# def add_header(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     return response
# dictionary-like object in Flask used to store configuration settings for the application

# logging.getLogger('flask_cors').level = logging.DEBUG

load_dotenv() #find .env file at the root of the project and run the context
app.config[
    "PROPAGATE_EXCEPTIONS"
] = True  # if there is an exception propagate to main app
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"  # api standards
app.config[
    "OPENAPI_URL_PREFIX"
] = "/"  # standard telling flask smorest where the root of the api is
# app.config['CORS_HEADERS'] = 'application/json'
app.config[
    "OPENAPI_SWAGGER_UI_PATH"
] = "/swagger-ui"  # to tell smorest to us swagger for the documentaion
app.config[
    "OPENAPI_SWAGGER_UI_URL"
] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL"
)
# we can also use for getting env varibales : os.getenv()"DATABASE_URL", "sqlite:///data.db")
# connection string that has all necessary info to theclient, inthis case falk app is the client, includes db usernames db password where it hosted etc
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
print("SQLALCHEMY_DATABASE_URI:", app.config["SQLALCHEMY_DATABASE_URI"])
db.init_app(
    app
)  # it initiates the flask sqlachemy extension giving the flask app so it can connects it
# when migraitng to postgres, we will use an environment variable, but now it doesnt exist so it uses sqlite
migrate = Migrate(app, db)
api = Api(app)
#jwt = JWT(UserBlueprint)

    
# # Configure Flask-Session
# app.config["SESSION_TYPE"] = "filesystem"  #  can use different storage options
# app.config["SESSION_COOKIE_SECURE"] = True  # Enable secure (HTTPS-only) cookies
# app.config["SESSION_USE_SIGNER"] = True  # Sign session cookies for security

# # Initialize Flask-Session
# Session(app)

# setting refresh token :

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=8)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(seconds=1000)
app.config["JWT_SECRET_KEY"] = "96649321673240285422287757096837466547"
# secret ket dont get stored normaly in code but in env variable
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(
    jwt_header, jwt_payload
):  # if this fct returns true token gives error token not available/revoqued
    return jwt_payload["jti"] in BLOCKLIST

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "description": "The token is not fresh.",
                "error": "fresh_token_required",
            }
        ),
        401,
    )

# claim to add extra infos to the jwt except the user_id:
@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:  # exemple as the admin with id =1 is the only ne with access
        return {"is_admin": True}
    return {"is_admin": False}

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )

with app.app_context():
    db.create_all()  # sqlalchemy knows because we imported models

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)
api.register_blueprint(TagBlueprint)
api.register_blueprint(UserBlueprint)
api.register_blueprint(CookieBlueprint)



        # if __name__ == "__main__":
        #     app = create_app()  # Create the Flask app
        #     app.run(debug=True)  # Start the development server with debug mode enabled
