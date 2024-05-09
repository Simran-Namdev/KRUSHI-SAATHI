import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib

# Load the dataset
df = pd.read_csv('Fertilizer Prediction.csv')  # Replace 'your_dataset.csv' with your dataset filename

# Load the label encoders for Soil Type, Crop Type, and Fertilizer Name
label_encoder_soil_type = joblib.load('label_encoder_soil_type.pkl')
label_encoder_crop_type = joblib.load('label_encoder_crop_type.pkl')
label_encoder_fertilizer_name = joblib.load('label_encoder_fertilizer_name.pkl')

# Load the scaler
scaler = joblib.load('scaler.pkl')

# Load the Naive Bayes model
naive_bayes_model = joblib.load('naive_bayes_model.pkl')

# Define options for soil type and crop type
soil_type_options = ['Loamy', 'Sandy', 'Clayey', 'Black', 'Red']
crop_type_options = ['Sugarcane', 'Cotton', 'Millets', 'Paddy', 'Pulses', 'Wheat', 'Tobacco', 'Barley', 'Oil seeds', 'Ground Nuts', 'Maize']

# Function to recommend fertilizer based on user input
def recommend_fertilizer(temperature, humidity, moisture, soil_type, crop_type, nitrogen, potassium, phosphorous):
    # Encode soil type and crop type
    soil_type_encoded = label_encoder_soil_type.transform([soil_type])[0]
    crop_type_encoded = label_encoder_crop_type.transform([crop_type])[0]
    
    # Transform user input using scaler
    user_input = [[temperature, humidity, moisture, soil_type_encoded, crop_type_encoded, nitrogen, potassium, phosphorous]]
    X_user = scaler.transform(user_input)
    
    # Predict the fertilizer
    fertilizer_index = naive_bayes_model.predict(X_user)[0]
    
    # Decode the fertilizer name
    fertilizer_name = label_encoder_fertilizer_name.inverse_transform([fertilizer_index])[0]
    
    return fertilizer_name

# Get user input
temperature = int(input("Enter temperature: "))
humidity = int(input("Enter humidity: "))
moisture = int(input("Enter moisture: "))
print("Select Soil Type:")
for i, option in enumerate(soil_type_options):
    print(f"{i+1}. {option}")
soil_type_choice = int(input("Enter your choice: "))
soil_type = soil_type_options[soil_type_choice - 1]
print("Select Crop Type:")
for i, option in enumerate(crop_type_options):
    print(f"{i+1}. {option}")
crop_type_choice = int(input("Enter your choice: "))
crop_type = crop_type_options[crop_type_choice - 1]
nitrogen = int(input("Enter nitrogen level: "))
potassium = int(input("Enter potassium level: "))
phosphorous = int(input("Enter phosphorous level: "))

# Get fertilizer recommendation
recommended_fertilizer = recommend_fertilizer(temperature, humidity, moisture, soil_type, crop_type, nitrogen, potassium, phosphorous)

print("Recommended fertilizer:", recommended_fertilizer)
