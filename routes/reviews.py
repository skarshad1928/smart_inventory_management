from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime

from utils.db import database
from utils.auth import token_required
from services.sentiment import analyze_sentiment

reviews_bp = Blueprint("reviews", __name__)


# -------------------------------------------------------
# Helper: Get Collections
# -------------------------------------------------------
def get_products_collection():
    return database.get_collection("products")

def get_reviews_collection():
    return database.get_collection("reviews")


# -------------------------------------------------------
# Validation Function
# -------------------------------------------------------
def validate_review(data):
    errors = {}

    required = ["product_id", "review_text", "rating"]  # user_id removed

    for field in required:
        if field not in data or data[field] in [None, ""]:
            errors[field] = f"{field} is required"

    if errors:
        return errors

    try:
        ObjectId(data["product_id"])
    except:
        errors["product_id"] = "Invalid product_id"

    if not isinstance(data["rating"], int):
        errors["rating"] = "Rating must be integer"
    elif not (1 <= data["rating"] <= 5):
        errors["rating"] = "Rating must be between 1 and 5"

    if len(data["review_text"]) < 5:
        errors["review_text"] = "Review too short"

    return errors


# -------------------------------------------------------
# POST /api/reviews  (Protected Route)
# -------------------------------------------------------
@reviews_bp.route("/api/reviews", methods=["POST"])
@token_required
def add_review():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON body"}), 400

        errors = validate_review(data)
        if errors:
            return jsonify({
                "status": "validation_error",
                "errors": errors
            }), 400

        products = get_products_collection()
        reviews = get_reviews_collection()

        product_id = ObjectId(data["product_id"])
        rating = int(data["rating"])
        review_text = data["review_text"]

        # 🔐 user_id comes from JWT
        user_id = ObjectId(request.user_id)

        # Check product exists
        product = products.find_one({"_id": product_id})
        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Sentiment analysis
        sentiment = analyze_sentiment(review_text)

        review_doc = {
            "product_id": product_id,
            "user_id": user_id,
            "review_text": review_text,
            "rating": rating,
            "sentiment": sentiment,
            "created_at": datetime.utcnow()
        }

        reviews.insert_one(review_doc)

        # ------------------------------------------------
        # Computed Pattern Update (NO aggregation)
        # ------------------------------------------------
        old_avg = product.get("rating_average", 0)
        old_count = product.get("rating_count", 0)

        new_count = old_count + 1
        new_avg = ((old_avg * old_count) + rating) / new_count

        inc_fields = {
            "rating_count": 1
        }

        if sentiment == "positive":
            inc_fields["positive_count"] = 1
        elif sentiment == "negative":
            inc_fields["negative_count"] = 1

        products.update_one(
            {"_id": product_id},
            {
                "$inc": inc_fields,
                "$set": {
                    "rating_average": round(new_avg, 2)
                }
            }
        )

        return jsonify({
            "message": "Review added successfully",
            "sentiment": sentiment
        }), 201

    except Exception as e:
        return jsonify({
            "error": "Failed to submit review",
            "details": str(e)
        }), 500
