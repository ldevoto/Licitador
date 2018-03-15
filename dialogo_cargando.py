from sys import argv as sysargv, exit as sysexit
from operator import itemgetter, attrgetter
from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, 
                            QHBoxLayout, QStyle, QLabel, QGridLayout, QFrame, QGroupBox,
                            QShortcut, QComboBox, QAbstractItemView, QSizePolicy, QCheckBox, QVBoxLayout, QWidget, QSizePolicy)
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator, QKeySequence
from PyQt5.QtCore import Qt, QSize, QTimer, QTime
from clases import Lote, Empresa, Asociacion, Contrato, ConjuntoOfertas, Oferta, Adicional
from widgets_ocultos import QCheckBoxLote
from animacion_cargando import AnimacionCargando

class DialogoCargando(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dibujar_IU()
    
    def dibujar_IU(self):
        self.setWindowTitle("Calculando...")
        self.setWindowModality(Qt.ApplicationModal)
        self.setSizeGripEnabled(False)
        self.setContentsMargins(10, 10, 10, 10)
        self.setFixedSize(QSize(500, 300))
        self.animacion = AnimacionCargando()
        self.texto_informativo = QLabel("")
        self.texto_informativo.setAlignment(Qt.AlignCenter)
        self.texto_informativo.setWordWrap(True)
        self.texto_tiempo = QLabel("00:00:00")
        self.texto_tiempo.setAlignment(Qt.AlignCenter)
        self.texto_tiempo.setWordWrap(True)
        self.caja_horizontal = QHBoxLayout()
        self.caja_horizontal.addStretch(1)
        self.caja_horizontal.addWidget(self.animacion)
        self.caja_horizontal.addStretch(1)
        self.caja = QVBoxLayout()
        self.caja.setAlignment(Qt.AlignCenter)
        self.caja.addStretch(4)
        self.caja.addWidget(self.texto_informativo)
        self.caja.addStretch(1)
        self.caja.addLayout(self.caja_horizontal)
        self.caja.addWidget(self.texto_tiempo)
        self.caja.addStretch(2)
        grupo = QGroupBox()
        grupo.setLayout(self.caja)
        hola = QVBoxLayout()
        hola.addWidget(grupo)
        self.setLayout(hola)
        self.reloj = QTime(0, 0, 0, 0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_reloj)
        self.timer.start(1000)
        self.boton_confirmar = QPushButton(QIcon("iconos/right-arrow.png"), "", self)
        self.boton_confirmar.clicked.connect(self.accept)
        self.boton_confirmar.setDefault(True)
        self.boton_confirmar.setMinimumSize(50, 22)
        self.boton_confirmar.setMaximumSize(50, 22)
        self.boton_confirmar.setVisible(False)
        self.boton_confirmar.move(400, 240)
    
    def setear_texto(self, texto):
        self.texto_informativo.setText(texto)
    
    def actualizar_reloj(self):
        self.reloj = self.reloj.addSecs(1)
        self.texto_tiempo.setText(self.reloj.toString("hh:mm:ss"))
    
    def mostrar_boton_confirmar(self):
        self.texto_tiempo.setVisible(False)
        self.animacion.gif.stop()
        self.setear_texto("Proceso terminado exitosamente en {0}\nA continuación podrá consultar los resultados finales".format(self.reloj.toString("hh:mm:ss")))
        self.boton_confirmar.setVisible(True)


    
if __name__ == '__main__':
    app = QApplication(sysargv)
    ex = DialogoCargando()
    if ex.exec() == QDialog.Accepted:
        print("Exitoso")