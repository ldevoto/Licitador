from sys import argv as sysargv, exit as sysexit
from time import sleep
from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, 
                             QStyle, QTableWidget, QGridLayout, QLabel, QVBoxLayout, QHeaderView, 
                             QAbstractItemView, QTableWidgetItem, QAbstractScrollArea, QFrame, 
                             QMainWindow, QWidget, QLayout, QMessageBox, QGroupBox, QShortcut, QStackedWidget)
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator, QKeySequence, QScreen, QGuiApplication
from PyQt5.QtCore import Qt, QModelIndex, QMimeData, QLine, QSize
from clases import Asociacion, Empresa, Contrato, Combinacion, Licitador
from widgets_ocultos import Estados, MensajeSalida
from widgets_resultados import CombinacionGanadora, Combinaciones

class DialogoResultados(QDialog):
    def __init__(self, licitacion, parent=None):
        super().__init__(parent=parent)
        self.licitacion = licitacion
        self.dibujar_IU()

    def dibujar_IU(self):
        self.setWindowTitle('Resultados licitación "{0}"'.format(self.licitacion.nombre))
        self.setWindowModality(Qt.ApplicationModal)
        self.setSizeGripEnabled(True)
        self.setWindowState(self.windowState() | Qt.WindowMaximized)
        self.setContentsMargins(10, 0, 10, 20)

        self.contenedor = QHBoxLayout()
        self.marco_control = QGroupBox()
        self.caja_control = QVBoxLayout()
        self.boton_combinacion_ganadora = QPushButton("Combinación Ganadora")
        self.boton_todas_las_combinaciones = QPushButton("Combinaciones")
        self.boton_todas_las_posibilidades = QPushButton("Posibilidades")
        self.boton_datos = QPushButton("Datos")
        self.boton_informacion_adicional = QPushButton("Información Adicional")
        self.boton_salir = QPushButton("Terminar")
        self.marco_vista = QGroupBox()
        self.caja_vista = QVBoxLayout()
        self.widget_vista = QStackedWidget()
        self.combinacion_ganadora = CombinacionGanadora(self.licitacion)
        self.en_construccion = QLabel("En contruccion...")
        self.combinaciones = Combinaciones(self.licitacion)
        #self.posibilidades = Posibilidades(self.licitacion)
        #self.datos = Datos(self.licitacion)
        #self.informacion_adicional = InformacionAdicional(self.licitacion)

        self.boton_combinacion_ganadora.clicked.connect(self.boton1_clickeado)
        self.boton_todas_las_combinaciones.clicked.connect(self.boton2_clickeado)
        self.boton_todas_las_posibilidades.clicked.connect(self.boton3_clickeado)
        self.boton_datos.clicked.connect(self.boton4_clickeado)
        self.boton_informacion_adicional.clicked.connect(self.boton5_clickeado)
        self.boton_salir.clicked.connect(self.accept)

        self.widget_vista.addWidget(self.combinacion_ganadora)
        self.widget_vista.addWidget(self.combinaciones)
        #self.widget_vista.addWidget(self.posibilidades)
        #self.widget_vista.addWidget(self.datos)
        #self.widget_vista.addWidget(self.informacion_adicional)
        self.widget_vista.addWidget(self.en_construccion)
        self.caja_vista.addWidget(self.widget_vista)
        self.marco_vista.setLayout(self.caja_vista)
        self.caja_control.addWidget(self.boton_combinacion_ganadora)
        self.caja_control.addWidget(self.boton_todas_las_combinaciones)
        #self.caja_control.addWidget(self.boton_todas_las_posibilidades)
        #self.caja_control.addWidget(self.boton_datos)
        #self.caja_control.addWidget(self.boton_informacion_adicional)
        self.caja_control.addStretch(1)
        self.caja_control.addWidget(self.boton_salir)
        self.marco_control.setLayout(self.caja_control)
        self.contenedor.addWidget(self.marco_control)
        self.contenedor.addWidget(self.marco_vista)
        self.setLayout(self.contenedor)

    
    def boton1_clickeado(self):
        self.widget_vista.setCurrentWidget(self.combinacion_ganadora)
    
    def boton2_clickeado(self):
        self.widget_vista.setCurrentWidget(self.combinaciones)
    
    def boton3_clickeado(self):
        self.widget_vista.setCurrentWidget(self.en_construccion)
    
    def boton4_clickeado(self):
        self.widget_vista.setCurrentWidget(self.en_construccion)
    
    def boton5_clickeado(self):
        self.widget_vista.setCurrentWidget(self.en_construccion)

if __name__ == "__main__":
    app = QApplication(sysargv)
    licitacion = Licitador("licitacion1")
    #licitacion = Licitador("lic1")
    licitacion.cargar_licitacion()
    licitacion.iniciar_licitacion()
    licitacion.reducir_combinaciones()
    licitacion.ordenar_combinaciones()
    dialogo_resultado = DialogoResultados(licitacion)
    dialogo_resultado.exec()
