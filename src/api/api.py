import logging

from flask import Blueprint, request

from dao.titanic import Titanic
from lib.decorator import json_response

api_bp = Blueprint("api_bp", __name__, url_prefix="/api")

logger = logging.getLogger(__name__)
titanic_dao = Titanic()


# /api/prices
# qs: [quantiles]
@api_bp.route("/prices")
@json_response
def prices():
    return titanic_dao.prices_quantile(request.args.get("quantiles"))


# /api/passengers/<id>
# qs: [cols, limit]
@api_bp.route("/passengers", defaults={"id": None})
@api_bp.route("/passengers/<id>")
@json_response
def passenger(id=None):
    return titanic_dao.get_passengers(id, request)
