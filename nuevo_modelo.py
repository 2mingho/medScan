import numpy as np
import cv2
from tensorflow.keras.models import load_model

# Cargar el modelo entrenado
model = load_model('assets\\models\\All_classification_Attempt_3.h5')

# Preprocesar la imagen
def preprocess_image(image_path, target_size=(224, 224)):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is not None:
        img = cv2.resize(img, target_size)
        img = img / 255.0
        img = np.expand_dims(img, axis=-1)
        img = np.expand_dims(img, axis=0)
    return img

# Realizar la predicción
def predict_image(model, image_path):
    img = preprocess_image(image_path)
    if img is not None:
        prediction = model.predict(img)
        return prediction
    else:
        print(f"Image not found or unable to read: {image_path}")
        return None

# Interpretar las predicciones
def interpret_predictions(predictions, threshold=0.5):
    results = (predictions >= threshold).astype(int)
    return results

# Definir las columnas de las enfermedades
disease_columns = [
    'Cardiomegaly', 'Emphysema', 'Effusion', 'Hernia', 'Infiltration',
    'Mass', 'Nodule', 'Atelectasis', 'Pneumothorax', 'Pleural_Thickening',
    'Pneumonia', 'Fibrosis', 'Edema', 'Consolidation'
]

# Ruta de la imagen de prueba
image_path = 'assets\\testing\\archive\\chest_xray\\test\\NORMAL\\NORMAL-4512-0001.jpeg'

# Realizar la predicción
predictions = predict_image(model, image_path)

# Interpretar y mostrar los resultados
if predictions is not None:
    results = interpret_predictions(predictions)
    for i, disease in enumerate(disease_columns):
        print(f"{disease}: {'Positive' if results[0][i] == 1 else 'Negative'}")

# print(predictions)