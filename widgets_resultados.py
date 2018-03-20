from sys import argv as sysargv, exit as sysexit
from time import sleep
from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, 
                             QStyle, QTableWidget, QGridLayout, QLabel, QVBoxLayout, QHeaderView, 
                             QAbstractItemView, QTableWidgetItem, QAbstractScrollArea, QFrame, 
                             QMainWindow, QWidget, QLayout, QMessageBox, QGroupBox, QShortcut, QStackedWidget, QScrollArea)
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator, QKeySequence
from PyQt5.QtCore import Qt, QModelIndex, QMimeData
from clases import Asociacion, Empresa, Contrato, Combinacion, Licitador
from widgets_ocultos import Estados, MensajeSalida

class CombinacionGanadora(QWidget):
    def __init__(self, licitacion, parent=None):
        super().__init__(parent=parent)
        self.licitacion = licitacion
        #self.combinacion_ganadora = self.licitacion.combinacion_ganadora()
        self.dibujar_IU()
    
    def dibujar_IU(self):
        self.contenedor = QHBoxLayout()
        #self.area_de_scroll = QScrollArea()
        self.marco_general = QGroupBox("Combinación Ganadora")
        self.caja = QVBoxLayout()
        self.marco_por_lote = QGroupBox("Por lote")
        self.marco_por_empresa = QGroupBox("Por Empresa")
        self.marco_totales = QGroupBox("Totales")
        self.caja.addWidget(self.marco_por_lote)
        self.caja.addWidget(self.marco_por_empresa)
        self.caja.addWidget(self.marco_totales)
        self.marco_general.setLayout(self.caja)
        #self.area_de_scroll.setWidget(self.marco_general)
        #self.contenedor.addWidget(self.area_de_scroll)
        self.contenedor.addWidget(self.marco_general)
        self.setLayout(self.contenedor)

if __name__ == "__main__":
    app = QApplication(sysargv)
    c = CombinacionGanadora(None)
    c.show()
    sysexit(app.exec_())
    