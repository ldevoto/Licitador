from sys import argv as sysargv, exit as sysexit
from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, 
                            QHBoxLayout, QStyle, QLabel, QGridLayout, QFrame, QGroupBox,
                            QShortcut, QComboBox, QAbstractItemView, QSizePolicy)
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator, QKeySequence
from PyQt5.QtCore import Qt
from clases import Lote, Empresa, Asociacion, Contrato, ConjuntoOfertas, Oferta

class DialogoOferta(QDialog):
    def __init__(self, parent=None, oferta=None, lotes=[], empresas=[], conjunto_ofertas=ConjuntoOfertas()):
        super().__init__(parent)
        self.array_lotes = lotes
        self.array_empresas = empresas
        self.conjunto_ofertas = conjunto_ofertas
        self.oferta = oferta
        self.dibujar_IU()
        if self.oferta != None:
            self.cargar_oferta()
            self.setWindowTitle("Modificación de Oferta")
        self.marcar_empresa_erronea()
    
    def dibujar_IU(self):
        self.setWindowTitle("Ingreso de Oferta")
        self.setWindowModality(Qt.ApplicationModal)
        self.setSizeGripEnabled(False)
        self.setContentsMargins(10, 10, 10, 10)

        self.empresa = QComboBox()
        self.lote = QComboBox()
        self.valor = QLineEdit()
        self.empresa_error = QLabel("*")
        self.lote_error = QLabel("*")
        self.valor_error = QLabel("*")
        self.espaciador = QLabel(" ")

        self.cargar_lista_lotes()
        self.cargar_lista_empresas()

        self.empresa.setFixedWidth(250)
        self.empresa.currentTextChanged.connect(self.marcar_empresa_erronea)
        self.lote.currentTextChanged.connect(self.marcar_lote_erroneo)
        self.lote.setFixedWidth(250)
        self.valor.setValidator(QDoubleValidator(0, 999999999, 3))
        self.valor.textChanged.connect(self.marcar_valor_erroneo)
        self.valor.setAlignment(Qt.AlignRight)
        self.valor.setMaximumWidth(150)
        self.valor.setToolTip("Valor que oferta la Empresa por el Lote")
        self.empresa_error.setStyleSheet("QLabel {color : red}")
        self.empresa_error.setVisible(False)
        self.empresa_error.setFixedWidth(10)
        self.lote_error.setStyleSheet("QLabel {color : red}")
        self.lote_error.setVisible(False)
        self.lote_error.setFixedWidth(10)
        self.valor_error.setStyleSheet("QLabel {color : red}")
        self.valor_error.setVisible(False)
        self.valor_error.setFixedWidth(10)
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

        grilla = QGridLayout()
        grilla.setColumnMinimumWidth(1, 20)
        grilla.addWidget(QLabel("Empresa"), 0, 0)
        grilla.addWidget(self.empresa_error, 0, 1, Qt.AlignTop | Qt.AlignRight)
        grilla.addWidget(self.empresa, 0, 2)
        grilla.addWidget(QLabel("Lote"), 1, 0)
        grilla.addWidget(self.lote_error, 1, 1, Qt.AlignTop | Qt.AlignRight)
        grilla.addWidget(self.lote, 1, 2)
        grilla.addWidget(QLabel("valor"), 2, 0)
        grilla.addWidget(self.valor_error, 2, 1, Qt.AlignTop | Qt.AlignRight)
        grilla.addWidget(self.valor, 2, 2)
        grilla.addWidget(self.espaciador, 3, 1)
        marco = QGroupBox("Oferta")
        marco.setLayout(grilla)

        formulario = QFormLayout(self)
        formulario.addRow(marco)
        formulario.addRow(caja_horizontal)
        self.setMinimumSize(self.sizeHint())
        self.setMaximumSize(self.sizeHint())
    
    def accept(self):
        self.marcar_campos_erroneos()
        if self.oferta_existente():
            self.lote.setFocus()
            self.lote.showPopup()
        elif len(self.valor.text()) == 0:
            self.valor.setFocus()
        else:
            super().accept()
    
    def marcar_campos_erroneos(self):
        self.marcar_lote_erroneo()
        self.marcar_valor_erroneo()
    
    def marcar_empresa_erronea(self):
        if self.oferta_existente():
            self.empresa_error.setVisible(True)
            self.lote_error.setVisible(True)
        else:
            self.empresa_error.setVisible(False)
            self.lote_error.setVisible(False)
    
    def marcar_lote_erroneo(self):
        if self.oferta_existente():
            self.empresa_error.setVisible(True)
            self.lote_error.setVisible(True)
        else:
            self.empresa_error.setVisible(False)
            self.lote_error.setVisible(False)
    
    def marcar_valor_erroneo(self):
        if len(self.valor.text()) == 0:
            self.valor_error.setVisible(True)
        else:
            self.valor_error.setVisible(False)
    
    def cargar_oferta(self):
        self.empresa.setCurrentIndex(self.empresa.findData(self.oferta.empresa))
        self.lote.setCurrentIndex(self.lote.findData(self.oferta.lote))
        self.valor.setText(str(self.oferta.valor))
        self.marcar_campos_erroneos()

    def cargar_lista_lotes(self):
        for lote in self.array_lotes:
            if lote.descripcion != "":
                self.lote.addItem("{0}".format(lote.descripcion.strip()), lote)
            else:
                self.lote.addItem("Lote {0}".format(lote.id), lote)

    def cargar_lista_empresas(self):
        for empresa in self.array_empresas:
            self.empresa.addItem(empresa.nombre.strip(), empresa)

    def obtener_oferta(self):
        return Oferta(self.empresa.currentData(), self.lote.currentData(), float(self.valor.text()))
    
    def oferta_existente(self):
        if self.oferta != None and self.oferta.es_equivalente(Oferta(self.empresa.currentData(), self.lote.currentData(), 0.00)):
            return False
        else:
            return self.conjunto_ofertas.oferta_existente(Oferta(self.empresa.currentData(), self.lote.currentData(), 0.00))

    
if __name__ == '__main__':
    app = QApplication(sysargv)
    lotes = [Lote(1, 1, 1, 1), Lote(2, 2.2, 2.22, 2.222), Lote(3, 3.3, 3.33, 3.333)]
    empresas = [Empresa(1, "Empresa 1", 1, 1, [Contrato(2017, 1), Contrato(2017, 1)]), Empresa(2, "Empresa 2", 2, 2, [Contrato(2017, 2), Contrato(2017, 2)]), Empresa(3, "Empresa 3", 3, 3, [Contrato(2017, 3), Contrato(2017, 3)]), Asociacion(1, "Asociacion 1",  [Empresa(10, "Empresa 10", 1, 1, [Contrato(2017, 1), Contrato(2017, 1)]), Empresa(20, "Empresa 20", 2, 2, [Contrato(2017, 2), Contrato(2017, 2)]), Empresa(30, "Empresa 30", 3, 3, [Contrato(2017, 3), Contrato(2017, 3)])])]
    oferta1 = Oferta(empresas[0], lotes[0], 12312)
    oferta2 = Oferta(empresas[1], lotes[1], 23434)
    conjunto_ofertas = ConjuntoOfertas()
    conjunto_ofertas.agregar_oferta(oferta1)
    conjunto_ofertas.agregar_oferta(oferta2)
    ex = DialogoOferta(lotes=lotes, empresas=empresas, conjunto_ofertas=conjunto_ofertas)
    if ex.exec() == QDialog.Accepted:
        oferta = ex.obtener_oferta()
        print(oferta.empresa.nombre)
        print(oferta.lote.id)
        print(oferta.valor)
    ex = DialogoOferta(lotes=lotes, oferta=oferta2, empresas=empresas, conjunto_ofertas=conjunto_ofertas)
    if ex.exec() == QDialog.Accepted:
        oferta = ex.obtener_oferta()
        print(oferta.empresa.nombre)
        print(oferta.lote.id)
        print(oferta.valor)