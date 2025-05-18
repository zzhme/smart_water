from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
jwt = JWTManager(app)

@app.route('/api/sensor_data')
@jwt_required()
def get_sensor_data():
    try:
        # Data collection logic...
        return jsonify({"data": processed_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500