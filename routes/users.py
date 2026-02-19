from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from utils.db import database
from config import Config

users_bp = Blueprint("users", __name__)


def get_users_collection():
    return database.get_collection("users")


# -------------------------------
# Register
# -------------------------------
@users_bp.route("/api/users/register", methods=["POST"])
def register_user():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON body"}), 400

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"error": "All fields required"}), 400

        users = get_users_collection()

        if users.find_one({"email": email}):
            return jsonify({"error": "Email already registered"}), 400

        hashed_password = generate_password_hash(password)

        user_doc = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "created_at": datetime.utcnow()
        }

        result = users.insert_one(user_doc)

        return jsonify({
            "message": "User registered successfully",
            "user_id": str(result.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({
            "error": "Registration failed",
            "details": str(e)
        }), 500


# -------------------------------
# Login
# -------------------------------
@users_bp.route("/api/users/login", methods=["POST"])
def login_user():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON body"}), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        users = get_users_collection()
        user = users.find_one({"email": email})

        if not user:
            return jsonify({"error": "User not found"}), 404

        if not check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid credentials"}), 401

        # Generate JWT
        payload = {
            "user_id": str(user["_id"]),
            "exp": datetime.utcnow() + timedelta(hours=2)
        }

        token = jwt.encode(
            payload,
            Config.SECRET_KEY,
            algorithm="HS256"
        )

        return jsonify({
            "message": "Login successful",
            "token": token
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Login failed",
            "details": str(e)
        }), 500


# -------------------------------
# Get User
# -------------------------------
@users_bp.route("/api/users/<id>", methods=["GET"])
def get_user(id):
    try:
        users = get_users_collection()

        try:
            obj_id = ObjectId(id)
        except:
            return jsonify({"error": "Invalid user ID"}), 400

        user = users.find_one({"_id": obj_id})

        if not user:
            return jsonify({"error": "User not found"}), 404

        user["_id"] = str(user["_id"])
        user.pop("password", None)

        return jsonify(user), 200

    except Exception as e:
        return jsonify({
            "error": "Failed to fetch user",
            "details": str(e)
        }), 500
