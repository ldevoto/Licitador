from sys import argv as sysargv, exit as sysexit
from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, QStyle, QTableWidget, QGridLayout, QLabel, QVBoxLayout, QHeaderView, QAbstractItemView, QTableWidgetItem
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QModelIndex, QMimeData
from clases import Empresa, Contrato


class DialogoEmpresa(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dibujar_IU()
    
    def dibujar_IU(self):
        self.setWindowTitle("Empresa")
        self.setWindowModality(Qt.ApplicationModal)
        self.setSizeGripEnabled(False)
        self.setContentsMargins(10, 10, 10, 10)
        self.id = QLineEdit()
        self.nombre = QLineEdit()
        self.facturacion_media_anual = QLineEdit()
        self.recursos_financieros = QLineEdit()
        self.contratos = QTableWidget(0, 2)
        self.cantidad_contratos = QLabel("0")
        self.total_valor_contratos = QLabel("$0.000")

        self.id.setValidator(QIntValidator(1, 100))
        self.id.setAlignment(Qt.AlignRight)
        self.nombre.setAlignment(Qt.AlignRight)
        self.facturacion_media_anual.setValidator(QDoubleValidator(0, 999999999, 3))
        self.facturacion_media_anual.setAlignment(Qt.AlignRight)
        self.recursos_financieros.setValidator(QDoubleValidator(0, 999999999, 3))
        self.recursos_financieros.setAlignment(Qt.AlignRight)
        self.contratos.setHorizontalHeaderLabels(["Año", "Valor"])
        self.contratos.verticalHeader().setVisible(False)
        self.contratos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.contratos.setSelectionMode(QAbstractItemView.SingleSelection)
        self.contratos.itemChanged.connect(self.actualizar_totales)
        boton_confirmar = QPushButton(QIcon("iconos/check.png"), "")
        boton_confirmar.clicked.connect(self.accept)
        boton_confirmar.setDefault(True)
        boton_confirmar.setMinimumSize(50, 10)
        boton_cancelar = QPushButton(QIcon("iconos/cancel.png"), "")
        boton_cancelar.clicked.connect(self.reject)
        boton_cancelar.setMinimumSize(50, 10)
        boton_agregar_contrato = QPushButton(QIcon("iconos/plus.png"), "")
        boton_agregar_contrato.clicked.connect(self.agregar_contrato)
        boton_agregar_contrato.setMinimumSize(50, 10)
        boton_eliminar_contrato = QPushButton(QIcon("iconos/minus.png"), "")
        boton_eliminar_contrato.clicked.connect(self.eliminar_contrato)
        boton_eliminar_contrato.setMinimumSize(50, 10)
        caja_botones = QVBoxLayout()
        caja_botones.addStretch(1)
        caja_botones.addWidget(boton_agregar_contrato)
        caja_botones.addWidget(boton_eliminar_contrato)
        caja_botones.addStretch(5)
        caja_totales = QHBoxLayout()
        caja_totales.addWidget(self.cantidad_contratos)
        caja_totales.addWidget(self.total_valor_contratos)

        grilla_contratos = QGridLayout()
        #grilla_contratos.setColumnMinimumWidth(0, 200)
        grilla_contratos.addWidget(QLabel("Id"), 0, 0)
        grilla_contratos.addWidget(self.id, 0, 1)
        grilla_contratos.addWidget(QLabel("Nombre"), 1, 0)
        grilla_contratos.addWidget(self.nombre, 1, 1)
        grilla_contratos.addWidget(QLabel("Facturación Media Anual"), 2, 0)
        grilla_contratos.addWidget(self.facturacion_media_anual, 2, 1)
        grilla_contratos.addWidget(QLabel("Recursos Financieros"), 3, 0)
        grilla_contratos.addWidget(self.recursos_financieros, 3, 1)
        grilla_contratos.addWidget(QLabel("Contratos"), 4, 0, Qt.AlignTop)
        grilla_contratos.addWidget(self.contratos, 4, 1)
        grilla_contratos.addLayout(caja_botones, 4, 2)
        grilla_contratos.addLayout(caja_totales, 5, 1)

        caja_horizontal = QHBoxLayout()
        caja_horizontal.addStretch(1)
        caja_horizontal.addWidget(boton_cancelar)
        caja_horizontal.addStretch(5)
        caja_horizontal.addWidget(boton_confirmar)
        caja_horizontal.addStretch(1)
        caja_horizontal.setContentsMargins(10, 10, 10, 0)
        formulario = QFormLayout(self)
        formulario.addRow(grilla_contratos)
        formulario.addRow(caja_horizontal)
        self.resize(self.sizeHint())
        self.setMinimumSize(self.sizeHint())
        self.setMaximumSize(self.sizeHint())
    
    def accept(self):
        if len(self.id.text()) == 0:
            #self.id.setStyleSheet("QLineEdit { border-color: red; border-style: solid; border-width: 1px}")
            self.id.setFocus()
        elif len(self.nombre.text()) == 0:
            self.nombre.setFocus()
        elif len(self.facturacion_media_anual.text()) == 0:
            self.facturacion_media_anual.setFocus()
        elif len(self.recursos_financieros.text()) == 0:
            self.recursos_financieros.setFocus()
        elif not self.datos_contratos_completos():
            pass
        else:
            super().accept()
    
    def datos_contratos_completos(self):
        completos = True
        for fila in range(0, self.contratos.rowCount()):
            #if len(self.contratos.cellWidget(fila, 0).text()) == 0:
            if len(self.contratos.item(fila, 0).text()) == 0:
                #self.contratos.cellWidget(fila, 0).setFocus()
                self.contratos.setFocus()
                self.contratos.setCurrentItem(self.contratos.item(fila, 0))
                completos = False
                break
            #if len(self.contratos.cellWidget(fila, 1).text()) == 0:
            if len(self.contratos.item(fila, 1).text()) == 0:
                #self.contratos.cellWidget(fila, 1).setFocus()
                self.contratos.setFocus()
                self.contratos.setCurrentItem(self.contratos.item(fila, 1))
                completos = False
                break
        return completos
    
    def agregar_contrato(self):
        if self.datos_contratos_completos():
            self.contratos.insertRow(self.contratos.rowCount())
            item_anio = QTableWidgetItem() #QLineEdit()
            item_valor = QTableWidgetItem() #QLineEdit()
            #item_anio.setValidator(QIntValidator(1, 3000))
            #item_valor.setValidator(QDoubleValidator(0, 999999999, 3))
            #self.contratos.setCellWidget(self.contratos.rowCount() - 1, 0, item_anio)
            #self.contratos.setCellWidget(self.contratos.rowCount() - 1, 1, item_valor)
            #self.contratos.setFocus()
            #self.contratos.cellWidget(self.contratos.rowCount() - 1, 0).setFocus()
            #self.contratos.cellWidget(self.contratos.rowCount() - 1, 0).setFocus()
            self.contratos.setItem(self.contratos.rowCount() - 1, 0, item_anio)
            self.contratos.setItem(self.contratos.rowCount() - 1, 1, item_valor)
            self.actualizar_totales()
            self.contratos.setFocus()
            self.contratos.setCurrentItem(item_anio)

    def eliminar_contrato(self):
        self.contratos.removeRow(self.contratos.currentRow())
        self.actualizar_totales()

    def actualizar_totales(self):
        self.actualizar_cantidad_contratos()
        self.actualizar_total_valor_contratos()
    
    def actualizar_cantidad_contratos(self):
        self.cantidad_contratos.setText(str(self.contratos.rowCount()))

    def actualizar_total_valor_contratos(self):
        suma = 0.00
        for fila in range(0, self.contratos.rowCount()):
            if self.contratos.item(fila, 1) == None:
                continue
            valor_contrato = self.contratos.item(fila, 1).text()
            if len(valor_contrato) == 0:
                valor_contrato = 0.00
            else:
                valor_contrato = float(valor_contrato)
            suma += valor_contrato
        self.total_valor_contratos.setText("${0:.3f}".format(suma))
        

    def obtener_empresa(self):
        contratos = []
        for fila in range(self.contratos.rowCount()):
            item_anio = self.contratos.item(fila, 0)
            item_valor = self.contratos.item(fila, 1)
            contrato = Contrato(int(item_anio.text()), float(item_valor.text()))
            contratos.append(contrato)
        return Empresa(int(self.id.text()), self.nombre.text(), float(self.facturacion_media_anual.text()), float(self.recursos_financieros.text()), contratos)

    
if __name__ == '__main__':
    app = QApplication(sysargv)
    ex = DialogoEmpresa()
    if ex.exec() == QDialog.Accepted:
        empresa = ex.obtener_empresa()
        print(empresa.id)
        print(empresa.nombre)
    ex.deleteLater()
    #sysexit(app.exec_()