from flask import Flask, render_template, session, abort, flash, redirect, url_for
from routes.auth_routes import auth_bp
from routes.question_routes import question_bp
from routes.ressource_routes import resource_bp
from functools import wraps
from models.db import init_db
import secrets
from models.user_model import get_user_by_id
from models.question_model import get_recent_questions
from models.resource_model import get_recent_resources
from models.favorite_model import get_user_favorite_questions, get_user_favorite_resources
app = Flask(
    __name__,
    template_folder="../Front-end/HTML-PRINCIPAL",
    static_folder="../Front-end"
)

app.secret_key = secrets.token_hex(16)


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            abort(401)
        return f(*args, **kwargs)
    return wrapper


init_db()

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(question_bp, url_prefix="/questions")
app.register_blueprint(resource_bp, url_prefix="/resources")


@app.route("/")
def acceuil():
    return render_template("accueil.html")

@app.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")
    if not user_id:
        flash("Authentification requise.", "error")
        return redirect(url_for("auth.login"))

    user = get_user_by_id(user_id)
    if not user:
        flash("Utilisateur introuvable.", "error")
        return redirect(url_for("auth.login"))

    favorite_questions = get_user_favorite_questions(user_id)
    favorite_resources = get_user_favorite_resources(user_id)

    recent_questions = get_recent_questions(
        user_field_of_study=user["field_of_study"]
    )
    recent_resources = get_recent_resources(
        user_field_of_study=user["field_of_study"]
    )

    return render_template(
        "dashboard.html",
        user=user,
        favorite_questions_count=len(favorite_questions),
        favorite_resources_count=len(favorite_resources),
        recent_questions=recent_questions,
        recent_resources=recent_resources
    )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
"""
@app.get('/login')
def login_form():
    #TODO

    pass

@app.get('/register')
def register_form():
    #TODO
    pass

@app.post('/login')
def login_user():
    #TODO
    pass 

@app.post('/register')
def register_user():
    #TODO
    pass

app.get('/dashboard')
def dashboard():
    #TODO
    pass

app.get('/forum')
def forum():
    #TODO
    pass

@app.get('/questions/new')
def question_form():
    #TODO
    pass

@app.post('/questions')
def question():
    #TODO
    pass

@app.post('/questions/:id/favorite')
def add_favorite_question():
    #TODO
    pass

@app.get('/ressources')
def ressource_form():
    #TODO
    pass

"""


    