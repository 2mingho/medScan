import sys
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

from modelo import predict_disease  

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
        self.setGeometry(100, 100, 350, 400)
        self.setStyleSheet("background-color: #EEEDEB;")
        self.img = None

        self.initUI()

    def show_about_dialog(self):
        dialog = AboutDialog()
        # Centrar el diálogo en la ventana principal
        x = self.x() - (self.width() - dialog.width()) // 2
        y = self.y() - (self.height() - dialog.height()) // 2
        dialog.setGeometry(x, y, 200, 300)
        dialog.exec_()  

    def reset_app(self):
        self.img = None
        self.img_label.clear()
        self.result_label.clear()
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
        self.result_label.setStyleSheet("color: blue;")

        QTimer.singleShot(3000, self.show_diagnosis_result)

    def show_diagnosis_result(self):
        if self.img is not None:
            prediction = predict_disease(self.img)
            result_text = f"Diagnóstico: Enfermedad \n{prediction}" if prediction >= 0.12 else f"Diagnóstico: No Enfermedad \n{prediction}"
            result_color = "red" if prediction >= 0.12 else "green"
            self.result_label.setText(result_text)
            self.result_label.setStyleSheet(f"color: {result_color}; border:none; border-radius:15px; width:75px; height:40px; font-weight:900;")
        else:
            QMessageBox.warning(self, "No Image", "Please upload an image first.")

    def initUI(self):
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

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

        # Botón "Reset"
        reset_button = QPushButton("Reset", self)
        reset_button.clicked.connect(self.reset_app)
        reset_button.setStyleSheet(
            button_style + "QPushButton { background-color: #EF9C66; color: #2F3645; }"  # Estilo específico para Reset
        )
        button_layout.addWidget(reset_button)

        # Botón para cargar imagen
        self.upload_button = QPushButton("Upload Image", self)
        self.upload_button.clicked.connect(self.upload_image)
        self.upload_button.setStyleSheet(
            button_style + "QPushButton { background-color: #2F3645; color: #EEEDEB; }"                                 
        )  # Usar el estilo base
        button_layout.addWidget(self.upload_button)

        layout.addLayout(button_layout)

        # Etiqueta para mostrar la imagen
        self.img_label = QLabel(self)
        self.img_label.setStyleSheet("background-color: #EEEDEB;border:solid 1px gray; border-radius: 15px;")
        self.img_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.img_label)

        # Botón para realizar el diagnóstico (inicialmente oculto)
        self.diagnose_button = QPushButton("Realizar Diagnóstico", self)
        self.diagnose_button.clicked.connect(self.perform_diagnosis)
        self.diagnose_button.setStyleSheet(button_style + "QPushButton { background-color: #95D2B3; color: #2F3645; }")  # Usar el estilo base
        self.diagnose_button.hide()
        layout.addWidget(self.diagnose_button)

        # Etiqueta para mostrar el resultado
        self.result_label = QLabel(self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("color: white;")
        layout.addWidget(self.result_label)

        # Botón "About"
        about_button = QPushButton("About", self)
        about_button.clicked.connect(self.show_about_dialog)
        about_button.setStyleSheet(button_style)
        layout.addWidget(about_button)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MedScanApp()
    window.show()
    sys.exit(app.exec_())
