from sys import argv as sysargv, exit as sysexit
from time import sleep
from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, 
                             QStyle, QTableWidget, QGridLayout, QLabel, QVBoxLayout, QHeaderView, 
                             QAbstractItemView, QTableWidgetItem, QAbstractScrollArea, QFrame, 
                             QMainWindow, QWidget, QLayout, QMessageBox, QGroupBox, QShortcut, QStackedWidget)
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator, QKeySequence
from PyQt5.QtCore import Qt, QModelIndex, QMimeData, QLine
from clases import Asociacion, Empresa, Contrato, Combinacion, Licitador
from widgets_ocultos import Estados, MensajeSalida
from widgets_resultados import CombinacionGanadora

class DialogoResultados(QDialog):
    def __init__(self, licitacion, parent=None):
        super().__init__(parent=parent)
        self.licitacion = licitacion
        self.dibujar_IU()

    def dibujar_IU(self):
        #self.setWindowTitle('Resultados licitación "{0}"'.format(self.licitacion.nombre))
        self.setWindowTitle('Resultados licitación "{0}"'.format("Hola Mundo"))
        self.setWindowModality(Qt.ApplicationModal)
        self.setSizeGripEnabled(False)
        self.setContentsMargins(10, 10, 10, 10)

        self.contenedor = QHBoxLayout()
        self.marco = QGroupBox()
        self.marco2 = QGroupBox()
        self.contenedor.addWidget(self.marco)
        self.contenedor.addWidget(self.marco2)
        #self.contenedor.addWidget(self.marco)
        #self.contenedor.addWidget(self.marco2)
        self.boton_combinacion_ganadora = QPushButton("Combinación Ganadora")
        self.boton_todas_las_combinaciones = QPushButton("Combinaciones")
        self.boton_todas_las_posibilidades = QPushButton("Posibilidades")
        self.boton_datos = QPushButton("Datos")
        self.boton_estadisticos = QPushButton("Estadísticos")
        self.boton_salir = QPushButton("Terminar")
        self.panel_control = QVBoxLayout()
        #self.panel_control.setContentsMargins(10, 10, 10, 10)
        self.panel_control.addWidget(self.boton_combinacion_ganadora)
        self.panel_control.addWidget(self.boton_todas_las_combinaciones)
        self.panel_control.addWidget(self.boton_todas_las_posibilidades)
        self.panel_control.addWidget(self.boton_datos)
        self.panel_control.addWidget(self.boton_estadisticos)
        self.panel_control.addStretch(1)
        self.panel_control.addWidget(self.boton_salir)
        self.marco.setLayout(self.panel_control)

        self.combinacion_ganadora = CombinacionGanadora(self.licitacion)
        #self.combinaciones = Combinaciones(self.licitacion)
        #self.posibilidades = Posibilidades(self.licitacion)
        #self.datos = Datos(self.licitacion)
        #self.estadisticos = Estadisticos(self.licitacion)
        self.panel_vista = QVBoxLayout()
        self.widget_vista = QStackedWidget(self.licitacion)
        self.widget_vista.addWidget(self.combinacion_ganadora)
        #self.panel_vista.addWidget(self.combinaciones)
        #self.panel_vista.addWidget(self.posibilidades)
        #self.panel_vista.addWidget(self.datos)
        #self.panel_vista.addWidget(self.estadisticos)
        self.panel_vista.addWidget(self.widget_vista)
        self.marco2.setLayout(self.panel_vista)
        self.setLayout(self.contenedor)

        self.setFixedSize(1300, 600)

if __name__ == "__main__":
    app = QApplication(sysargv)
    dialogo_resultado = DialogoResultados(None)
    dialogo_resultado.exec()
