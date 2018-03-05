from sys import argv as sysargv, exit as sysexit
from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, QStyle, QTableWidget, QGridLayout, QLabel, QVBoxLayout, QHeaderView, QAbstractItemView, QTableWidgetItem, QAbstractScrollArea
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QModelIndex, QMimeData
from clases import Asociacion, Empresa, Contrato
from dialogo_empresa import DialogoEmpresa


class DialogoAsociacion(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dibujar_IU()
        self.array_empresas = []
    
    def dibujar_IU(self):
        self.setWindowTitle("Asociación")
        self.setWindowModality(Qt.ApplicationModal)
        self.setSizeGripEnabled(False)
        self.setContentsMargins(10, 10, 10, 10)
        self.id = QLineEdit()
        self.nombre = QLineEdit()
        self.empresas = QTableWidget(0, 6)
        self.facturacion_media_anual = QLineEdit()
        self.recursos_financieros = QLineEdit()
        self.cantidad_empresas = QLabel("0")
        self.espacio = QLabel("")
        self.total_facturacion_media_anual = QLabel("$0.000")
        self.total_recursos_financieros = QLabel("$0.000")
        self.total_experiencia = QLabel("$0.000")

        self.id.setValidator(QIntValidator(1, 100))
        self.id.setAlignment(Qt.AlignRight)
        self.id.setMaximumWidth(100)
        self.nombre.setAlignment(Qt.AlignRight)
        self.nombre.setMaximumWidth(200)
        self.empresas.setHorizontalHeaderLabels(["Id", "Nombre", "Facturación Media Anual", "Recursos Financieros", "Experiencia", "Oculto"])
        self.empresas.verticalHeader().setVisible(False)
        self.empresas.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.empresas.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.empresas.horizontalHeader().hideSection(5)
        self.empresas.setSelectionMode(QAbstractItemView.SingleSelection)
        self.empresas.resizeColumnsToContents()
        self.empresas.setColumnWidth(0, self.empresas.columnWidth(0) + 10)
        self.empresas.setColumnWidth(1, self.empresas.columnWidth(1) + 150)
        self.empresas.setColumnWidth(3, self.empresas.columnWidth(2))
        self.empresas.setColumnWidth(4, self.empresas.columnWidth(2))
        self.empresas.resize(self.empresas.sizeHint())
        self.empresas.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.empresas.setFixedHeight(self.empresas.height())
        self.empresas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.cantidad_empresas.setFixedWidth(self.empresas.columnWidth(0))
        self.espacio.setFixedWidth(self.empresas.columnWidth(1))

        boton_confirmar = QPushButton(QIcon("iconos/check.png"), "")
        boton_confirmar.clicked.connect(self.accept)
        boton_confirmar.setDefault(True)
        boton_confirmar.setMinimumSize(50, 10)
        boton_cancelar = QPushButton(QIcon("iconos/cancel.png"), "")
        boton_cancelar.clicked.connect(self.reject)
        boton_cancelar.setMinimumSize(50, 10)
        boton_agregar_empresa = QPushButton(QIcon("iconos/plus.png"), "")
        boton_agregar_empresa.clicked.connect(self.agregar_empresa)
        boton_agregar_empresa.setMinimumSize(50, 10)
        boton_eliminar_empresa = QPushButton(QIcon("iconos/minus.png"), "")
        boton_eliminar_empresa.clicked.connect(self.eliminar_empresa)
        boton_eliminar_empresa.setMinimumSize(50, 10)
        caja_botones = QVBoxLayout()
        caja_botones.addStretch(1)
        caja_botones.addWidget(boton_agregar_empresa)
        caja_botones.addWidget(boton_eliminar_empresa)
        caja_botones.addStretch(5)
        caja_totales = QHBoxLayout()
        caja_totales.addWidget(self.cantidad_empresas)
        caja_totales.addWidget(self.espacio)
        caja_totales.addWidget(self.total_facturacion_media_anual)
        caja_totales.addWidget(self.total_recursos_financieros)
        caja_totales.addWidget(self.total_experiencia)

        grilla_contratos = QGridLayout()
        grilla_contratos.addWidget(QLabel("Id"), 0, 0)
        grilla_contratos.addWidget(self.id, 0, 1)
        grilla_contratos.addWidget(QLabel("Nombre"), 1, 0)
        grilla_contratos.addWidget(self.nombre, 1, 1)
        grilla_contratos.addWidget(QLabel("Socios"), 2, 0, Qt.AlignTop)
        grilla_contratos.addWidget(self.empresas, 2, 1)
        grilla_contratos.addLayout(caja_botones, 2, 2)
        grilla_contratos.addLayout(caja_totales, 3, 1)

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
            self.id.setFocus()
        elif len(self.nombre.text()) == 0:
            self.nombre.setFocus()
        else:
            super().accept()
    
    def agregar_empresa(self):
        dialogo_empresa = DialogoEmpresa()
        if dialogo_empresa.exec() == QDialog.Accepted:
            empresa = dialogo_empresa.obtener_empresa()
            self.array_empresas.append(empresa)
            self.empresas.insertRow(self.empresas.rowCount())
            item_id = QTableWidgetItem()
            item_nombre = QTableWidgetItem()
            item_facturacion_media_anual = QTableWidgetItem()
            item_recursos_financieros = QTableWidgetItem()
            item_experiencia = QTableWidgetItem()
            item_id.setText(str(empresa.id))
            item_nombre.setText(empresa.nombre)
            item_empresa = QTableWidgetItemEmpresa(empresa)
            item_facturacion_media_anual.setText("{0:.3f}".format(empresa.facturacion_media_anual()))
            item_recursos_financieros.setText("{0:.3f}".format(empresa.recursos_financieros()))
            item_experiencia.setText("{0:.3f}".format(sum(contrato.valor for contrato in empresa.contratos())))
            self.empresas.setItem(self.empresas.rowCount() - 1, 0, item_id)
            self.empresas.setItem(self.empresas.rowCount() - 1, 1, item_nombre)
            self.empresas.setItem(self.empresas.rowCount() - 1, 2, item_facturacion_media_anual)
            self.empresas.setItem(self.empresas.rowCount() - 1, 3, item_recursos_financieros)
            self.empresas.setItem(self.empresas.rowCount() - 1, 4, item_experiencia)
            self.empresas.setItem(self.empresas.rowCount() - 1, 5, item_empresa)
            self.actualizar_totales()
            self.empresas.setFocus()
            self.empresas.setCurrentItem(item_id)
        else:
            print("rechazado")

    def eliminar_empresa(self):
        self.array_empresas.remove(self.empresas.item(self.empresas.currentRow(), 5).empresa)
        self.empresas.removeRow(self.empresas.currentRow())
        self.actualizar_totales()

    def actualizar_totales(self):
        self.actualizar_cantidad_empresas()
        self.actualizar_total_valores_empresas()
    
    def actualizar_cantidad_empresas(self):
        self.cantidad_empresas.setText(str(self.empresas.rowCount()))

    def actualizar_total_valores_empresas(self):
        suma_facturacion_media_anual = 0.00
        suma_recursos_financieros = 0.00
        suma_experiencia = 0.00
        for fila in range(0, self.empresas.rowCount()):
            if self.empresas.item(fila, 2) == None:
                valor_facturacion_media_anual = 0.00
            else:
                valor_facturacion_media_anual = self.empresas.item(fila, 2).text()
                if len(valor_facturacion_media_anual) == 0:
                    valor_facturacion_media_anual = 0.00
                else:
                    valor_facturacion_media_anual = float(valor_facturacion_media_anual)
            if self.empresas.item(fila, 3) == None:
                valor_recursos_financieros = 0.00
            else:
                valor_recursos_financieros = self.empresas.item(fila, 3).text()
                if len(valor_recursos_financieros) == 0:
                    valor_recursos_financieros = 0.00
                else:
                    valor_recursos_financieros = float(valor_recursos_financieros)
            if self.empresas.item(fila, 4) == None:
                valor_experiencia = 0.00
            else:
                valor_experiencia = self.empresas.item(fila, 4).text()
                if len(valor_experiencia) == 0:
                    valor_experiencia = 0.00
                else:
                    valor_experiencia = float(valor_experiencia)
            suma_facturacion_media_anual += valor_facturacion_media_anual
            suma_recursos_financieros += valor_recursos_financieros
            suma_experiencia += valor_experiencia
            
        self.total_facturacion_media_anual.setText("${0:.3f}".format(suma_facturacion_media_anual))
        self.total_recursos_financieros.setText("${0:.3f}".format(suma_recursos_financieros))
        self.total_experiencia.setText("${0:.3f}".format(suma_experiencia))
        

    def obtener_asociacion(self):
        return Asociacion(int(self.id.text()),self.nombre.text(), self.array_empresas)


class QTableWidgetItemEmpresa(QTableWidgetItem):
    def __init__(self, empresa):
        super().__init__()
        self.empresa = empresa


if __name__ == '__main__':
    app = QApplication(sysargv)
    ex = DialogoAsociacion()
    if ex.exec() == QDialog.Accepted:
        asociacion = ex.obtener_asociacion()
        print(asociacion.id)
        print(asociacion.nombre)
        print(asociacion.socios)
        print(asociacion.facturacion_media_anual())
        print(asociacion.recursos_financieros())
    ex.deleteLater()
    #sysexit(app.exec_()