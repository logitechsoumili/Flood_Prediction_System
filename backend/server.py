from flask import Flask, request, jsonify, send_file
from predictor import predict_city
from flask import render_template
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/maps/city_markers_map.html")
def city_markers_map():
    map_path = os.path.join(os.path.dirname(__file__), '..', 'maps', 'city_markers_map.html')
    return send_file(map_path, mimetype='text/html')

@app.route("/maps/flood_risk_heatmap.html")
def flood_heatmap_map():
    map_path = os.path.join(os.path.dirname(__file__), '..', 'maps', 'flood_risk_heatmap.html')
    return send_file(map_path, mimetype='text/html')

@app.route("/predict-city", methods=["POST"])
def predict_city_api():
    data = request.get_json()

    if not data or "city" not in data:
        return jsonify({
            "error": "City name is required"
        }), 400

    city = data["city"]

    try:
        result = predict_city(city)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)