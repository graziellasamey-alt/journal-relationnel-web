from flask import Blueprint

question_routes = Blueprint("question_routes", __name__)

@question_routes.route("/questions/<int:id>", methods=["GET"])
def get_question(id):

    return {
        "id": id,
        "title": "Example question",
        "content": "This is a mock question"
    }