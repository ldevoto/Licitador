from sys import argv as sysargv, exit as sysexit
from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, QStyle, QLabel, QGridLayout, QFrame
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtCore import Qt
from clases import Lote

class DialogoLote(QDialog):
    def __init__(self, parent=None, lote=None):
        super().__init__(parent)
        self.dibujar_IU()
        self.lote = lote
        if self.lote != None:
            self.cargar_lote()
            self.setWindowTitle("Modificación de Lote")
            self.id.setFocus()
    
    def dibujar_IU(self):
        self.setWindowTitle("Ingreso de Lote")
        self.setWindowModality(Qt.ApplicationModal)
        self.setSizeGripEnabled(False)
        self.setContentsMargins(10, 10, 10, 10)
        self.id = QLineEdit()
        self.descripcion = QLineEdit()
        self.facturacion_media_anual = QLineEdit()
        self.recursos_financieros = QLineEdit()
        self.experiencia = QLineEdit()
        self.id_error = QLabel("*")
        self.facturacion_media_anual_error = QLabel("*")
        self.recursos_financieros_error = QLabel ("*")
        self.experiencia_error = QLabel("*")
        self.espaciador = QLabel(" ")

        self.id.setValidator(QIntValidator(1, 100))
        self.id.textChanged.connect(self.marcar_id_erroneo)
        self.id.setAlignment(Qt.AlignRight)
        self.id.setMaximumWidth(100)
        self.id.setToolTip("Identidicador único de lote en todo el sistema")
        #self.descripcion.setAlignment(Qt.AlignRight)
        self.descripcion.setMinimumWidth(250)
        self.descripcion.setMaximumWidth(250)
        self.descripcion.setToolTip("Breve descripción o información relevante")
        self.facturacion_media_anual.setValidator(QDoubleValidator(0, 999999999, 3))
        self.facturacion_media_anual.textChanged.connect(self.marcar_facturacion_erronea)
        self.facturacion_media_anual.setAlignment(Qt.AlignRight)
        self.facturacion_media_anual.setMaximumWidth(150)
        self.facturacion_media_anual.setToolTip("Facturación media anual requerida para su adjudicación")
        self.recursos_financieros.setValidator(QDoubleValidator(0, 999999999, 3))
        self.recursos_financieros.textChanged.connect(self.marcar_recursos_erroneos)
        self.recursos_financieros.setAlignment(Qt.AlignRight)
        self.recursos_financieros.setMaximumWidth(150)
        self.recursos_financieros.setToolTip("Recursos financieros requeridos para su adjudicación")
        self.experiencia.setValidator(QDoubleValidator(0, 999999999, 3))
        self.experiencia.textChanged.connect(self.marcar_experiencia_erronea)
        self.experiencia.setAlignment(Qt.AlignRight)
        self.experiencia.setMaximumWidth(150)
        self.experiencia.setToolTip("Experiencia requerida para su adjudicación")
        self.id_error.setStyleSheet("QLabel {color : red}")
        self.id_error.setVisible(False)
        self.id_error.setFixedWidth(10)
        self.facturacion_media_anual_error.setStyleSheet("QLabel {color : red}")
        self.facturacion_media_anual_error.setVisible(False)
        self.facturacion_media_anual_error.setFixedWidth(10)
        self.recursos_financieros_error.setStyleSheet("QLabel {color : red}")
        self.recursos_financieros_error.setVisible(False)
        self.recursos_financieros_error.setFixedWidth(10)
        self.experiencia_error.setStyleSheet("QLabel {color : red}")
        self.experiencia_error.setVisible(False)
        self.experiencia_error.setFixedWidth(10)
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
        grilla.addWidget(QLabel("Id"), 0, 0)
        grilla.addWidget(self.id_error, 0, 1, Qt.AlignTop)
        grilla.addWidget(self.id, 0, 2)
        grilla.addWidget(QLabel("Descripción"), 1, 0)
        grilla.addWidget(self.espaciador, 1, 1)
        grilla.addWidget(self.descripcion, 1, 2)
        grilla.addWidget(QLabel("Facturación Media Anual"), 2, 0)
        grilla.addWidget(self.facturacion_media_anual_error, 2, 1, Qt.AlignTop)
        grilla.addWidget(self.facturacion_media_anual, 2, 2)
        grilla.addWidget(QLabel("Recursos Financieros"), 3, 0)
        grilla.addWidget(self.recursos_financieros_error, 3, 1, Qt.AlignTop)
        grilla.addWidget(self.recursos_financieros, 3, 2)
        grilla.addWidget(QLabel("Experiencia"), 4, 0)
        grilla.addWidget(self.experiencia_error, 4, 1, Qt.AlignTop)
        grilla.addWidget(self.experiencia, 4, 2)
        marco = QFrame()
        marco.setFrameStyle(QFrame.StyledPanel)
        marco.setLayout(grilla)

        formulario = QFormLayout(self)
        formulario.addRow(marco)
        formulario.addRow(caja_horizontal)
        self.setMinimumSize(self.sizeHint())
        self.setMaximumSize(self.sizeHint())
    
    def accept(self):
        self.marcar_campos_erroneos()
        if len(self.id.text()) == 0:
            #self.id.setStyleSheet("QLineEdit { border-color: red; border-style: solid; border-width: 1px}")
            self.id.setFocus()
        elif len(self.facturacion_media_anual.text()) == 0:
            self.facturacion_media_anual.setFocus()
        elif len(self.recursos_financieros.text()) == 0:
            self.recursos_financieros.setFocus()
        elif len(self.experiencia.text()) == 0:
            self.experiencia.setFocus()
        else:
            super().accept()
    
    def marcar_campos_erroneos(self):
        self.marcar_id_erroneo()
        self.marcar_facturacion_erronea()
        self.marcar_recursos_erroneos()
        self.marcar_experiencia_erronea()
    
    def marcar_id_erroneo(self):
        if len(self.id.text()) == 0:
            self.id_error.setVisible(True)
        else:
            self.id_error.setVisible(False)
    
    def marcar_facturacion_erronea(self):
        if len(self.facturacion_media_anual.text()) == 0:
            self.facturacion_media_anual_error.setVisible(True)
        else:
            self.facturacion_media_anual_error.setVisible(False)
    
    def marcar_recursos_erroneos(self):
        if len(self.recursos_financieros.text()) == 0:
            self.recursos_financieros_error.setVisible(True)
        else:
            self.recursos_financieros_error.setVisible(False)
    
    def marcar_experiencia_erronea(self):
        if len(self.experiencia.text()) == 0:
            self.experiencia_error.setVisible(True)
        else:
            self.experiencia_error.setVisible(False)
    
    def cargar_lote(self):
        self.id.setText(str(self.lote.id))
        self.descripcion.setText(self.lote.descripcion)
        self.facturacion_media_anual.setText(str(self.lote.facturacion_media_anual))
        self.recursos_financieros.setText(str(self.lote.recursos_financieros))
        self.experiencia.setText(str(self.lote.experiencia))

    def obtener_lote(self):
        lote = Lote(int(self.id.text()), float(self.facturacion_media_anual.text()), float(self.recursos_financieros.text()), float(self.experiencia.text()))
        if len(self.descripcion.text()) != 0:
            lote.descripcion = self.descripcion.text()
        return lote

    
if __name__ == '__main__':
    app = QApplication(sysargv)
    ex = DialogoLote()
    if ex.exec() == QDialog.Accepted:
        lote = ex.obtener_lote()
        print(lote.id)
        print(lote.descripcion)
    lote = Lote(2, 3000.943, 30000.23, 3000.11)
    lote.descripcion = "Soy el lote 2"
    ex = DialogoLote(lote=lote)
    if ex.exec() == QDialog.Accepted:
        lote = ex.obtener_lote()
        print(lote.id)
        print(lote.descripcion)
    #sysexit(app.exec_())