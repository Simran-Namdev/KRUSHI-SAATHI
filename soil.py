from flask import Flask, render_template, request
import tensorflow as tf
from keras.preprocessing import image
import numpy as np
import tensorflow_hub as hub
from flask import Blueprint
import pickle
soil = Blueprint('soil', __name__)

def load_mobilenetv2_layer(model_handle):
    return hub.KerasLayer(model_handle, trainable=False)

def load_custom_model(model_path, model_handle):
    custom_objects = {'KerasLayer': load_mobilenetv2_layer(model_handle)}
    return tf.keras.models.load_model(model_path, custom_objects=custom_objects)

class_names = ['Alluvial soil', 'Black Soil', 'Clay soil', 'Red soil']
model_path = 'Models/soilclass.h5'  
model_handle = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/4"
model = load_custom_model(model_path, model_handle)

def load_and_preprocess_image(image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    return img_array

def predict_image(model, image_path):
    img_array = load_and_preprocess_image(image_path)
    predictions = model.predict(img_array)
    return predictions

def print_predictions(predictions, class_names):
    predicted_class_index = np.argmax(predictions)
    predicted_class_name = class_names[predicted_class_index]
    confidence = predictions[0][predicted_class_index] * 100

    return f"Predicted class: {predicted_class_name}, Confidence: {confidence:.2f}%"

@soil.route('/')
def index():
    return render_template('soilclass.html')

@soil.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        file_path = 'static/uploaded_image.jpeg'
        file.save(file_path)
        predictions = predict_image(model, file_path)
        result = print_predictions(predictions, class_names)
        return result

if __name__ == '__main__':
    soil.run(debug=True)
