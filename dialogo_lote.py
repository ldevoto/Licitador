from sys import argv as sysargv, exit as sysexit
from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, QStyle
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtCore import Qt
from clases import Lote

class DialogoLote(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dibujar_IU()
    
    def dibujar_IU(self):
        self.setWindowTitle("Lote")
        self.setWindowModality(Qt.ApplicationModal)
        self.setSizeGripEnabled(False)
        self.id = QLineEdit()
        self.descripcion = QLineEdit()
        self.facturacion_media_anual = QLineEdit()
        self.recursos_financieros = QLineEdit()
        self.experiencia = QLineEdit()
        self.id.setValidator(QIntValidator(1, 100))
        self.facturacion_media_anual.setValidator(QDoubleValidator(0, 999999999, 3))
        self.recursos_financieros.setValidator(QDoubleValidator(0, 999999999, 3))
        self.experiencia.setValidator(QDoubleValidator(0, 999999999, 3))
        boton_confirmar = QPushButton(QIcon("iconos/check.png"), "")
        boton_confirmar.clicked.connect(self.accept)
        boton_confirmar.setDefault(True)
        boton_confirmar.setMinimumSize(50, 10)
        boton_cancelar = QPushButton(QIcon("iconos/cancel.png"), "")
        boton_cancelar.clicked.connect(self.reject)
        boton_cancelar.setMinimumSize(50, 10)
        caja_horizontal = QHBoxLayout()
        caja_horizontal.addStretch(1)
        caja_horizontal.addWidget(boton_cancelar)
        caja_horizontal.addStretch(5)
        caja_horizontal.addWidget(boton_confirmar)
        caja_horizontal.addStretch(1)
        caja_horizontal.setContentsMargins(10, 10, 10, 0)
        formulario = QFormLayout(self)
        formulario.addRow("Id", self.id)
        formulario.addRow("Descripción", self.descripcion)
        formulario.addRow("Facturación Media Anual", self.facturacion_media_anual)
        formulario.addRow("Recursos Financieros", self.recursos_financieros)
        formulario.addRow("Experiencia", self.experiencia)
        formulario.addRow(caja_horizontal)
        self.setMinimumSize(self.sizeHint())
        self.setMaximumSize(self.sizeHint())
    
    def accept(self):
        if len(self.id.text()) == 0:
            #self.id.setStyleSheet("QLineEdit { border-color: red; border-style: solid; border-width: 1px}")
            self.id.setFocus()
        elif len(self.facturacion_media_anual.text()) == 0:
            self.facturacion_media_anual.setFocus()
        elif len(self.recursos_financieros.text()) == 0:
            self.recursos_financieros.setFocus()
        elif len(self.experiencia.text()) == 0:
            self.experiencia.setFocus()
        else:
            super().accept()

    def obtener_lote(self):
        lote = Lote(int(self.id.text()), float(self.facturacion_media_anual.text()), float(self.recursos_financieros.text()), float(self.experiencia.text()))
        if len(self.descripcion.text()) != 0:
            lote.descripcion = self.descripcion.text()
        return lote

    
if __name__ == '__main__':
    app = QApplication(sysargv)
    ex = DialogoLote()
    if ex.exec() == QDialog.Accepted:
        lote = ex.obtener_lote()
        print(lote.id)
        print(lote.descripcion)
    ex.deleteLater()
    #sysexit(app.exec_())