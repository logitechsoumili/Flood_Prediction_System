import joblib
import numpy as np

# Load trained model
model = joblib.load("../flood_model_v1.pkl")

sample_input = np.array([[293.09, 25.50, 39.81, 4408.71, 3.90, 7378.93, 1700.21,
                          0, 1,
                          0, 0, 1, 0, 0,
                          0, 0, 0, 0, 1]])

# Predict
prediction = model.predict(sample_input)[0]
probability = model.predict_proba(sample_input)

print("Prediction (0 = No Flood, 1 = Flood):", prediction)
print("Probabilities:", probability)