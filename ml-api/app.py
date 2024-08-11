from flask import Flask, jsonify
import pickle
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

# Load the trained Prophet model
with open('prophet_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/predict', methods=['GET'])
def predict_replicas():
    # Get the current time
    current_time = datetime.now()

    # Calculate the future timestamp for the next 30-minute interval (e.g., 1:30 PM)
    next_interval_time = current_time + timedelta(minutes=(30 - current_time.minute % 30))

    # Create a future DataFrame with the target timestamp
    future = pd.DataFrame({
        'ds': [next_interval_time]
    })

    # Make prediction
    forecast = model.predict(future)

    # Extract the predicted replicas count and round it to the nearest integer
    predicted_replicas = int(round(forecast['yhat'].iloc[-1]))

    return jsonify({'timestamp': next_interval_time.isoformat(), 'predicted_replicas': predicted_replicas})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
