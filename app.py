from flask import Flask, request, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import io
import os
import boto3

# Disable TensorFlow OneDNN optimizations
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

app = Flask(__name__)

# S3 bucket information
BUCKET_NAME = 'mdlfinal2'
MODEL_KEY = 'model.h5'
LOCAL_MODEL_PATH = '/home/ubuntu/mdl/model.h5'

def download_model_from_s3():
    """Download model from S3 if it's not already present locally."""
    if not os.path.exists(LOCAL_MODEL_PATH):
        s3 = boto3.client('s3')
        try:
            os.makedirs(os.path.dirname(LOCAL_MODEL_PATH), exist_ok=True)
            s3.download_file(BUCKET_NAME, MODEL_KEY, LOCAL_MODEL_PATH)
            print("Model downloaded successfully from S3.")
        except Exception as e:
            print("Error downloading model from S3:", e)
            return False
    return True

# Download model from S3 and load it
model = None
if download_model_from_s3():
    try:
        model = load_model(LOCAL_MODEL_PATH)
        print("Model loaded successfully.")
    except Exception as e:
        print("Error loading model:", e)

# CIFAR-10 class labels
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
               'dog', 'frog', 'horse', 'ship', 'truck']

def preprocess_image(image):
    """
    Preprocess the input image to the required format for the CIFAR-10 model.
    Args:
        image (io.BytesIO): Image file in memory.
    Returns:
        np.array: Preprocessed image array.
    """
    image = load_img(image, target_size=(32, 32))
    image = img_to_array(image) / 255.0  # Normalize to [0, 1]
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

def predict_image_class(image):
    """
    Predict the class of an image using the CIFAR-10 model.
    Args:
        image (io.BytesIO): Image file in memory.
    Returns:
        str: Predicted class label.
    """
    processed_image = preprocess_image(image)
    predictions = model.predict(processed_image)
    predicted_class = class_names[np.argmax(predictions[0])]
    return predicted_class

@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        file = request.files["file"]
        image_bytes = io.BytesIO(file.read())
        predicted_class = predict_image_class(image_bytes)
        return f"Predicted class: {predicted_class}"
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Set port to 8080
