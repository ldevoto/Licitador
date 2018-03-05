from sys import argv as sysargv, exit as sysexit
from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, QStyle, QTableWidget, QGridLayout, QLabel, QVBoxLayout, QHeaderView, QAbstractItemView, QTableWidgetItem, QAbstractScrollArea, QFrame
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QModelIndex, QMimeData
from clases import Asociacion, Empresa, Contrato
from dialogo_empresa import DialogoEmpresa


class DialogoAsociacion(QDialog):
    def __init__(self, parent=None, asociacion=None):
        super().__init__(parent)
        self.dibujar_IU()
        self.array_empresas = []
        self.asociacion = asociacion
        if self.asociacion != None:
            self.cargar_asociacion()
            self.setWindowTitle("Modificación de Asociación")
            self.id.setFocus()
    
    def dibujar_IU(self):
        self.setWindowTitle("Ingreso de Asociación")
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
        self.id_error = QLabel("*")
        self.nombre_error = QLabel("*")
        self.empresas_error = QLabel("*")
        self.espaciador = QLabel(" ")

        self.id.setValidator(QIntValidator(1, 100))
        self.id.setAlignment(Qt.AlignRight)
        self.id.setMaximumWidth(100)
        self.id.textChanged.connect(self.marcar_id_erroneo)
        self.id.setToolTip("Identificador único de asociacón en todo el sistema")
        #self.nombre.setAlignment(Qt.AlignRight)
        self.nombre.setMaximumWidth(250)
        self.nombre.textChanged.connect(self.marcar_nombre_erroneo)
        self.nombre.setToolTip("Nombre con el que se la conoce")
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
        self.empresas.cellChanged.connect(self.marcar_empresas_erroneas)
        self.empresas.setToolTip("Empresas que la componen")
        self.empresas.doubleClicked.connect(self.editar_empresa)
        self.cantidad_empresas.setFixedWidth(self.empresas.columnWidth(0))
        self.espacio.setFixedWidth(self.empresas.columnWidth(1))
        self.id_error.setStyleSheet("QLabel {color : red}")
        self.id_error.setVisible(False)
        self.id_error.setFixedWidth(10)
        self.nombre_error.setStyleSheet("QLabel {color : red}")
        self.nombre_error.setVisible(False)
        self.nombre_error.setFixedWidth(10)
        self.empresas_error.setStyleSheet("QLabel {color : red}")
        self.empresas_error.setVisible(False)
        self.empresas_error.setFixedWidth(10)

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
        boton_editar_empresa = QPushButton(QIcon("iconos/edit.png"), "")
        boton_editar_empresa.clicked.connect(self.editar_empresa)
        boton_editar_empresa.setMinimumSize(50, 10)
        caja_botones = QVBoxLayout()
        caja_botones.addStretch(1)
        caja_botones.addWidget(boton_agregar_empresa)
        caja_botones.addWidget(boton_eliminar_empresa)
        caja_botones.addWidget(boton_editar_empresa)
        caja_botones.addStretch(5)
        caja_totales = QHBoxLayout()
        caja_totales.addWidget(self.cantidad_empresas)
        caja_totales.addWidget(self.espacio)
        caja_totales.addWidget(self.total_facturacion_media_anual)
        caja_totales.addWidget(self.total_recursos_financieros)
        caja_totales.addWidget(self.total_experiencia)

        grilla = QGridLayout()
        grilla.setColumnMinimumWidth(1, 20)
        grilla.addWidget(QLabel("Id"), 0, 0)
        grilla.addWidget(self.id_error, 0, 1, Qt.AlignTop)
        grilla.addWidget(self.id, 0, 2)
        grilla.addWidget(QLabel("Nombre"), 1, 0)
        grilla.addWidget(self.nombre_error, 1, 1, Qt.AlignTop)
        grilla.addWidget(self.nombre, 1, 2)
        grilla.addWidget(QLabel("Socios"), 2, 0, Qt.AlignTop)
        grilla.addWidget(self.empresas_error, 2, 1, Qt.AlignTop)
        grilla.addWidget(self.empresas, 2, 2)
        grilla.addLayout(caja_botones, 2, 3)
        grilla.addWidget(self.espaciador, 3, 1)
        grilla.addLayout(caja_totales, 3, 2)
        marco = QFrame()
        marco.setFrameStyle(QFrame.StyledPanel)
        marco.setLayout(grilla)

        caja_horizontal = QHBoxLayout()
        caja_horizontal.addStretch(1)
        caja_horizontal.addWidget(boton_cancelar)
        caja_horizontal.addStretch(5)
        caja_horizontal.addWidget(boton_confirmar)
        caja_horizontal.addStretch(1)
        caja_horizontal.setContentsMargins(10, 10, 10, 0)
        formulario = QFormLayout(self)
        formulario.addRow(marco)
        formulario.addRow(caja_horizontal)
        self.resize(self.sizeHint())
        self.setMinimumSize(self.sizeHint())
        self.setMaximumSize(self.sizeHint())
    
    def accept(self):
        self.marcar_campos_erroneos()
        if len(self.id.text()) == 0:
            self.id.setFocus()
        elif len(self.nombre.text()) == 0 or self.nombre.text().isspace():
            self.nombre.setFocus()
        elif self.empresas.rowCount() == 0:
            self.empresas.setFocus()
            self.agregar_empresa()
        else:
            super().accept()
    
    def marcar_campos_erroneos(self):
        self.marcar_id_erroneo()
        self.marcar_nombre_erroneo()
        self.marcar_empresas_erroneas()
    
    def marcar_id_erroneo(self):
        if len(self.id.text()) == 0:
            self.id_error.setVisible(True)
        else:
            self.id_error.setVisible(False)
    
    def marcar_nombre_erroneo(self):
        if len(self.nombre.text()) == 0 or self.nombre.text().isspace():
            self.nombre_error.setVisible(True)
        else:
            self.nombre_error.setVisible(False)
    
    def marcar_empresas_erroneas(self):
        if self.empresas.rowCount() == 0:
            self.empresas_error.setVisible(True)
        else:
            self.empresas_error.setVisible(False)
    
    def agregar_empresa(self):
        dialogo_empresa = DialogoEmpresa()
        if dialogo_empresa.exec() == QDialog.Accepted:
            empresa = dialogo_empresa.obtener_empresa()
            self.cargar_linea_empresa(self.empresas.rowCount())
            self.cargar_datos_empresa(self.empresas.rowCount() - 1, empresa)
            self.empresas.setFocus()
            self.empresas.setCurrentItem(self.empresas.item(self.empresas.rowCount() -1, 0))
        
    def cargar_linea_empresa(self, fila):
        self.empresas.insertRow(fila)
        item_id = QTableWidgetItem()
        item_nombre = QTableWidgetItem()
        item_facturacion_media_anual = QTableWidgetItem()
        item_recursos_financieros = QTableWidgetItem()
        item_experiencia = QTableWidgetItem()
        item_empresa = QTableWidgetItemEmpresa(None)

        self.empresas.setItem(fila, 0, item_id)
        self.empresas.setItem(fila, 1, item_nombre)
        self.empresas.setItem(fila, 2, item_facturacion_media_anual)
        self.empresas.setItem(fila, 3, item_recursos_financieros)
        self.empresas.setItem(fila, 4, item_experiencia)
        self.empresas.setItem(fila, 5, item_empresa)
    
    def cargar_datos_empresa(self, fila, empresa):
        self.array_empresas.append(empresa)

        item_id = self.empresas.item(fila, 0)
        item_nombre = self.empresas.item(fila, 1)
        item_facturacion_media_anual = self.empresas.item(fila, 2)
        item_recursos_financieros = self.empresas.item(fila, 3)
        item_experiencia = self.empresas.item(fila, 4)
        item_empresa = self.empresas.item(fila, 5)

        item_id.setText(str(empresa.id))
        item_nombre.setText(empresa.nombre)
        item_facturacion_media_anual.setText("{0:.3f}".format(empresa.facturacion_media_anual()))
        item_recursos_financieros.setText("{0:.3f}".format(empresa.recursos_financieros()))
        item_experiencia.setText("{0:.3f}".format(sum(contrato.valor for contrato in empresa.contratos())))
        item_empresa.empresa = empresa
        self.actualizar_totales()

    def eliminar_empresa(self):
        if self.empresas.rowCount() != 0:
            self.array_empresas.remove(self.empresas.item(self.empresas.currentRow(), 5).empresa)
            self.empresas.removeRow(self.empresas.currentRow())
        self.marcar_empresas_erroneas()
        self.actualizar_totales()

    def editar_empresa(self):
        if self.empresas.rowCount() != 0:
            empresa = self.empresas.item(self.empresas.currentRow(), 5).empresa
            dialogo_empresa = DialogoEmpresa(empresa=empresa)
            if dialogo_empresa.exec() == QDialog.Accepted:
                self.array_empresas.remove(empresa)
                empresa = dialogo_empresa.obtener_empresa()
                self.cargar_datos_empresa(self.empresas.currentRow(), empresa)
            

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

    def cargar_asociacion(self):
        self.id.setText(str(self.asociacion.id))
        self.nombre.setText(self.asociacion.nombre)
        for socio in self.asociacion.socios:
            self.cargar_linea_empresa(self.empresas.rowCount())
            self.cargar_datos_empresa(self.empresas.rowCount() - 1, socio)
        self.empresas.setFocus()
        self.empresas.setCurrentItem(self.empresas.item(self.empresas.rowCount()-1, 0))

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
    asociacion = Asociacion(2, "Asociacion WTF 2", [Empresa(1, "Empresa 1", 2000.03, 3000.02, [Contrato(2017, 1235.25)]), Empresa(3, "Empresa 3", 11111.11, 222222.22, [Contrato(2018, 3333.33), Contrato(2019, 44444.444)])])
    ex = DialogoAsociacion(asociacion=asociacion)
    if ex.exec() == QDialog.Accepted:
        asociacion = ex.obtener_asociacion()
        print(asociacion.id)
        print(asociacion.nombre)
        print(asociacion.socios)
        print(asociacion.facturacion_media_anual())
        print(asociacion.recursos_financieros())
    ex.deleteLater()
    #sysexit(app.exec_()