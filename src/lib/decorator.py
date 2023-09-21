import logging
from functools import wraps
from flask import jsonify, request


def json_response(f):
    """
    decorator function that wraps the json response
    and handles the error message
    :param f: route function
    :return: response
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return jsonify(error=None, result=f(*args, **kwargs))
        except Exception as e:
            logging.getLogger().error(f"{request.path} error", e)
            return jsonify(error=str(e), result=[]), 500

    return decorated_function
