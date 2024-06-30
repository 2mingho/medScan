import sys
import os
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox, QDialog, QScrollArea, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

from nuevo_modelo import predict_image, interpret_predictions, disease_columns

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About MedScan")
        layout = QVBoxLayout()
        info_label = QLabel("MedScan v1.2\nThis is an alpha version for improvemnts and testing\nCreadores: Grupo H - SIC\nModelo: All_classification_model.h5")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        self.setLayout(layout)

class MedScanApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MedScan")
        self.setGeometry(100, 100, 700, 400)  # Ventana más ancha
        self.setStyleSheet("background-color: #EEEDEB;")
        self.img = None

        # Crear la etiqueta de resultados (antes de initUI)
        self.result_label = QLabel(self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("color: white;")
        self.result_label.setWordWrap(True)

        self.initUI()

    def show_about_dialog(self):
        dialog = AboutDialog()
        x = self.x() - (self.width() - dialog.width()) // 2
        y = self.y() - (self.height() - dialog.height()) // 2
        dialog.setGeometry(x, y, 200, 300)
        dialog.exec_()

    def reset_app(self):
        self.img = None
        self.img_label.clear()
        
        # Limpiar el layout de resultados (si existe)
        for i in reversed(range(self.results_layout.count())):
            self.results_layout.itemAt(i).widget().setParent(None)

        self.upload_button.setText("Upload Image")
        self.upload_button.setStyleSheet(
            "background-color: #939185; color: #EEEDEB; border: none;border-radius: 15px; width: 75px;height: 40px;font-weight: 900;"
        )
        self.diagnose_button.hide()

    def upload_image(self):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Select an image", "",
            "Image files (*.jpg *.jpeg *.png);;All files (*)", options=options
        )
        
        if filepath:
            self.img = Image.open(filepath)
            pixmap = QPixmap(filepath)
            pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
            self.img_label.setPixmap(pixmap)
            self.upload_button.setText("Upload New Image")
            self.upload_button.setStyleSheet("background-color: #E6B9A6; color: #2F3645; border:none; border-radius:15px; width:75px; height:40px; font-weight:900;")
            self.diagnose_button.show()

    def perform_diagnosis(self):
        self.result_label.setText("Analizando...")
        QTimer.singleShot(3000, self.show_diagnosis_result)

    def initUI(self):
        layout = QGridLayout()
        self.setGeometry(100, 100, 700, 400)  

        # Estilos base para los botones
        button_style = """
            QPushButton {
                background-color: #939185;
                color: #EEEDEB;
                border: none;
                border-radius: 15px;
                width: 75px;
                height: 40px;
                font-weight: 900;
            }
            QPushButton:hover {
                background-color: #D1C9C2;
            }
        """

        # Columna izquierda (botones, imagen, diagnóstico)
        left_column = QVBoxLayout()
        left_column.setSpacing(10)  

        # Layout horizontal para los botones superiores
        top_buttons_layout = QHBoxLayout()

        # Botón "Reset"
        reset_button = QPushButton("Reset", self)
        reset_button.clicked.connect(self.reset_app)
        reset_button.setStyleSheet(
            button_style + "QPushButton { background-color: #EF9C66; color: #2F3645; }"
        )
        top_buttons_layout.addWidget(reset_button)

        # Botón para cargar imagen
        self.upload_button = QPushButton("Upload Image", self)
        self.upload_button.clicked.connect(self.upload_image)
        self.upload_button.setStyleSheet(
            button_style + "QPushButton { background-color: #2F3645; color: #EEEDEB; }"
        )
        top_buttons_layout.addWidget(self.upload_button)
        
        # Etiqueta para mostrar la imagen (tamaño fijo 300x300)
        self.img_label = QLabel(self)
        self.img_label.setFixedSize(300, 300)  
        self.img_label.setStyleSheet("background-color: #EEEDEB; border: solid 1px gray; border-radius: 15px;")
        self.img_label.setAlignment(Qt.AlignCenter)

        # Botón para realizar el diagnóstico (inicialmente oculto)
        self.diagnose_button = QPushButton("Realizar Diagnóstico", self)
        self.diagnose_button.clicked.connect(self.perform_diagnosis)
        self.diagnose_button.setStyleSheet(button_style + "QPushButton { background-color: #95D2B3; color: #2F3645; }")
        self.diagnose_button.hide()

        left_column.addLayout(top_buttons_layout)
        left_column.addWidget(self.img_label)
        left_column.addWidget(self.diagnose_button)
        layout.addLayout(left_column, 0, 0, 3, 1)  # Expandir a 3 filas

        # Columna derecha (resultados, botón About)
        right_column = QVBoxLayout()
        right_column.setSpacing(10)  
        
        # Título "Resultados"
        results_title = QLabel("Resultados")
        results_title.setAlignment(Qt.AlignCenter)  # Centrar el título
        results_title.setStyleSheet("font-weight: bold; font-size: 16px;")  # Estilo para el título
        right_column.addWidget(results_title)

        # Widget contenedor para las pills (¡aquí está el cambio!)
        results_widget = QWidget()
        self.results_layout = QGridLayout(results_widget)
        self.results_layout.setAlignment(Qt.AlignTop)
        
        # Agregar el widget contenedor al layout de la columna derecha
        right_column.addWidget(results_widget)
        
        # Botón "About"
        about_button = QPushButton("About", self)
        about_button.clicked.connect(self.show_about_dialog)
        about_button.setStyleSheet(button_style)
        right_column.addWidget(about_button)

        # Alinear el botón "About" al final
        right_column.addStretch(1)
        layout.addLayout(right_column, 0, 1)

        self.setLayout(layout)

        # Hovers para los botones
        for button in [self.upload_button, self.diagnose_button, reset_button, about_button]:
            button.setStyleSheet(
                button.styleSheet() + 
                """
                QPushButton:hover {
                    background-color: #D1C9C2; color: #2F3645;
                }
                """
            )
            
        # Evitar que la ventana se pueda redimensionar
        self.setFixedSize(self.size())

    def show_diagnosis_result(self):
        if self.img is not None:
            # Guardar la imagen temporalmente
            temp_image_path = "temp_image.png"
            self.img.save(temp_image_path)

            # Importar el modelo desde nuevo_modelo.py
            from nuevo_modelo import model 

            # Obtener predicciones y resultados
            predictions = predict_image(model, temp_image_path)  
            results = interpret_predictions(predictions)

            # Limpiar el layout de resultados anterior (si existe)
            for i in reversed(range(self.results_layout.count())):
                self.results_layout.itemAt(i).widget().setParent(None)

            # Crear y agregar las pills de resultados en dos columnas
            row = 0
            col = 0
            for i, disease in enumerate(disease_columns):
                result = results[0][i]
                pill = QPushButton(disease, self)
                pill.setFixedSize(150, 20)  
                pill.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {"#FFCCCB" if result == 1 else "#90EE90"};
                        color: black;
                        border: none;
                        border-radius: 10px; 
                    }}
                    QPushButton:hover {{
                        background-color: {"#FF9999" if result == 1 else "#66CC66"};
                    }}
                """)

                # Usar directamente self.results_layout (que ahora es QGridLayout)
                self.results_layout.addWidget(pill, row, col)  

                col += 1
                if col == 2:  
                    col = 0
                    row += 1

            # Eliminar la imagen temporal
            os.remove(temp_image_path)
        else:
            QMessageBox.warning(self, "No Image", "Please upload an image first.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MedScanApp()
    window.show()
    sys.exit(app.exec_())