from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
from flask import Blueprint

fertilizer = Blueprint('fertilizer', __name__)

# Load label encoders, scaler, and model
label_encoder_soil_type = joblib.load('models/label_encoder_soil_type.pkl')
label_encoder_crop_type = joblib.load('models/label_encoder_crop_type.pkl')
label_encoder_fertilizer_name = joblib.load('models/label_encoder_fertilizer_name.pkl')
scaler = joblib.load('Models/scaler.pkl')
naive_bayes_model = joblib.load('Models/fertilizer.pkl')

# Define options for soil type and crop type
soil_type_options = ['Loamy', 'Sandy', 'Clayey', 'Black', 'Red']
crop_type_options = ['Sugarcane', 'Cotton', 'Millets', 'Paddy', 'Pulses', 'Wheat', 'Tobacco', 'Barley', 'Oil seeds', 'Ground Nuts', 'Maize']

@fertilizer.route('/')
def index():
    return render_template('fertilizer.html', soil_type_options=soil_type_options, crop_type_options=crop_type_options)

@fertilizer.route('/recommend', methods=['POST'])
def recommend():
    if request.method == 'POST':
        temperature = int(request.form['temperature'])
        humidity = int(request.form['humidity'])
        moisture = int(request.form['moisture'])
        soil_type = request.form['soil_type']
        crop_type = request.form['crop_type']
        nitrogen = int(request.form['nitrogen'])
        potassium = int(request.form['potassium'])
        phosphorous = int(request.form['phosphorous'])

        # Encode soil type and crop type
        soil_type_encoded = label_encoder_soil_type.transform([soil_type])[0]
        crop_type_encoded = label_encoder_crop_type.transform([crop_type])[0]

        # Transform user input using scaler
        user_input = [[temperature, humidity, moisture, soil_type_encoded, crop_type_encoded, nitrogen, potassium, phosphorous]]
        X_user = scaler.transform(user_input)

        # Predict the fertilizer
        fertilizer_index = naive_bayes_model.predict(X_user)[0]

        # Decode the fertilizer name
        recommended_fertilizer = label_encoder_fertilizer_name.inverse_transform([fertilizer_index])[0]

        return jsonify({'recommended_fertilizer': recommended_fertilizer})

if __name__ == '__main__':
    fertilizer.run(debug=True)
