import logging

from flask import Blueprint, request, jsonify, current_app as app

from dao.titanic import Titanic

api_bp = Blueprint("api_bp", __name__, url_prefix="/api")

logger = logging.getLogger(__name__)
titanic_dao = Titanic()


# /api/prices
# qs: [quantiles]
@api_bp.route("/prices")
def prices():
    try:
        return jsonify(
            error=None,
            result=titanic_dao.prices_quantile(request.args.get("quantiles")),
        )
    except Exception as e:
        logger.error("/prices error", e)
        return jsonify(error=str(e), result=[]), 500


# /api/passengers/<id>
# qs: [cols, limit]
@api_bp.route("/passengers", defaults={"id": None})
@api_bp.route("/passengers/<id>")
def passenger(id=None):
    try:
        return jsonify(error=None, result=titanic_dao.get_passengers(id, request))
    except Exception as e:
        logger.error("/passenger error", e)
        return jsonify(error=str(e), result=[]), 500
