from flask import Blueprint

from lib.decorator import json_response

home_bp = Blueprint("home_bp", __name__, url_prefix="/")


# /
# everyone needs a home
@home_bp.route("/")
@json_response
def index():
    return ["Welcome to the Titanic API"]
