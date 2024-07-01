# MedScan v1.5 - Diagnóstico Inteligente de Rayos X de Tórax

MedScan es una aplicación innovadora que aprovecha el poder de la inteligencia artificial para analizar radiografías de tórax y detectar posibles enfermedades pulmonares. Con una interfaz intuitiva y resultados precisos, MedScan empodera a los profesionales de la salud para tomar decisiones informadas y brindar un mejor cuidado a sus pacientes.

![alt text](/assets/images/logo.png)
![alt text](/assets/images/image.png)
![alt text](/assets/images/image-1.png)
![alt text](/assets/images/image-2.png)

## Características Principales

- **Detección de Múltiples Enfermedades:** MedScan analiza radiografías de tórax y evalúa la probabilidad de presencia de diversas enfermedades pulmonares, como:

    - Cardiomegalia
    - Enfisema
    - Derrame pleural
    - Hernia
    - Infiltración
    - Masa
    - Nódulo
    - Atelectasia
    - Neumotórax
    - Engrosamiento pleural
    - Neumonía
    - Fibrosis
    - Edema
    - Consolidación

- **Interfaz Gráfica Intuitiva:**  Su interfaz amigable permite cargar imágenes fácilmente y visualizar los resultados en un formato claro y conciso.

- **Resultados en Tiempo Real:**  MedScan procesa las imágenes y muestra los resultados de manera rápida y eficiente, optimizando el flujo de trabajo clínico.

- **Modelo de IA Avanzado:**  La aplicación utiliza un modelo de inteligencia artificial entrenado para garantizar un alto nivel de precisión en el diagnóstico.

## Cómo Usar MedScan

1. **Instalación:** Asegúrate de tener Python 3.11 y PyQt5 instalados en tu sistema. Luego, clona este repositorio y navega a la carpeta del proyecto.

2. **Entorno Virtual (Recomendado):** Crea un entorno virtual e instala las dependencias:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
3. **Ejecución: Inicia la aplicación desde la terminal:**

    ```bash
    python interface.py
    ````
4. **Carga de Imágenes:** Haz clic en el botón "Upload Image" y selecciona la radiografía de tórax que deseas analizar.

5. **Diagnóstico:**  Una vez cargada la imagen, haz clic en el botón "Realizar Diagnóstico". MedScan procesará la imagen y mostrará los resultados en la columna derecha.

**Importante**
Las funcionalidades y la interfaz pueden cambiar en futuras versiones.
El modelo de IA proporcionado es solo para fines de demostración y no debe utilizarse para diagnósticos médicos reales.

**Contribuciones**
¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar MedScan, por favor abre un issue o envía un pull request.
