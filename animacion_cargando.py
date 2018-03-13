from sys import argv as sysargv, exit as sysexit
from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, 
                             QStyle, QTableWidget, QGridLayout, QLabel, QVBoxLayout, QHeaderView, 
                             QAbstractItemView, QTableWidgetItem, QAbstractScrollArea, QFrame, 
                             QMainWindow, QWidget, QLayout, QMessageBox, QGroupBox, QShortcut)
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator, QKeySequence, QPixmap, QMovie
from PyQt5.QtCore import Qt, QModelIndex, QMimeData, QSize
from clases import Asociacion, Empresa, Contrato
from dialogo_empresa import DialogoEmpresa

class AnimacionCargando(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.dibujar_IU()

    def dibujar_IU(self):
        self.setWindowTitle("Cargando...")

        self.gif = QMovie("iconos/loader.gif")
        self.cuadro = QLabel(self)
        self.cuadro.setMovie(self.gif)
        #self.gif.setScaledSize(QSize(440, 38))
        self.gif.start()
        self.setFixedWidth(220)
        self.setFixedHeight(19)

if __name__ == '__main__':
    app = QApplication(sysargv)
    animacion = AnimacionCargando()
    animacion.show()
    sysexit(app.exec_())
    #print("hola mundo!")
