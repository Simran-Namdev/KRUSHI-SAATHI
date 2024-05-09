from flask import Flask, request, jsonify, render_template
import tensorflow as tf
from keras.preprocessing import image
from keras.utils import img_to_array
import keras.utils as image
import cv2
import numpy as np
import re
import os
from flask import Blueprint

disease = Blueprint('disease', __name__)

class_labels = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 
                'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy', 
                'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 
                'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 
                'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 
                'Peach___Bacterial_spot', 'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 
                'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 
                'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 
                'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 
                'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 
                'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']

# Create cleaned version of class labels
plant_list = [" ".join(filter(None, i.split('_'))) for i in class_labels]
pattern = r'\(.*?\)'
class_labels = [re.sub(pattern, '', item).strip() for item in plant_list]

def predict(model, img_path, class_labels):
    print("Predict function called")
    img = image.load_img(img_path)
    img_array = img_to_array(img)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    resize = tf.image.resize(tf.convert_to_tensor([img_array]), (224, 224))
    yhat = model.predict(resize / 255.0)
    predicted_class_index = np.argmax(yhat)
    predicted_class_label = class_labels[predicted_class_index]
    print("Predicted class:", predicted_class_label)
    return predicted_class_label

new_model = tf.keras.models.load_model('Models\DiseaseDect.keras')

@disease.route('/')
def index():
    return render_template('disease.html')

@disease.route('/predict', methods=['POST'])
def predict_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        img_path = 'temp.jpg'  # Save the file temporarily
        file.save(img_path)
        result = predict(model=new_model, img_path=img_path, class_labels=class_labels)
        os.remove(img_path)  # Remove the temporary file
        print("Result:", result)
        return jsonify({'result': result})

if __name__ == '__main__':
    disease.run(debug=True)