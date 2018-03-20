from PyQt5.QtWidgets import QTableWidgetItem, QCheckBox, QWidget, QHBoxLayout, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QDoubleValidator

class QTableWidgetItemEmpresa(QTableWidgetItem):
    def __init__(self, empresa):
        super().__init__()
        self.empresa = empresa

class QTableWidgetItemLote(QTableWidgetItem):
    def __init__(self, lote):
        super().__init__()
        self.lote = lote
    
class QCheckBoxOferta(QCheckBox):
    def __init__(self, oferta, parent=None):
        super().__init__(parent=parent)
        self.oferta = oferta
    
class QCheckBoxLote(QCheckBox):
    def __init__(self, lote, parent=None):
        super().__init__(parent=parent)
        self.lote = lote
        self.oferta = None
        if self.lote.descripcion != "":
            self.setText("{0}".format(self.lote.descripcion.strip()))
        else:
            self.setText("Lote {0}".format(self.lote.id))
        self.setFixedWidth(150)
    
    def setear_oferta(self, oferta):
        self.oferta = oferta
    
    def habilitar(self):
        self.setEnabled(True)
    
    def deshabilitar(self):
        self.setCheckState(Qt.Unchecked)
        self.setEnabled(False)
    
class QCheckBoxOfertaLote(QWidget):
    def __init__(self, lote, parent=None, valor=None):
        super().__init__(parent=parent)
        self.lote = lote
        self.dibujar_IU()
        if valor != None:
            self.cargar_valor(valor)

    
    def dibujar_IU(self):
        caja_horizontal = QHBoxLayout()
        if (self.lote.descripcion != ""):
            self.check_lote = QCheckBox("Lote {0} - {1}".format(self.lote.id, self.lote.descripcion))
        else:
            self.check_lote = QCheckBox("Lote {0}".format(self.lote.id))

        self.valor_lote = QLineEdit()

        self.check_lote.setFixedWidth(100)
        self.check_lote.setToolTip("Determina si el Lote es ofertado por la Empresa o no")
        self.check_lote.stateChanged.connect(self.cambio_estado)
        self.valor_lote.setFixedWidth(100)
        self.valor_lote.setToolTip("Valor que oferta la Empresa por el Lote")
        self.valor_lote.setEnabled(False)
        self.valor_lote.editingFinished.connect(self.fuera_de_foco)

        caja_horizontal.addWidget(self.check_lote)
        #caja_horizontal.addWidget(self.etiqueta_valor)
        caja_horizontal.addWidget(self.valor_lote)

        self.setLayout(caja_horizontal)
    
    def cambio_estado(self):
        if self.check_lote.isChecked():
            self.valor_lote.setEnabled(True)
        else:
            self.valor_lote.setText("")
            self.valor_lote.setEnabled(False)
    
    def fuera_de_foco(self):
        if len(self.valor_lote.text()) == 0:
            self.check_lote.setCheckState(Qt.Unchecked)
        
    def obtener_valor(self):
        try:
            return float(self.valor_lote.text())
        except ValueError:
            return 0.0
    
    def lote_seleccionado(self):
        return self.check_lote.isChecked()

    def cargar_valor(self, valor):
        self.valor_lote.setText(str(valor))
        self.check_lote.setCheckState(Qt.Checked)

    def deshabilitar(self):
        self.check_lote.setCheckable(Qt.Unchecked)

class MensajeSalida(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Salir")
        self.setText("Está a punto de salir del sistema. Si lo hace, perderá toda la información no guardada.")
        self.setInformativeText("Desea salir de todos modos?")
        self.boton_si = self.addButton("Si", QMessageBox.YesRole)
        self.boton_no = self.addButton("No", QMessageBox.NoRole)
        self.setDefaultButton(self.boton_no)

class Estados():
    E_CONTINUAR = 2
    E_RETROCEDER = 1
    E_SALIR = 0
    E_INDETERMINADO = 99