from sys import argv as sysargv, exit as sysexit
from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, QStyle, QTableWidget, QGridLayout, QLabel, QVBoxLayout, QHeaderView, QAbstractItemView, QTableWidgetItem, QFrame, QGroupBox
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QModelIndex, QMimeData
from clases import Empresa, Contrato


class DialogoEmpresa(QDialog):
    def __init__(self, parent=None, empresa=None, id_sugerido=None, universo_empresas=[]):
        super().__init__(parent)
        self.dibujar_IU()
        self.empresa = empresa
        self.universo_empresas = universo_empresas
        if self.empresa != None:
            self.cargar_empresa()
            self.setWindowTitle("Modificación de Empresa")
            self.id.setFocus()
        elif id_sugerido != None:
            self.id.setText(str(id_sugerido))
            self.id.setFocus()
    
    def dibujar_IU(self):
        self.setWindowTitle("Ingreso de Empresa")
        self.setWindowModality(Qt.ApplicationModal)
        self.setSizeGripEnabled(False)
        self.setContentsMargins(10, 10, 10, 10)
        self.id = QLineEdit()
        self.nombre = QLineEdit()
        self.facturacion_media_anual = QLineEdit()
        self.recursos_financieros = QLineEdit()
        self.contratos = QTableWidget(0, 2)
        self.cantidad_contratos = QLabel("0")
        self.total_valor_contratos = QLabel("0.000")
        self.id_error = QLabel("*")
        self.nombre_error = QLabel("*")
        self.facturacion_media_anual_error = QLabel("*")
        self.recursos_financieros_error = QLabel("*")
        self.contratos_error = QLabel("*")
        self.espaciador = QLabel(" ")

        self.id.setValidator(QIntValidator(1, 999))
        self.id.setAlignment(Qt.AlignRight)
        self.id.setMaximumWidth(100)
        self.id.textChanged.connect(self.marcar_id_erroneo)
        self.id.setToolTip("Identificador único de empresa en todo el sistema")
        #self.nombre.setAlignment(Qt.AlignRight)
        self.nombre.setMaximumWidth(250)
        self.nombre.textChanged.connect(self.marcar_nombre_erroneo)
        self.nombre.setToolTip("Nombre con el que se la conoce")
        self.facturacion_media_anual.setValidator(QDoubleValidator(0, 999999999, 3))
        self.facturacion_media_anual.setAlignment(Qt.AlignRight)
        self.facturacion_media_anual.setMaximumWidth(150)
        self.facturacion_media_anual.textChanged.connect(self.marcar_facturacion_erronea)
        self.facturacion_media_anual.setToolTip("Facturación media anual")
        self.recursos_financieros.setValidator(QDoubleValidator(0, 999999999, 3))
        self.recursos_financieros.setAlignment(Qt.AlignRight)
        self.recursos_financieros.setMaximumWidth(150)
        self.recursos_financieros.textChanged.connect(self.marcar_recursos_erroneos)
        self.recursos_financieros.setToolTip("Recursos financieros con los que cuenta")
        self.contratos.setHorizontalHeaderLabels(["Año", "Valor"])
        self.contratos.verticalHeader().setVisible(False)
        self.contratos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.contratos.setSelectionMode(QAbstractItemView.SingleSelection)
        self.contratos.itemChanged.connect(self.actualizar_totales)
        self.contratos.cellChanged.connect(self.marcar_contratos_erroneos)
        self.contratos.setToolTip("Contratos anteriores concretados")
        self.id_error.setStyleSheet("QLabel {color : red}")
        self.id_error.setVisible(False)
        self.id_error.setFixedWidth(10)
        self.nombre_error.setStyleSheet("QLabel {color : red}")
        self.nombre_error.setVisible(False)
        self.nombre_error.setFixedWidth(10)
        self.facturacion_media_anual_error.setStyleSheet("QLabel {color : red}")
        self.facturacion_media_anual_error.setVisible(False)
        self.facturacion_media_anual_error.setFixedWidth(10)
        self.recursos_financieros_error.setStyleSheet("QLabel {color : red}")
        self.recursos_financieros_error.setVisible(False)
        self.recursos_financieros_error.setFixedWidth(10)
        self.contratos_error.setStyleSheet("QLabel {color : red}")
        self.contratos_error.setVisible(False)
        self.contratos_error.setFixedWidth(10)
        self.espaciador.setFixedWidth(10)
        self.espaciador.setFixedHeight(0)

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

        grilla = QGridLayout()
        grilla.setColumnMinimumWidth(1, 20)
        grilla.addWidget(QLabel("Id"), 0, 0)
        grilla.addWidget(self.id_error, 0, 1, Qt.AlignTop)
        grilla.addWidget(self.id, 0, 2)
        grilla.addWidget(QLabel("Nombre"), 1, 0)
        grilla.addWidget(self.nombre_error, 1, 1, Qt.AlignTop)
        grilla.addWidget(self.nombre, 1, 2)
        grilla.addWidget(QLabel("Facturación Media Anual"), 2, 0)
        grilla.addWidget(self.facturacion_media_anual_error, 2, 1, Qt.AlignTop)
        grilla.addWidget(self.facturacion_media_anual, 2, 2)
        grilla.addWidget(QLabel("Recursos Financieros"), 3, 0)
        grilla.addWidget(self.recursos_financieros_error, 3, 1, Qt.AlignTop)
        grilla.addWidget(self.recursos_financieros, 3, 2)
        grilla.addWidget(QLabel("Contratos"), 4, 0, Qt.AlignTop)
        grilla.addWidget(self.contratos_error, 4, 1, Qt.AlignTop)
        grilla.addWidget(self.contratos, 4, 2)
        grilla.addLayout(caja_botones, 4, 3)
        grilla.addLayout(caja_totales, 5, 2)
        grilla.addWidget(self.espaciador, 6, 1)
        marco = QGroupBox("Empresa")
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
        if len(self.id.text()) == 0 or self.empresa_existente(int(self.id.text())):
            self.id.setFocus()
        elif len(self.nombre.text()) == 0 or self.nombre.text().isspace():
            self.nombre.setFocus()
        elif len(self.facturacion_media_anual.text()) == 0:
            self.facturacion_media_anual.setFocus()
        elif len(self.recursos_financieros.text()) == 0:
            self.recursos_financieros.setFocus()
        elif not self.datos_contratos_completos():
            pass
        else:
            super().accept()
    
    def marcar_campos_erroneos(self):
        self.marcar_id_erroneo()
        self.marcar_nombre_erroneo()
        self.marcar_facturacion_erronea()
        self.marcar_recursos_erroneos()
        self.marcar_contratos_erroneos()
    
    def marcar_id_erroneo(self):
        if len(self.id.text()) == 0 or self.empresa_existente(int(self.id.text())):
            self.id_error.setVisible(True)
        else:
            self.id_error.setVisible(False)
    
    def marcar_nombre_erroneo(self):
        if len(self.nombre.text()) == 0 or self.nombre.text().isspace():
            self.nombre_error.setVisible(True)
        else:
            self.nombre_error.setVisible(False)
    
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
    
    def marcar_contratos_erroneos(self):
        if not self.datos_contratos_completos():
            self.contratos_error.setVisible(True)
        else:
            self.contratos_error.setVisible(False)
    
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
            try:
                int(self.contratos.item(fila, 0).text())
            except ValueError:
                self.contratos.setFocus()
                self.contratos.setCurrentItem(self.contratos.item(fila,0))
                completos = False
                break
            try:
                float(self.contratos.item(fila, 1).text())
            except ValueError:
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
        self.marcar_contratos_erroneos()
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
                try:
                    valor_contrato = float(valor_contrato)
                except ValueError:
                    valor_contrato = 0.00
            suma += valor_contrato
        self.total_valor_contratos.setText("{0:,.3f}".format(suma))

    def cargar_empresa(self):
        self.id.setText(str(self.empresa.id))    
        self.nombre.setText(self.empresa.nombre)
        self.facturacion_media_anual.setText(str(self.empresa.facturacion_media_anual()))
        self.recursos_financieros.setText(str(self.empresa.recursos_financieros()))
        for contrato in self.empresa.contratos():
            self.agregar_contrato()
            self.contratos.item(self.contratos.currentRow(), 0).setText(str(contrato.anio))
            self.contratos.item(self.contratos.currentRow(), 1).setText(str(contrato.valor))

    def obtener_empresa(self):
        contratos = []
        for fila in range(self.contratos.rowCount()):
            item_anio = self.contratos.item(fila, 0)
            item_valor = self.contratos.item(fila, 1)
            contrato = Contrato(int(item_anio.text()), float(item_valor.text()))
            contratos.append(contrato)
        return Empresa(int(self.id.text()), self.nombre.text(), float(self.facturacion_media_anual.text()), float(self.recursos_financieros.text()), contratos)
    
    def empresa_existente(self, id):
        return any(id == empresa.id for empresa in set.union(*[set(empresa.empresas_involucradas()) for empresa in self.universo_empresas] + [set()]) if empresa != self.empresa)
        #return any(id in empresa.ids_involucrados() for empresa in set(self.universo_empresas).difference(set([self.empresa])))

    
if __name__ == '__main__':
    app = QApplication(sysargv)
    ex = DialogoEmpresa()
    if ex.exec() == QDialog.Accepted:
        empresa = ex.obtener_empresa()
        print(empresa.id)
        print(empresa.nombre)
    empresa = Empresa(2, "Empresa 2 del pebet", 34234.234, 2343.234, [Contrato(2017, 25365.25), Contrato(2018, 2323.25)])
    ex = DialogoEmpresa(empresa=empresa)
    if ex.exec() == QDialog.Accepted:
        empresa = ex.obtener_empresa()
        print(empresa.id)
        print(empresa.nombre)
    #sysexit(app.exec_()