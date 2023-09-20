from flask import Blueprint, jsonify

home_bp = Blueprint('home_bp', __name__, url_prefix="/")


# /
# everyone needs a home
@home_bp.route('/')
def index():
    return jsonify(error=None, results=["Welcome to the Titanic API"])
