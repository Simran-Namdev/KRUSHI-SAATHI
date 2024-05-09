@app.route('/predict', methods=['POST'])
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