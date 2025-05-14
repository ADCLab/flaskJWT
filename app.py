from flask import Flask, jsonify, request
import jwt
import datetime
from flask_cors import CORS
import os

app = Flask(__name__)

# Load CORS origins and secret key from environment variables
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",")  # Expected format: "http://example.com,http://anotherwebsite.com"
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")  # Default fallback if environment variable is not set

# Load JWT expiration time from an environment variable (default to 20 minutes if not set)
JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", 20))

# Enable CORS and restrict it to specific domains
CORS(app, resources={r"/*": {"origins": CORS_ORIGINS}})

# Function to generate a new JWT
def generate_jwt():
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXPIRATION_MINUTES)
    payload = {
        "exp": expiration_time,  # Expiration time
        "iat": datetime.datetime.utcnow(),  # Issued at time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token, expiration_time

# Endpoint to generate a new JWT
@app.route('/generate-key', methods=['POST'])
def generate_key():
    token, expiration_time = generate_jwt()
    return jsonify({"api_key": token, "expires_at": expiration_time.isoformat()})

# Endpoint to validate a JWT
@app.route('/validate-key', methods=['POST'])
def validate_key():
    data = request.json
    token = data.get("api_key")
    if not token:
        return jsonify({"error": "API key missing"}), 400

    try:
        # Decode and validate the JWT
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"status": "valid", "expires_at": decoded["exp"]})
    except jwt.ExpiredSignatureError:
        return jsonify({"status": "expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"status": "invalid"}), 401

if __name__ == '__main__':
    app.run(debug=True)
