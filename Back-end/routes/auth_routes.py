from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import create_user, get_user_by_email

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    nom = data.get("nom")
    prenom = data.get("prenom")
    email = data.get("email")
    password = data.get("password")
    field_of_study = data.get("field_of_study")
    study_year = data.get("study_year")

    if not all([nom, prenom, email, password, field_of_study, study_year]):
        return jsonify({"error": "Tous les champs sont obligatoires"}), 400

    existing_user = get_user_by_email(email)
    if existing_user:
        return jsonify({"error": "Email déjà utilisé"}), 409

    password_hash = generate_password_hash(password)

    user_id = create_user(
        nom,
        prenom,
        email,
        password_hash,
        field_of_study,
        study_year
    )

    return jsonify({
        "message": "Utilisateur créé avec succès",
        "user_id": user_id
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email et mot de passe requis"}), 400

    user = get_user_by_email(email)
    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404

    if not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Mot de passe incorrect"}), 401

    session["user_id"] = user["id"]

    return jsonify({
        "message": "Connexion réussie",
        "user": {
            "id": user["id"],
            "nom": user["nom"],
            "prenom": user["prenom"],
            "email": user["email"],
            "field_of_study": user["field_of_study"],
            "study_year": user["study_year"]
        }
    }), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Déconnexion réussie"}), 200