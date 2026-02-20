from flask import Flask
from flask_cors import CORS

from utils.db import database
from routes.products import products_bp
from routes.reviews import reviews_bp
from routes.users import users_bp


# -------------------------------------------------
# Create App
# -------------------------------------------------
app = Flask(__name__)
CORS(app)


# -------------------------------------------------
# Connect Database ONCE at app startup
# -------------------------------------------------
database.connect()


# -------------------------------------------------
# Register Blueprints
# -------------------------------------------------
app.register_blueprint(products_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(users_bp)


# -------------------------------------------------
# Health Route
# -------------------------------------------------
@app.route("/")
def home():
    return {"message": "Smart Inventory API Running"}


# -------------------------------------------------
# IMPORTANT:
# DO NOT force port when deploying to Render
# Render automatically assigns PORT
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)