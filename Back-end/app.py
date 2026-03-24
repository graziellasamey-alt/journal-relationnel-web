from flask import Flask, jsonify, session, request, Response, redirect, url_for,render_template, abort 
from models.user_model import create_users_table
from routes.auth_routes import auth_bp
from routes.question_routes import question_bp
from routes.ressource_routes import resource_bp
import secrets
from functools import wraps
from models.db import init_db


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

#Decorateur de connexion 
def login_required(f):
    @wraps(f)
    def wrapper(*args,**kwrags):
        if 'user_id' not in session:
            abort(401)
        return f(*args, **kwrags)
    return wrapper

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(question_bp, url_prefix="/questions")
app.register_blueprint(resource_bp, url_prefix="/resources")


init_db()
@app.route("/")
def home():
    return jsonify({"message": "Backend AMU Help démarré"})

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



if __name__ == "__main__":
    app.run(debug=True)