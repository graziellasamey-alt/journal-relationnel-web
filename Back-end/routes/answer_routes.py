from flask import Blueprint

answer_routes = Blueprint("answer_routes", __name__)

@answer_routes.route("/answers", methods=["GET"])
def get_answers():
    return {"answers": []}