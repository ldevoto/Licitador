from sys import argv as sysargv, exit as sysexit
from operator import itemgetter, attrgetter
from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, 
                            QHBoxLayout, QStyle, QLabel, QGridLayout, QFrame, QGroupBox,
                            QShortcut, QComboBox, QAbstractItemView, QSizePolicy, QCheckBox)
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator, QKeySequence
from PyQt5.QtCore import Qt
from clases import Lote, Empresa, Asociacion, Contrato, ConjuntoOfertas, Oferta, Adicional
from widgets_ocultos import QCheckBoxLote

class DialogoAdicional(QDialog):
    def __init__(self, parent=None, adicional=None, ofertas=[], lotes=[], empresas=[], adicionales=[]):
        super().__init__(parent)
        self.adicional = adicional
        self.array_ofertas = ofertas
        self.array_lotes = sorted(lotes, key=attrgetter("id"))
        self.array_empresas = sorted(empresas, key=attrgetter("id"))
        self.array_adicionales = adicionales
        self.dibujar_IU()
        if self.adicional != None:
            self.cargar_adicional()
    
    def dibujar_IU(self):
        self.setWindowTitle("Ingreso Descuento")
        self.setWindowModality(Qt.ApplicationModal)
        self.setSizeGripEnabled(False)
        self.setContentsMargins(10, 10, 10, 10)

        self.empresa = QComboBox()
        self.ofertas = QGridLayout()
        self.porcentaje = QLineEdit()
        self.empresa_error = QLabel("*")
        self.ofertas_error = QLabel("*")
        self.porcentaje_error = QLabel("*")
        self.espaciador = QLabel(" ")

        self.cargar_lista_empresas()
        self.completar_grilla_con_lotes()

        self.empresa.setFixedWidth(250)
        self.empresa.currentTextChanged.connect(self.cargar_lista_ofertas)
        self.empresa.currentTextChanged.connect(self.marcar_adicional_erroneo)
        self.porcentaje.setValidator(QDoubleValidator(1, 100, 3))
        self.porcentaje.textChanged.connect(self.marcar_porcentaje_erroneo)
        self.porcentaje.setAlignment(Qt.AlignRight)
        self.porcentaje.setMaximumWidth(150)
        self.porcentaje.setMinimumWidth(150)
        self.porcentaje.setToolTip("Porcentaje de descuento que la Empresa ofrece por el conjunto de Ofertas")
        self.empresa_error.setStyleSheet("QLabel {color : red}")
        self.empresa_error.setVisible(False)
        self.empresa_error.setFixedWidth(10)
        self.ofertas_error.setStyleSheet("QLabel {color : red}")
        self.ofertas_error.setVisible(False)
        self.ofertas_error.setFixedWidth(10)
        self.porcentaje_error.setStyleSheet("QLabel {color : red}")
        self.porcentaje_error.setVisible(False)
        self.porcentaje_error.setFixedWidth(10)
        self.espaciador.setFixedWidth(10)
        self.espaciador.setFixedHeight(0)

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

        self.grilla = QGridLayout()
        self.grilla.setColumnMinimumWidth(1, 20)
        self.grilla.addWidget(QLabel("Empresa"), 0, 0)
        self.grilla.addWidget(self.empresa_error, 0, 1, Qt.AlignTop | Qt.AlignRight)
        self.grilla.addWidget(self.empresa, 0, 2)
        self.grilla.addWidget(QLabel("Porcentaje"), 1, 0)
        self.grilla.addWidget(self.porcentaje_error, 1, 1, Qt.AlignTop | Qt.AlignRight)
        self.grilla.addWidget(self.porcentaje, 1, 2)
        self.grilla.addWidget(QLabel("Lotes"), 2, 0, Qt.AlignTop)
        self.grilla.addWidget(self.ofertas_error, 2, 1, Qt.AlignTop | Qt.AlignRight)
        self.grilla.addLayout(self.ofertas, 2, 2)
        self.grilla.addWidget(self.espaciador, 3, 1)
        marco = QGroupBox("Descuento")
        marco.setLayout(self.grilla)

        formulario = QFormLayout(self)
        formulario.addRow(marco)
        formulario.addRow(caja_horizontal)
        #self.setMinimumSize(self.sizeHint())
        #self.setMaximumSize(self.sizeHint())
    
    def accept(self):
        self.marcar_campos_erroneos()
        if not self.oferta_seleccionada():
            pass
        elif self.adicional_existente():
            pass
        elif len(self.porcentaje.text()) == 0:
            self.porcentaje.setFocus()
        else:
            super().accept()
    
    def marcar_campos_erroneos(self):
        self.marcar_adicional_erroneo()
        self.marcar_porcentaje_erroneo()
    
    def marcar_adicional_erroneo(self):
        if not self.oferta_seleccionada():
            self.ofertas_error.setVisible(True)
        else:
            self.ofertas_error.setVisible(False)
            if self.adicional_existente():
                self.empresa_error.setVisible(True)
                self.ofertas_error.setVisible(True)
            else:
                self.empresa_error.setVisible(False)
                self.ofertas_error.setVisible(False)
    
    def marcar_porcentaje_erroneo(self):
        if len(self.porcentaje.text()) == 0:
            self.porcentaje_error.setVisible(True)
        else:
            self.porcentaje_error.setVisible(False)
        
    def oferta_seleccionada(self):
        return any(self.ofertas.itemAt(i).widget().isChecked() for i in range(self.ofertas.count()))
    
    def cargar_adicional(self):
        self.empresa.setCurrentIndex(self.empresa.findData(self.adicional.empresa))
        self.porcentaje.setText(str(self.adicional.porcentaje * -1))
        #self.completar_grilla_con_ofertas()
        for i in range(self.ofertas.count()):
            item = self.ofertas.itemAt(i).widget()
            if self.adicional.conjunto_ofertas.oferta_contenida(item.oferta):
                item.setCheckState(Qt.Checked)

    def cargar_lista_empresas(self):
        for empresa in self.array_empresas:
            self.empresa.addItem(empresa.nombre.strip(), empresa)
    
    def cargar_lista_ofertas(self):
        for i in range(self.ofertas.count()):
            item_lote = self.ofertas.itemAt(i).widget()
            item_lote.setear_oferta(None)
            item_lote.deshabilitar()
            for oferta in self.array_ofertas:
                if oferta.lote == item_lote.lote and oferta.empresa == self.empresa.currentData():
                    item_lote.setear_oferta(oferta)
                    item_lote.habilitar()
                    break

    def obtener_adicional(self):
        return Adicional(self.empresa.currentData(), self.conjunto_ofertas(), float(self.porcentaje.text()) * -1)
    
    def adicional_existente(self):
        return any(self.adicional_temporal().es_equivalente(adicional) for adicional in self.array_adicionales if (self.adicional == None) or (self.adicional != None and not adicional.es_equivalente(self.adicional)))
    
    def adicional_temporal(self):
        return Adicional(self.empresa.currentData(), self.conjunto_ofertas(), 0.00)
    
    def conjunto_ofertas(self):
        conjunto_ofertas = ConjuntoOfertas()
        for i in range(0, self.ofertas.count()):
            item_lote = self.ofertas.itemAt(i).widget()
            if item_lote.isChecked():
                conjunto_ofertas.agregar_oferta(item_lote.oferta)
        return conjunto_ofertas
    
    def cambio_seleccion(self, asdf):
        self.marcar_adicional_erroneo()
    
    def completar_grilla_con_lotes(self):
        for i, lote in enumerate(self.array_lotes):
            item_lote = QCheckBoxLote(lote)
            item_lote.stateChanged.connect(self.cambio_seleccion)
            if len(self.array_lotes) <= 10:
                if (i >= len(self.array_lotes) / 2):
                    self.ofertas.addWidget(item_lote, i - len(self.array_lotes) / 2, 1)
                else:
                    self.ofertas.addWidget(item_lote, i, 0)
            else:
                if (i >= len(self.array_lotes) / 3 * 2):
                    self.ofertas.addWidget(item_lote, i - len(self.array_lotes) / 3 * 2, 2)
                elif (i >= len(self.array_lotes) / 3):
                    self.ofertas.addWidget(item_lote, i - len(self.array_lotes) / 3, 1)
                else:
                    self.ofertas.addWidget(item_lote, i, 0)
        self.cargar_lista_ofertas()

    
if __name__ == '__main__':
    app = QApplication(sysargv)
    lotes = [Lote(1, 1, 1, 1), Lote(2, 2.2, 2.22, 2.222), Lote(3, 3.3, 3.33, 3.333), Lote(4, 4.4, 4.44, 4.444), Lote(5, 5.5, 5.55, 5.555)]
    empresas = [Empresa(1, "Empresa 1", 1, 1, [Contrato(2017, 1), Contrato(2017, 1)]), Empresa(2, "Empresa 2", 2, 2, [Contrato(2017, 2), Contrato(2017, 2)]), Empresa(3, "Empresa 3", 3, 3, [Contrato(2017, 3), Contrato(2017, 3)]), Asociacion(1, "Asociacion 1",  [Empresa(10, "Empresa 10", 1, 1, [Contrato(2017, 1), Contrato(2017, 1)]), Empresa(20, "Empresa 20", 2, 2, [Contrato(2017, 2), Contrato(2017, 2)]), Empresa(30, "Empresa 30", 3, 3, [Contrato(2017, 3), Contrato(2017, 3)])])]
    oferta1 = Oferta(empresas[0], lotes[0], 12312)
    oferta2 = Oferta(empresas[0], lotes[1], 23434)
    oferta3 = Oferta(empresas[0], lotes[2], 515611)
    oferta4 = Oferta(empresas[0], lotes[3], 511)
    oferta5 = Oferta(empresas[1], lotes[0], 15)
    oferta6 = Oferta(empresas[1], lotes[3], 5)
    ofertas = [oferta1, oferta2, oferta3, oferta4, oferta5, oferta6]
    conjunto_ofertas = ConjuntoOfertas()
    conjunto_ofertas.agregar_oferta(oferta1)
    conjunto_ofertas.agregar_oferta(oferta2)
    conjunto_ofertas.agregar_oferta(oferta3)
    conjunto_ofertas.agregar_oferta(oferta4)
    conjunto_ofertas2 = ConjuntoOfertas()
    conjunto_ofertas2.agregar_oferta(oferta5)
    conjunto_ofertas2.agregar_oferta(oferta6)
    adicional1 = Adicional(empresas[0], conjunto_ofertas, 100)
    adicional2 = Adicional(empresas[1], conjunto_ofertas2, 52)
    ex = DialogoAdicional(ofertas=ofertas, lotes=lotes, empresas=empresas, adicionales=[adicional1, adicional2])
    if ex.exec() == QDialog.Accepted:
        adicional = ex.obtener_adicional()
        print(adicional.empresa.nombre)
        print(adicional.porcentaje)
        for oferta in adicional.conjunto_ofertas.ofertas:
            print(oferta.lote.id)
    ex = DialogoAdicional(adicional=adicional2, ofertas=ofertas, lotes=lotes, empresas=empresas, adicionales=[adicional1, adicional2])
    if ex.exec() == QDialog.Accepted:
        adicional = ex.obtener_adicional()
        print(adicional.empresa.nombre)
        print(adicional.porcentaje)
        for oferta in adicional.conjunto_ofertas.ofertas:
            print(oferta.lote.id)