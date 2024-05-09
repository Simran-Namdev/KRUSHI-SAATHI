from flask import Flask, render_template, request, jsonify
import joblib
import pickle
import numpy as np
from flask import Blueprint

fertility = Blueprint('fertility', __name__)

def predict_soil_fertility(N, P, K, pH, EC, OC, S, Zn, Fe, Cu, Mn, B):
    with open('Models//fertility.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('Models//fertilityscaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    
    input_data = np.array([N, P, K, pH, EC, OC, S, Zn, Fe, Cu, Mn, B]).reshape(1, -1)
    input_data_scaled = scaler.transform(input_data)
    
    predicted_class = model.predict(input_data_scaled)[0]
    
    fertility_levels = {0: 'Less Fertile', 1: 'Fertile', 2: 'Highly Fertile'}
    predicted_fertility = fertility_levels[predicted_class]
    
    return predicted_fertility

@fertility.route('/')
def index():
    return render_template('fertility.html')

@fertility.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        pH = float(request.form['pH'])
        EC = float(request.form['EC'])
        OC = float(request.form['OC'])
        S = float(request.form['S'])
        Zn = float(request.form['Zn'])
        Fe = float(request.form['Fe'])
        Cu = float(request.form['Cu'])
        Mn = float(request.form['Mn'])
        B = float(request.form['B'])
        
        predicted_fertility = predict_soil_fertility(N, P, K, pH, EC, OC, S, Zn, Fe, Cu, Mn, B)
        
        return jsonify(predicted_fertility)

if __name__ == '__main__':
    fertility.run(debug=True)
