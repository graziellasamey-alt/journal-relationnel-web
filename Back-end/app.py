from flask import Flask
from flask_cors import CORS
from database import db
from models.user_model import User
from routes.auth_routes import auth_routes
from routes.question_routes import question_routes

app = Flask(__name__)

app.register_blueprint(question_routes)

app.register_blueprint(auth_routes)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

CORS(app)

@app.route("/")
def home():
    return {"message": "Backend running"}

@app.route("/users")
def get_users():
    users = User.query.all()

    return {
        "users": [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email
            }
            for u in users
        ]
    }

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
