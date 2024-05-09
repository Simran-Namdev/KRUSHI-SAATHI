import pickle
import numpy as np

def predict_soil_fertility(N, P, K, pH, EC, OC, S, Zn, Fe, Cu, Mn, B):
    # Load the saved model and scaler
    with open('random_forest_model.pkl', 'rb') as f:  # Update filename to match your saved model
        model = pickle.load(f)
    
    with open('scaler.pkl', 'rb') as f:  # Update filename to match your saved scaler
        scaler = pickle.load(f)
    
    # Scale the input data
    input_data = np.array([N, P, K, pH, EC, OC, S, Zn, Fe, Cu, Mn, B]).reshape(1, -1)
    input_data_scaled = scaler.transform(input_data)
    
    # Predict the fertility class
    predicted_class = model.predict(input_data_scaled)[0]
    
    # Map the predicted class to fertility levels
    fertility_levels = {0: 'Less Fertile', 1: 'Fertile', 2: 'Highly Fertile'}
    predicted_fertility = fertility_levels[predicted_class]
    
    return predicted_fertility

# Example usage
N = float(input("Enter ratio of Nitrogen (NH4+) content in soil: "))
P = float(input("Enter ratio of Phosphorous (P) content in soil: "))
K = float(input("Enter ratio of Potassium (K) content in soil: "))
pH = float(input("Enter soil acidity (pH): "))
EC = float(input("Enter electrical conductivity: "))
OC = float(input("Enter organic carbon: "))
S = float(input("Enter sulfur (S): "))
Zn = float(input("Enter Zinc (Zn): "))
Fe = float(input("Enter Iron (Fe): "))
Cu = float(input("Enter Copper (Cu): "))
Mn = float(input("Enter Manganese (Mn): "))
B = float(input("Enter Boron (B): "))

predicted_fertility = predict_soil_fertility(N, P, K, pH, EC, OC, S, Zn, Fe, Cu, Mn, B)
print("Predicted Soil Fertility Level:", predicted_fertility)
