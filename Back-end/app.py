from flask import Flask, render_template, session, abort
from routes.auth_routes import auth_bp
from routes.question_routes import question_bp
from routes.ressource_routes import resource_bp
from functools import wraps
from models.db import init_db
import secrets

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


if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)

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

if __name__ == "__main__":
    app.run(debug=True)
    