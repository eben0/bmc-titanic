import yaml
from flask import Blueprint
from flask_swagger_ui import get_swaggerui_blueprint

from lib.config import Config

SWAGGER_URL = "/api/docs"
API_URL = "/api/swagger"

swagger_bp = Blueprint("swagger_bp", __name__, url_prefix="/api")


# /api/swagger
# reruns as yaml
@swagger_bp.route("/swagger")
def swagger():
    swagger_file = Config().get("swagger")
    with open(swagger_file) as f:
        return yaml.safe_load(f)


# /api/docs
# swagger ui
swaggerui_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Titanic API"},
)
