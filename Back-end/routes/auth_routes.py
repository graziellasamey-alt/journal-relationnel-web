from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import create_user, get_user_by_email, get_user_by_id, update_user_profile
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("sign-up.html")

    nom = request.form.get("nom", "").strip()
    prenom = request.form.get("prenom", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")
    field_of_study = request.form.get("field_of_study", "").strip()
    study_year = request.form.get("study_year", "").strip()
    terms = request.form.get("terms")

    form_data = request.form

    if not all([nom, prenom, email, password, confirm_password, field_of_study, study_year]):
        flash("Tous les champs sont obligatoires.", "error")
        return render_template("sign-up.html", form_data=form_data)

    if password != confirm_password:
        flash("Les mots de passe ne correspondent pas.", "error")
        return render_template("sign-up.html", form_data=form_data)

    if not terms:
        flash("Vous devez accepter les conditions d'utilisation.", "error")
        return render_template("sign-up.html", form_data=form_data)

    if not (email.endswith("@etu.univ-amu.fr") or email.endswith("@univ-amu.fr")):
        flash("Veuillez utiliser une adresse email universitaire AMU.", "error")
        return render_template("sign-up.html", form_data=form_data)

    existing_user = get_user_by_email(email)
    if existing_user:
        flash("Email déjà utilisé.", "error")
        print("FLASH ERROR EMAIL")
        return render_template("sign-up.html", form_data=form_data)

    password_hash = generate_password_hash(password)

    create_user(
        nom,
        prenom,
        email,
        password_hash,
        field_of_study,
        study_year
    )

    flash("Inscription réussie. Vous pouvez maintenant vous connecter.", "success")
    return redirect(url_for("auth.login"))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        flash("Email et mot de passe requis", "error")
        return redirect(url_for("auth.login"))

    user = get_user_by_email(email)
    if not user:
        flash("Utilisateur introuvable", "error")
        return redirect(url_for("auth.login"))

    if not check_password_hash(user["password_hash"], password):
        flash("Mot de passe incorrect", "error")
        return redirect(url_for("auth.login"))

    session["user_id"] = user["id"]
    session.permanent = True
    flash("Connexion réussie", "success")
    return redirect(url_for("dashboard"))


@auth_bp.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop("user_id", None)
    flash("Déconnexion réussie", "success")
    return redirect(url_for("acceuil"))

@auth_bp.route("/profil", methods=["GET"])
def profil():
    user_id = session.get("user_id")
    if not user_id:
        flash("Authentification requise.", "error")
        return redirect(url_for("auth.login"))

    user = get_user_by_id(user_id)
    if not user:
        flash("Utilisateur introuvable.", "error")
        return redirect(url_for("auth.login"))

    return render_template("profil.html", user=user)



@auth_bp.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():
    user_id = session.get("user_id")

    if not user_id:
        flash("Authentification requise.", "error")
        return redirect(url_for("auth.login"))

    user = get_user_by_id(user_id)

    if request.method == "POST":
        prenom = request.form.get("prenom", "").strip()
        nom = request.form.get("nom", "").strip()
        email = request.form.get("email", "").strip()
        study_year = request.form.get("study_year", "").strip()
        field_of_study = request.form.get("field_of_study", "").strip()

        if not all([prenom, nom, email, study_year, field_of_study]):
            flash("Tous les champs sont obligatoires.", "error")
            return render_template("edit-profil.html", user=user)

        updated = update_user_profile(
            user_id,
            prenom,
            nom,
            email,
            study_year,
            field_of_study
        )

        if updated:
            flash("Profil mis à jour avec succès.", "success")
            return redirect(url_for("auth.profil"))
        else:
            flash("Erreur lors de la mise à jour.", "error")

    return render_template("edit-profil.html", user=user)