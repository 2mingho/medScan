import numpy as np
from tensorflow.keras.models import load_model

def preprocess_image(img):
    img = img.convert("L")
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=(0, -1))

model_path = 'assets\\models\\All_classification_model.h5'
loaded_model = load_model(model_path)

def predict_disease(img):
    preprocessed_image = preprocess_image(img)
    prediction = loaded_model.predict(preprocessed_image)[0][0]
    return prediction