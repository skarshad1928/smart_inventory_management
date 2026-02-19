from flask import Blueprint, request, jsonify
from bson import ObjectId
from utils.db import database
import math

products_bp = Blueprint("products", __name__)

# Get collection safely
def get_products_collection():
    return database.get_collection("products")


# ==========================================================
# GET /api/products?page=1
# Pagination: limit = 20
# ==========================================================
@products_bp.route("/api/products", methods=["GET"])
def get_products():
    try:
        products = get_products_collection()

        page = request.args.get("page", 1)

        try:
            page = int(page)
            if page < 1:
                page = 1
        except ValueError:
            page = 1

        limit = 20
        skip = (page - 1) * limit

        total_products = products.count_documents({})
        total_pages = math.ceil(total_products / limit) if total_products > 0 else 1

        product_cursor = products.find().skip(skip).limit(limit)
        product_list = list(product_cursor)

        for product in product_list:
            product["_id"] = str(product["_id"])

        return jsonify({
            "currentPage": page,
            "totalPages": total_pages,
            "totalProducts": total_products,
            "products": product_list
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Failed to fetch products",
            "details": str(e)
        }), 500


# ==========================================================
# GET /api/products/<id>
# ==========================================================
@products_bp.route("/api/products/<id>", methods=["GET"])
def get_product_by_id(id):
    try:
        products = get_products_collection()

        try:
            obj_id = ObjectId(id)
        except:
            return jsonify({"error": "Invalid product ID"}), 400

        product = products.find_one({"_id": obj_id})

        if not product:
            return jsonify({"error": "Product not found"}), 404

        product["_id"] = str(product["_id"])

        return jsonify(product), 200

    except Exception as e:
        return jsonify({
            "error": "Failed to fetch product",
            "details": str(e)
        }), 500
