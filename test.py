import os
from PIL import Image
from modelo import predict_disease

def analyze_images(folder_path):
    enfermedad_count = 0
    no_enfermedad_count = 0

    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            img_path = os.path.join(folder_path, filename)
            try:
                img = Image.open(img_path)
                prediction = predict_disease(img)
                if prediction >= 0.12:
                    enfermedad_count += 1
                else:
                    no_enfermedad_count += 1
            except Exception as e:
                print(f"Error al procesar la imagen {filename}: {e}")

    return enfermedad_count, no_enfermedad_count

if __name__ == "__main__":
    folder_path = input("Ingrese la ruta de la carpeta con las imágenes: ")
    enfermedad_count, no_enfermedad_count = analyze_images(folder_path)

    print("\nResultados:")
    print(f"Enfermedad: {enfermedad_count}")
    print(f"No Enfermedad: {no_enfermedad_count}")
