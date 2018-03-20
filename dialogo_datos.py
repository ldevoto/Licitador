from sys import argv as sysargv, exit as sysexit
from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, QStyle, QTableWidget, QGridLayout, QLabel, QVBoxLayout, QHeaderView, QAbstractItemView, QTableWidgetItem, QFrame, QGroupBox, QComboBox
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QModelIndex, QMimeData
from clases import Empresa, Contrato
from persistencia import licitacion_existente


class DialogoDatos(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dibujar_IU()
    
    def dibujar_IU(self):
        self.setWindowTitle("Ingreso de Datos")
        self.setWindowModality(Qt.ApplicationModal)
        self.setSizeGripEnabled(False)
        self.setContentsMargins(10, 10, 10, 10)

        self.nombre_licitacion = QLineEdit()
        self.nombre_licitacion_error = QLabel("*")
        self.espaciador = QLabel(" ")

        self.nombre_licitacion.setMaximumWidth(250)
        self.nombre_licitacion.setMinimumWidth(250)
        self.nombre_licitacion.textChanged.connect(self.marcar_nombre_licitacion_erroneo)
        self.nombre_licitacion.setToolTip("Nombre que quiera ponerle a la licitacion")
        self.nombre_licitacion_error.setStyleSheet("QLabel {color : red}")
        self.nombre_licitacion_error.setVisible(False)
        self.nombre_licitacion_error.setFixedWidth(10)
        self.espaciador.setFixedWidth(10)
        self.espaciador.setFixedHeight(0)

        boton_confirmar = QPushButton(QIcon("iconos/check.png"), "")
        boton_confirmar.clicked.connect(self.accept)
        boton_confirmar.setDefault(True)
        boton_confirmar.setMinimumSize(50, 10)
        boton_cancelar = QPushButton(QIcon("iconos/cancel.png"), "")
        boton_cancelar.clicked.connect(self.reject)
        boton_cancelar.setMinimumSize(50, 10)

        grilla = QGridLayout()
        grilla.setColumnMinimumWidth(1, 20)
        grilla.addWidget(QLabel("Nombre"), 0, 0)
        grilla.addWidget(self.nombre_licitacion_error, 0, 1, Qt.AlignTop | Qt.AlignRight)
        grilla.addWidget(self.nombre_licitacion, 0, 2)
        grilla.addWidget(self.espaciador, 1, 1)
        marco = QGroupBox("Licitación")
        marco.setLayout(grilla)

        caja_horizontal = QHBoxLayout()
        caja_horizontal.addStretch(1)
        caja_horizontal.addWidget(boton_cancelar)
        caja_horizontal.addStretch(5)
        caja_horizontal.addWidget(boton_confirmar)
        caja_horizontal.addStretch(1)
        caja_horizontal.setContentsMargins(10, 10, 10, 0)
        formulario = QFormLayout(self)
        formulario.addRow(marco)
        formulario.addRow(caja_horizontal)
        self.resize(self.sizeHint())
        self.setMinimumSize(self.sizeHint())
        self.setMaximumSize(self.sizeHint())
    
    def accept(self):
        self.marcar_campos_erroneos()
        if len(self.nombre_licitacion.text()) == 0 or self.nombre_licitacion.text().isspace() or licitacion_existente("Licitaciones.db", self.nombre_licitacion.text().strip()):
            self.nombre_licitacion.setFocus()
        else:
            super().accept()
    
    def marcar_campos_erroneos(self):
        self.marcar_nombre_licitacion_erroneo()
    
    def marcar_nombre_licitacion_erroneo(self):
        if len(self.nombre_licitacion.text()) == 0 or self.nombre_licitacion.text().isspace() or licitacion_existente("Licitaciones.db", self.nombre_licitacion.text().strip()):
            self.nombre_licitacion_error.setVisible(True)
        else:
            self.nombre_licitacion_error.setVisible(False)
    
    def obtener_nombre_licitacion(self):
        return self.nombre_licitacion.text().strip()


class DialogoCargaDatos(QDialog):
    def __init__(self, parent=None, licitaciones=None):
        super().__init__(parent)
        self.dibujar_IU()
        self.licitaciones = licitaciones
        if self.licitaciones != None:
            self.cargar_licitaciones()
    
    def dibujar_IU(self):
        self.setWindowTitle("Selección de Licitación")
        self.setWindowModality(Qt.ApplicationModal)
        self.setSizeGripEnabled(False)
        self.setContentsMargins(10, 10, 10, 10)

        self.nombre_licitacion = QComboBox()
        self.nombre_licitacion_error = QLabel("*")
        self.espaciador = QLabel(" ")

        self.nombre_licitacion.setMaximumWidth(250)
        self.nombre_licitacion.setMinimumWidth(250)
        #self.nombre_licitacion.textChanged.connect(self.marcar_nombre_licitacion_erroneo)
        self.nombre_licitacion.setToolTip("Nombre de la licitación a cargar")
        self.nombre_licitacion_error.setStyleSheet("QLabel {color : red}")
        self.nombre_licitacion_error.setVisible(False)
        self.nombre_licitacion_error.setFixedWidth(10)
        self.espaciador.setFixedWidth(10)
        self.espaciador.setFixedHeight(0)

        boton_confirmar = QPushButton(QIcon("iconos/check.png"), "")
        boton_confirmar.clicked.connect(self.accept)
        boton_confirmar.setDefault(True)
        boton_confirmar.setMinimumSize(50, 10)
        boton_cancelar = QPushButton(QIcon("iconos/cancel.png"), "")
        boton_cancelar.clicked.connect(self.reject)
        boton_cancelar.setMinimumSize(50, 10)

        grilla = QGridLayout()
        grilla.setColumnMinimumWidth(1, 20)
        grilla.addWidget(QLabel("Nombre"), 0, 0)
        grilla.addWidget(self.nombre_licitacion_error, 0, 1, Qt.AlignTop | Qt.AlignRight)
        grilla.addWidget(self.nombre_licitacion, 0, 2)
        grilla.addWidget(self.espaciador, 1, 1)
        marco = QGroupBox("Licitación")
        marco.setLayout(grilla)

        caja_horizontal = QHBoxLayout()
        caja_horizontal.addStretch(1)
        caja_horizontal.addWidget(boton_cancelar)
        caja_horizontal.addStretch(5)
        caja_horizontal.addWidget(boton_confirmar)
        caja_horizontal.addStretch(1)
        caja_horizontal.setContentsMargins(10, 10, 10, 0)
        formulario = QFormLayout(self)
        formulario.addRow(marco)
        formulario.addRow(caja_horizontal)
        self.resize(self.sizeHint())
        self.setMinimumSize(self.sizeHint())
        self.setMaximumSize(self.sizeHint())
    
    def accept(self):
        self.marcar_campos_erroneos()
        if len(self.nombre_licitacion.currentText()) == 0 or self.nombre_licitacion.currentText().isspace():
            self.nombre_licitacion.setFocus()
        else:
            super().accept()
    
    def marcar_campos_erroneos(self):
        self.marcar_nombre_licitacion_erroneo()
    
    def marcar_nombre_licitacion_erroneo(self):
        if len(self.nombre_licitacion.currentText()) == 0 or self.nombre_licitacion.currentText().isspace():
            self.nombre_licitacion_error.setVisible(True)
        else:
            self.nombre_licitacion_error.setVisible(False)

    def cargar_licitaciones(self):
        for licitacion in self.licitaciones:
            self.nombre_licitacion.addItem(licitacion["nombre"] + " (" + licitacion["fecha"] + ")" , licitacion["nombre"])

    def obtener_nombre_licitacion(self):
        return self.nombre_licitacion.currentData()
    
if __name__ == '__main__':
    app = QApplication(sysargv)
    ex = DialogoDatos()
    if ex.exec() == QDialog.Accepted:
        print(ex.obtener_nombre_licitacion())