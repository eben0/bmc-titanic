from flask import Flask
from lib.logger import Logger

from api.api import api_bp
from api.home import home_bp
from api.swagger import swagger_bp, swaggerui_bp
from lib.config import Config
from lib.db import Db

try:
    # create logger
    config = Config.instance().all()
    Logger.setup()
    app = Flask(__name__)
    app.logger.info("Titanic Leaving the dock...")
    app.config.update(config)

    # registering blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(swagger_bp)
    app.register_blueprint(swaggerui_bp)

    # init the db, load csv into sqlite
    Db.instance().init_db()

    app.logger.info("Titanic is cruising now. Have fun.")
except Exception as e:
    print("Oopsie, it looks like we hit that iceberg once again")
