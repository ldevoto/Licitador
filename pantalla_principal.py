from sys import argv as sysargv, exit as sysexit
from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, 
                             QStyle, QTableWidget, QGridLayout, QLabel, QVBoxLayout, QHeaderView, 
                             QAbstractItemView, QTableWidgetItem, QAbstractScrollArea, QFrame, 
                             QMainWindow, QWidget, QLayout, QMessageBox, QGroupBox)
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QModelIndex, QMimeData
from clases import Asociacion, Empresa, Contrato
from dialogo_empresa import DialogoEmpresa

class PantallaPrincipal(QDialog):
    A_CREAR = 1
    A_CARGAR = 2
    A_SALIR = 0
    A_INDEFINIDO = 99

    def __init__(self):
        super().__init__()
        self.dibujar_IU()
        self.accion = PantallaPrincipal.A_INDEFINIDO

    def dibujar_IU(self):
        self.setWindowTitle("LicitaSoft")

        boton_crear_nueva_licitacion = QPushButton("Crear nueva licitación")
        boton_cargar_licitacion_preexistente = QPushButton("Cargar licitación preexistente")
        boton_salir = QPushButton("Salir")

        boton_crear_nueva_licitacion.setContentsMargins(10, 10, 10, 10)
        boton_crear_nueva_licitacion.clicked.connect(self.crear_nueva_licitacion)
        boton_cargar_licitacion_preexistente.setContentsMargins(10, 10, 10, 10)
        boton_cargar_licitacion_preexistente.clicked.connect(self.cargar_licitacion_preexistente)
        boton_salir.setContentsMargins(10, 10, 10, 10)
        boton_salir.clicked.connect(self.close)

        caja = QVBoxLayout()
        caja.setContentsMargins(15, 15, 15, 15)
        caja.addStretch(1)
        caja.addWidget(boton_crear_nueva_licitacion)
        caja.addWidget(boton_cargar_licitacion_preexistente)
        caja.addStretch(3)
        caja.addWidget(boton_salir)
        caja.addStretch(1)
        marco = QGroupBox()
        marco.setLayout(caja)
        caja2 = QVBoxLayout()
        caja2.addWidget(marco)
        self.setLayout(caja2)

        self.resize(self.sizeHint() * 2)
    
    def crear_nueva_licitacion(self):
        self.accion = PantallaPrincipal.A_CREAR
        self.accept()
    
    def cargar_licitacion_preexistente(self):
        self.accion = PantallaPrincipal.A_CARGAR
        self.accept()
    
    def obtener_accion(self):
        return self.accion

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Salir', "Está a punto de salir.\nEstá seguro que desea salir?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.accion = PantallaPrincipal.A_SALIR
            event.accept()
        else:
            event.ignore()


def crear_nueva_licitacion():
    pass


def cargar_licitacion_preexistente():
    pass


if __name__ == '__main__':
    app = QApplication(sysargv)
    pantalla_principal = PantallaPrincipal()
    if pantalla_principal.exec() == QDialog.Accepted:
        accion = pantalla_principal.obtener_accion()
        if accion == PantallaPrincipal.A_CREAR:
            print("Crear")
            crear_nueva_licitacion()
            pass
        elif accion == PantallaPrincipal.A_CARGAR:
            print("Cargar")
            cargar_licitacion_preexistente()
            pass
        else:
            pass
    #sysexit(app.exec_())
    #print("hola mundo!")
