from flask import Blueprint, request, jsonify, session
from models.question_model import (
    create_question,
    get_question_by_id,
    get_recent_questions,
    get_user_questions,
    delete_question
)

question_bp = Blueprint("questions", __name__)


def login_required():
    user_id = session.get("user_id")
    return user_id


@question_bp.route("/", methods=["GET"])
def list_questions():
    user_field_of_study = request.args.get("field_of_study")
    user_study_year = request.args.get("study_year")
    search = request.args.get("search")

    questions = get_recent_questions(
        user_field_of_study=user_field_of_study,
        user_study_year=user_study_year,
        search=search
    )

    results = []
    for q in questions:
        results.append({
            "id": q["id"],
            "user_id": q["user_id"],
            "title": q["title"],
            "subject": q["subject"],
            "target_year": q["target_year"],
            "target_scope": q["target_scope"],
            "description": q["description"],
            "created_at": q["created_at"],
            "author": {
                "nom": q["nom"],
                "prenom": q["prenom"],
                "field_of_study": q["field_of_study"],
                "study_year": q["study_year"]
            }
        })

    return jsonify(results), 200


@question_bp.route("/<int:question_id>", methods=["GET"])
def question_detail(question_id):
    question = get_question_by_id(question_id)

    if not question:
        return jsonify({"error": "Question introuvable"}), 404

    return jsonify({
        "id": question["id"],
        "user_id": question["user_id"],
        "title": question["title"],
        "subject": question["subject"],
        "target_year": question["target_year"],
        "target_scope": question["target_scope"],
        "description": question["description"],
        "created_at": question["created_at"],
        "author": {
            "nom": question["nom"],
            "prenom": question["prenom"],
            "field_of_study": question["field_of_study"],
            "study_year": question["study_year"]
        }
    }), 200


@question_bp.route("/my", methods=["GET"])
def my_questions():
    user_id = login_required()
    if not user_id:
        return jsonify({"error": "Authentification requise"}), 401

    questions = get_user_questions(user_id)

    results = []
    for q in questions:
        results.append({
            "id": q["id"],
            "title": q["title"],
            "subject": q["subject"],
            "target_year": q["target_year"],
            "target_scope": q["target_scope"],
            "description": q["description"],
            "created_at": q["created_at"]
        })

    return jsonify(results), 200


@question_bp.route("/", methods=["POST"])
def add_question():
    user_id = login_required()
    if not user_id:
        return jsonify({"error": "Authentification requise"}), 401

    data = request.get_json()

    title = data.get("title")
    subject = data.get("subject")
    target_year = data.get("target_year")
    target_scope = data.get("target_scope")
    description = data.get("description")

    if not all([title, subject, target_year, target_scope, description]):
        return jsonify({"error": "Tous les champs sont obligatoires"}), 400

    question_id = create_question(
        user_id=user_id,
        title=title,
        subject=subject,
        target_year=target_year,
        target_scope=target_scope,
        description=description
    )

    return jsonify({
        "message": "Question créée avec succès",
        "question_id": question_id
    }), 201


@question_bp.route("/<int:question_id>", methods=["DELETE"])
def remove_question(question_id):
    user_id = login_required()
    if not user_id:
        return jsonify({"error": "Authentification requise"}), 401

    deleted = delete_question(question_id, user_id)

    if not deleted:
        return jsonify({"error": "Suppression impossible ou question introuvable"}), 404

    return jsonify({"message": "Question supprimée avec succès"}), 200