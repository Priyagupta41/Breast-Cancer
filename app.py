from flask import Flask, request, render_template, jsonify, send_from_directory
import os
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
from flask_cors import CORS

# Initialize the Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
CORS(app, resources={r"/*": {"origins": "*"}})

# Load the trained model
MODEL_PATH = 'Breast_Cancer_model.h5'
model = load_model(MODEL_PATH)

# Define the class labels and stages
CLASS_LABELS = ['Benign', 'Malignant']  # Replace with actual class names
STAGE_LABELS = {
    'Benign': 'No cancer or early-stage lesion detected.',
    'Malignant': 'Advanced stage detected; consult a specialist.'
}

# Function to preprocess the uploaded image
def preprocess_image(image_path):
    img = load_img(image_path, target_size=(224, 224))  # Resize image
    img_array = img_to_array(img) / 255.0  # Normalize the image
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

@app.route('/detect')
def index():
    return render_template('detect.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded!'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected!'})

    if file:
        # Save the file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Preprocess the image
        img_array = preprocess_image(file_path)

        # Make prediction
        prediction = model.predict(img_array)
        predicted_class = CLASS_LABELS[int(prediction[0] > 0.5)]  # Adjust for binary classification
        stage_info = STAGE_LABELS[predicted_class]  # Retrieve stage information

        # Return prediction and file path for frontend display
        return jsonify({
            'class': predicted_class,
            'stage_info': stage_info,
            'image_url': f'{file.filename}'
        })

if __name__ == '__main__':
    # Ensure the upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True, host='0.0.0.0') 
