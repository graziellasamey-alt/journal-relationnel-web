import os
from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
from models.resource_model import (
    create_resource,
    get_resource_by_id,
    get_recent_resources,
    get_user_resources,
    delete_resource
)

resource_bp = Blueprint("resources", __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


def login_required():
    user_id = session.get("user_id")
    return user_id


@resource_bp.route("/", methods=["GET"])
def list_resources():
    user_field_of_study = request.args.get("field_of_study")
    user_study_year = request.args.get("study_year")
    search = request.args.get("search")
    resource_type = request.args.get("resource_type")

    resources = get_recent_resources(
        user_field_of_study=user_field_of_study,
        user_study_year=user_study_year,
        search=search,
        resource_type=resource_type
    )

    results = []
    for r in resources:
        results.append({
            "id": r["id"],
            "user_id": r["user_id"],
            "title": r["title"],
            "subject": r["subject"],
            "resource_type": r["resource_type"],
            "file_path": r["file_path"],
            "target_year": r["target_year"],
            "target_scope": r["target_scope"],
            "created_at": r["created_at"],
            "author": {
                "nom": r["nom"],
                "prenom": r["prenom"],
                "field_of_study": r["field_of_study"],
                "study_year": r["study_year"]
            }
        })

    return jsonify(results), 200


@resource_bp.route("/<int:resource_id>", methods=["GET"])
def resource_detail(resource_id):
    resource = get_resource_by_id(resource_id)

    if not resource:
        return jsonify({"error": "Ressource introuvable"}), 404

    return jsonify({
        "id": resource["id"],
        "user_id": resource["user_id"],
        "title": resource["title"],
        "subject": resource["subject"],
        "resource_type": resource["resource_type"],
        "file_path": resource["file_path"],
        "target_year": resource["target_year"],
        "target_scope": resource["target_scope"],
        "created_at": resource["created_at"],
        "author": {
            "nom": resource["nom"],
            "prenom": resource["prenom"],
            "field_of_study": resource["field_of_study"],
            "study_year": resource["study_year"]
        }
    }), 200


@resource_bp.route("/my", methods=["GET"])
def my_resources():
    user_id = login_required()
    if not user_id:
        return jsonify({"error": "Authentification requise"}), 401

    resources = get_user_resources(user_id)

    results = []
    for r in resources:
        results.append({
            "id": r["id"],
            "title": r["title"],
            "subject": r["subject"],
            "resource_type": r["resource_type"],
            "file_path": r["file_path"],
            "target_year": r["target_year"],
            "target_scope": r["target_scope"],
            "created_at": r["created_at"]
        })

    return jsonify(results), 200


@resource_bp.route("/", methods=["POST"])
def add_resource():
    user_id = login_required()
    if not user_id:
        return jsonify({"error": "Authentification requise"}), 401

    title = request.form.get("title")
    subject = request.form.get("subject")
    resource_type = request.form.get("resource_type")
    target_year = request.form.get("target_year")
    target_scope = request.form.get("target_scope")
    file = request.files.get("file")

    if not all([title, subject, resource_type, target_year, target_scope, file]):
        return jsonify({"error": "Tous les champs sont obligatoires"}), 400

    filename = secure_filename(file.filename)
    if not filename:
        return jsonify({"error": "Nom de fichier invalide"}), 400

    file_path = os.path.join(UPLOAD_DIR, filename)
    file.save(file_path)

    resource_id = create_resource(
        user_id=user_id,
        title=title,
        subject=subject,
        resource_type=resource_type,
        file_path=file_path,
        target_year=target_year,
        target_scope=target_scope
    )

    return jsonify({
        "message": "Ressource créée avec succès",
        "resource_id": resource_id
    }), 201


@resource_bp.route("/<int:resource_id>", methods=["DELETE"])
def remove_resource(resource_id):
    user_id = login_required()
    if not user_id:
        return jsonify({"error": "Authentification requise"}), 401

    deleted = delete_resource(resource_id, user_id)

    if not deleted:
        return jsonify({"error": "Suppression impossible ou ressource introuvable"}), 404

    return jsonify({"message": "Ressource supprimée avec succès"}), 200