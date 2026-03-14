from flask import Blueprint, request, jsonify
from models.user_model import User
from database import db

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/register", methods=["POST"])
def register():

    data = request.json

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"error": "Email already used"}), 400

    new_user = User(
        username=username,
        email=email,
        password=password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created"})

@auth_routes.route("/verify-email", methods=["POST"])
def verify_email():

    data = request.json
    email = data.get("email")

    user = User.query.filter_by(email=email).first()

    if not user:
        return {"error": "User not found"}, 404

    user.verified = True
    db.session.commit()

    return {"message": "Email verified"}

@auth_routes.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or user.password != password:
        return {"error": "Invalid credentials"}, 401

    if not user.verified:
        return {"error": "Email not verified"}, 403

    return {
        "message": "Login successful",
        "user_id": user.id
    }