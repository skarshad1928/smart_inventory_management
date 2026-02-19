import jwt
from functools import wraps
from flask import request, jsonify
from config import Config


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Authorization token is missing"}), 401

        try:
            parts = auth_header.split(" ")

            if len(parts) != 2 or parts[0] != "Bearer":
                return jsonify({"error": "Invalid authorization format"}), 401

            token = parts[1]

            decoded = jwt.decode(
                token,
                Config.SECRET_KEY,
                algorithms=["HS256"]
            )

            request.user_id = decoded.get("user_id")

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        except Exception as e:
            return jsonify({
                "error": "Token verification failed",
                "details": str(e)
            }), 401

        return f(*args, **kwargs)

    return decorated
