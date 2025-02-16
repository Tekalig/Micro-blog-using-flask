import os

from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api

# import custom blueprint
from controllers.post import post_blueprint
# import database initial configuration
from config.db import db

# load environmental variables
load_dotenv()

# Get database connection parameters from the environment
DB_USERNAME = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

#  create PostgresSQL SQLAlchemy uri
postgres_db_uri = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# use function to initialize the app
def create_app():
    # initialize flask app
    app = Flask(__name__)

    # config the flask app
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Micro blog rust api"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = postgres_db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # initialize database
    db.init_app(app)

    # before creating or request anything create tables
    with app.app_context():
        db.create_all()

    # initialize the api
    api = Api(app)

    # user blueprint route
    api.register_blueprint(post_blueprint)

    return app



