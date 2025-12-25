import numpy as np
import pandas as pd
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------
# Load trained ML model
# --------------------------------------------------
model = joblib.load(os.path.join(BASE_DIR, "flood_model_v1.pkl"))

CITY_DF = pd.read_csv(os.path.join(BASE_DIR, "data", "city_features.csv"))
CITY_DF["city"] = CITY_DF["city"].str.lower()

# --------------------------------------------------
# Encoding helpers
# --------------------------------------------------
def encode_land_cover(land_cover):
    return [
        1 if land_cover == "agricultural" else 0,
        1 if land_cover == "desert" else 0,
        1 if land_cover == "forest" else 0,
        1 if land_cover == "urban" else 0,
        1 if land_cover == "water" else 0,
    ]


def encode_soil_type(soil):
    return [
        1 if soil == "clay" else 0,
        1 if soil == "loam" else 0,
        1 if soil == "peat" else 0,
        1 if soil == "sandy" else 0,
        1 if soil == "silt" else 0,
    ]


# --------------------------------------------------
# Core prediction function (PHASE 2 GOAL)
# --------------------------------------------------

def predict_city(city_name):
    city = city_name.lower()

    row = CITY_DF[CITY_DF["city"] == city]
    if row.empty:
        raise ValueError("City not found in dataset")

    row = row.iloc[0]

    features = [
        row["rainfall"],
        row["temperature"],
        row["humidity"],
        row["river_discharge"],
        row["water_level"],
        row["elevation"],
        row["population_density"],
        row["infrastructure"],
        row["historical_floods"],
    ]

    features += encode_land_cover(row["land_cover"])
    features += encode_soil_type(row["soil_type"])

    FEATURE_NAMES = ['Rainfall (mm)',
                    'Temperature (°C)',
                    'Humidity (%)',
                    'River Discharge (m³/s)',
                    'Water Level (m)',
                    'Elevation (m)',
                    'Population Density',
                    'Infrastructure',
                    'Historical Floods',
                    'Land Cover_Agricultural',
                    'Land Cover_Desert',
                    'Land Cover_Forest',
                    'Land Cover_Urban',
                    'Land Cover_Water Body',
                    'Soil Type_Clay',
                    'Soil Type_Loam',
                    'Soil Type_Peat',
                    'Soil Type_Sandy',
                    'Soil Type_Silt'
    ]   
    X = pd.DataFrame([features], columns=FEATURE_NAMES)

    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)

    flood_prob = float(probability[0][1])
    risk = risk_label(flood_prob)

    return {
        "city": city_name.title(),
        "flood_probability": round(flood_prob, 2),
        "risk_level": risk,
        "parameters": {
            "rainfall": float(row["rainfall"]),
            "temperature": float(row["temperature"]),
            "humidity": float(row["humidity"]),
            "river_discharge": float(row["river_discharge"]),
            "water_level": float(row["water_level"]),
            "elevation": float(row["elevation"]),
            "population_density": int(row["population_density"]),
            "historical_floods": int(row["historical_floods"]),
            "land_cover": str(row["land_cover"]),
            "soil_type": str(row["soil_type"])
        }
    }

def risk_label(prob_flood):
    if prob_flood < 0.35:
        return "Low"
    elif prob_flood < 0.65:
        return "Medium"
    else:
        return "High"


# --------------------------------------------------
# Local testing only (not used by Flask)
# --------------------------------------------------

if __name__ == "__main__":
    results = []

    for city in CITY_DF["city"]:
        result = predict_city(city)
        flood_prob = result["flood_probability"]
        risk = result["risk_level"]

        results.append((city, flood_prob, risk))

    # Sort by flood probability descending
    results.sort(key=lambda x: x[1], reverse=True)

    for city, flood_prob, risk in results:
        print(f"{city.title()} → Flood Probability: {flood_prob:.2f}")
        print(f"{city.title()} → Risk Level: {risk}")
        print("-" * 40)