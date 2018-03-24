from sys import argv as sysargv, exit as sysexit
from time import sleep
from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, 
                             QStyle, QTableWidget, QGridLayout, QLabel, QVBoxLayout, QHeaderView, 
                             QAbstractItemView, QTableWidgetItem, QAbstractScrollArea, QFrame, 
                             QMainWindow, QWidget, QLayout, QMessageBox, QGroupBox, QShortcut, QStackedWidget, QScrollArea, QSizePolicy)
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
        self.marco_general = QGroupBox("Combinación Ganadora")
        self.caja_general = QVBoxLayout()
        self.scroll_general = QScrollArea()
        self.wid = QWidget()
        self.caja = QVBoxLayout()
        self.contenedor.addWidget(self.marco_general)
        self.marco_general.setLayout(self.caja_general)
        self.caja_general.addWidget(self.scroll_general)
        #self.caja_general.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        #self.scroll_general.setWidget(self.wid)
        #self.wid.setLayout(self.caja)
        self.scroll_general.setLayout(self.caja)
        #self.scroll_general.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.marco_por_lote = QGroupBox("Por lote")
        self.caja_lote = QVBoxLayout()
        #self.scroll_lote = QScrollArea()
        #self.scroll_lote.setStyleSheet("QAbstractScrollArea {border:0px solid black}")
        #self.scroll_lote.setContentsMargins(10, 10, 10, 10)
        #self.scroll_lote.setWidget(QLabel("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaadddddddddddddddddddddddddddddddddddddddaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\nasd\nqweqwe\n13234\n23234\n12df\nasdfa"))
        self.caja_lote.addWidget(QLabel("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaadddddddddddddddddddddddddddddddddddddddaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\nasd\nqweqwe\n13234\n23234\n12df\nasdfa"))
        self.marco_por_lote.setLayout(self.caja_lote)
        #self.caja_lote.addWidget(self.scroll_lote)
        self.marco_por_empresa = QGroupBox("Por Empresa")
        self.caja_empresa = QVBoxLayout()
        #self.scroll_empresa = QScrollArea()
        self.marco_por_empresa.setLayout(self.caja_empresa)
        #self.caja_empresa.addWidget(self.scroll_empresa)
        self.marco_totales = QGroupBox("Totales")
        self.caja_totales = QVBoxLayout()
        #self.scroll_totales = QScrollArea()
        self.marco_totales.setLayout(self.caja_totales)
        #self.caja_totales.addWidget(self.scroll_totales)
        self.caja.addWidget(self.marco_por_lote)
        self.caja.addWidget(self.marco_por_empresa)
        self.caja.addWidget(self.marco_totales)
        #self.marco_general.setLayout(self.caja)
        #self.area_de_scroll.setWidget(self.marco_general)
        #self.contenedor.addWidget(self.area_de_scroll)
        #self.contenedor.addWidget(self.marco_general)
        self.setLayout(self.contenedor)

if __name__ == "__main__":
    app = QApplication(sysargv)
    c = CombinacionGanadora(None)
    c.show()
    sysexit(app.exec_())
    