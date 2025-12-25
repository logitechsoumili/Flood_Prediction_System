# Flood Risk Prediction System (v1)

An early-stage ML-powered system for predicting flood risk across Indian cities using environmental and geographical data.

## Overview

This project combines machine learning with geospatial visualization to identify flood-prone areas and assess risk levels. The system analyzes multiple environmental factors including rainfall, temperature, river discharge, and soil composition to generate city-level flood risk predictions.

## Features

- **ML-Based Predictions**: Trained classifier predicting flood probability for 50+ Indian cities
- **Interactive Risk Map**: Folium-based HTML map with toggle-enabled layers
  - City Risk Markers (color-coded by severity)
  - Flood Risk Heatmap (intensity visualization)
- **Risk Classification**: Three-tier risk system (Low/Medium/High)
- **Modular Architecture**: Separated prediction engine and visualization layers

## Project Structure

```
Flood_Prediction_System/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── V1_flood_prediction.ipynb          # Jupyter notebook for EDA & model training
├── data/
│   ├── city_features.csv              # City environmental features
│   └── flood_risk_dataset_india.csv   # Historical flood risk dataset
├── backend/
│   ├── predictor.py                   # Core prediction engine
│   └── server.py                      # Flask API server
├── maps/
│   ├── generate_map.py                # Map generation script
│   ├── city_coordinates.csv           # City lat/lon data
│   ├── city_predictions.csv           # Predictions output
│   ├── city_markers_map.html          # Interactive city risk markers map
│   └── flood_risk_heatmap.html        # Intensity heatmap visualization
└── templates/
    └── dashboard.html                 # Web dashboard (Flask template)
```

## Tech Stack

- **Python** 3.x
- **Pandas** - Data processing
- **NumPy** - Numerical computations
- **Scikit-learn** - ML model (Random Forest/Gradient Boosting)
- **Folium** - Interactive mapping

## Current Status

✅ EDA completed  
✅ Baseline ML model trained & saved  
✅ Interactive map with risk visualization  
⏳ Phase 2: Real-time API data integration (planned)

## Usage

### Option 1: Run Predictions & Generate Maps

```bash
cd backend
python predictor.py  # Run predictions for all cities

cd ../maps
python generate_map.py  # Generate interactive HTML maps
```

Open `maps/city_markers_map.html` or `maps/flood_risk_heatmap.html` in a web browser to view the maps.

### Option 2: Start the Flask API Server

```bash
cd backend
python server.py  # Start the Flask API on localhost:5000
```

Access the dashboard at `http://localhost:5000` and use the API endpoints for predictions.

### Option 3: Direct Python API

```python
from backend.predictor import predict_city, risk_label

city_name = "Chennai"
prediction, probability = predict_city(city_name)
flood_probability = probability[0][1]
risk = risk_label(flood_probability)

print(f"{city_name}: {flood_probability:.2f} ({risk} Risk)")
```

## Model Details

- **Input Features**: 19 (rainfall, temperature, humidity, discharge, elevation, land cover, soil type, etc.)
- **Output**: Binary classification (Flood/No Flood) with probability
- **Risk Thresholds**:
  - Low: < 0.35
  - Medium: 0.35 - 0.65
  - High: > 0.65

## Known Limitations (v1)

- Features are simulated approximations
- Limited to 50 pre-defined cities
- No real-time data updates yet
- Model trained on synthetic/historical data only
- Dashboard and server components in early development stage

## Next Steps (Phase 2)

- Integrate live weather APIs (OpenWeatherMap, WeatherAPI)
- River discharge data from government sources
- Improve model accuracy with real datasets
- Enhanced REST API endpoints and documentation
- Add time-series predictions (7-day forecast)
- Database integration for historical tracking