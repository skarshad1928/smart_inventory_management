from flask import Flask
from flask_cors import CORS

from utils.db import database
from routes.products import products_bp
from routes.reviews import reviews_bp
from routes.users import users_bp  # if using users

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
app.register_blueprint(users_bp)  # optional

# -------------------------------------------------
# Health Route
# -------------------------------------------------
@app.route("/")
def home():
    return "Flask Backend Running Successfully"

# -------------------------------------------------
# Run Server
# -------------------------------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True, use_reloader=False)
