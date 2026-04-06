import os
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    session,
    flash,
    send_from_directory,
    jsonify
)
from werkzeug.utils import secure_filename

from models.resource_model import (
    create_resource,
    get_resource_by_id,
    get_recent_resources,
    get_user_resources,
    delete_resource
)
from models.user_model import get_user_by_id
from models.favorite_model import (
    get_user_favorite_resources,
    get_user_favorite_resource_ids,
    toggle_favorite_resource
)
resource_bp = Blueprint("resources", __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


def get_current_user_id():
    return session.get("user_id")


@resource_bp.route("/", methods=["GET"])
def list_resources():
    search = request.args.get("search")
    resource_type = request.args.get("resource_type")
    user_field_of_study = None
    favorite_resource_ids = []
    target_year = request.args.get("target_year")

    user_id = get_current_user_id()
    if user_id:
        user = get_user_by_id(user_id)
        if user:
            user_field_of_study = user["field_of_study"]

        favorite_resource_ids = get_user_favorite_resource_ids(user_id)

    resources = get_recent_resources(
        user_field_of_study=user_field_of_study,
        search=search,
        resource_type=resource_type,
        target_year=target_year
    )

    return render_template(
        "resources.html",
        resources=resources,
        favorite_resource_ids=favorite_resource_ids
    )

@resource_bp.route("/", methods=["POST"])
def add_resource():
    user_id = get_current_user_id()
    if not user_id:
        flash("Vous devez être connecté pour ajouter une ressource.", "error")
        return redirect(url_for("auth.login"))

    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "").strip()
    resource_type = request.form.get("resource_type", "").strip()
    target_year = request.form.get("target_year", "").strip()
    target_scope = request.form.get("target_scope", "").strip()
    description = request.form.get("description", "").strip()
    file = request.files.get("file")

    if not all([title, subject, resource_type, description, target_year, target_scope, file]):
        flash("Tous les champs sont obligatoires.", "error")
        return redirect(url_for("resources.list_resources"))

    filename = secure_filename(file.filename)
    if not filename:
        flash("Nom de fichier invalide.", "error")
        return redirect(url_for("resources.list_resources"))

    file_path = os.path.join(UPLOAD_DIR, filename)
    file.save(file_path)

    create_resource(
        user_id=user_id,
        title=title,
        subject=subject,
        resource_type=resource_type,
        description=description,
        file_path=filename,
        target_year=target_year,
        target_scope=target_scope
    )

    flash("Ressource ajoutée avec succès.", "success")
    return redirect(url_for("resources.list_resources"))


@resource_bp.route("/<int:resource_id>", methods=["GET"])
def resource_detail(resource_id):
    resource = get_resource_by_id(resource_id)

    if not resource:
        flash("Ressource introuvable.", "error")
        return redirect(url_for("resources.list_resources"))

    return render_template("resource_detail.html", resource=resource)


@resource_bp.route("/my", methods=["GET"])
def my_resources():
    user_id = get_current_user_id()
    if not user_id:
        flash("Authentification requise.", "error")
        return redirect(url_for("auth.login"))

    resources = get_user_resources(user_id)
    return render_template("my_resources.html", resources=resources)


@resource_bp.route("/<int:resource_id>/delete", methods=["POST"])
def remove_resource(resource_id):
    user_id = get_current_user_id()
    if not user_id:
        flash("Authentification requise.", "error")
        return redirect(url_for("auth.login"))

    resource = get_resource_by_id(resource_id)
    if not resource:
        flash("Ressource introuvable.", "error")
        return redirect(url_for("resources.my_resources"))

    deleted = delete_resource(resource_id, user_id)

    if not deleted:
        flash("Suppression impossible.", "error")
    else:
        filename = resource["file_path"]
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        flash("Ressource supprimée avec succès.", "success")

    return redirect(url_for("resources.my_resources"))


@resource_bp.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

from flask import render_template
from models.favorite_model import get_user_favorite_resources


@resource_bp.route("/favorites", methods=["GET"])
def favorite_resources():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("auth.login"))

    resources = get_user_favorite_resources(user_id)

    return render_template(
        "ressources-fav.html",
        resources=resources
    )

@resource_bp.route("/<int:resource_id>/favorite", methods=["POST"])
def toggle_resource_favorite(resource_id):
    user_id = get_current_user_id()

    if not user_id:
        return jsonify({
            "success": False,
            "message": "Vous devez être connecté pour ajouter une ressource aux favoris."
        }), 401

    resource = get_resource_by_id(resource_id)
    if not resource:
        return jsonify({
            "success": False,
            "message": "Ressource introuvable."
        }), 404

    is_now_favorite = toggle_favorite_resource(user_id, resource_id)

    return jsonify({
        "success": True,
        "is_favorite": is_now_favorite
    }), 200