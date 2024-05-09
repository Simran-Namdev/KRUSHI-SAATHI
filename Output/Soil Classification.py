import tensorflow as tf
from keras.preprocessing import image
import numpy as np
import tensorflow_hub as hub

def load_mobilenetv2_layer(model_handle):
    return hub.KerasLayer(model_handle, trainable=False)
def load_custom_model(model_path, model_handle):
    custom_objects = {'KerasLayer': load_mobilenetv2_layer(model_handle)}
    return tf.keras.models.load_model(model_path, custom_objects=custom_objects)

class_names = ['Alluvial soil', 'Black Soil', 'Clay soil', 'Red soil']

if __name__ == "__main__":
    model_path = 'soil.h5'  
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

        print(f"Predicted class: {predicted_class_name}")
    test_image_path = 'D:\\EPICS\\SoilClass\\Dataset\\Train\\Black Soil\\Black_1.jpg'  

    predictions = predict_image(model, test_image_path)
    print_predictions(predictions, class_names)
