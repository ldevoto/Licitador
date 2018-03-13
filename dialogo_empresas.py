from sys import argv as sysargv, exit as sysexit
from operator import itemgetter, attrgetter
from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, 
                             QStyle, QTableWidget, QGridLayout, QLabel, QVBoxLayout, QHeaderView, 
                             QAbstractItemView, QTableWidgetItem, QAbstractScrollArea, QFrame, 
                             QMainWindow, QWidget, QLayout, QMessageBox, QGroupBox)
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QModelIndex, QMimeData
from clases import Asociacion, Empresa, Contrato, Lote
from widgets_ocultos import Estados
from dialogo_empresa import DialogoEmpresa
from dialogo_asociacion import DialogoAsociacion
from widgets_ocultos import QTableWidgetItemEmpresa

class DialogoEmpresas(QDialog):
    def __init__(self, parent=None, empresas=None):
        super().__init__(parent=parent)
        self.estado = Estados.E_INDETERMINADO
        self.dibujar_IU()
        self.array_empresas = []
        self.array_empresas_a_cargar = empresas
        if self.array_empresas_a_cargar != None:
            self.cargar_empresas()
            if self.empresas.rowCount() != 0:
                self.empresas.setFocus()
                self.empresas.setCurrentItem(self.empresas.item(0, 0))
        self.orden_anterior = {"columna":0, "orden":Qt.AscendingOrder}

    def dibujar_IU(self):
        self.setWindowTitle("Ingreso de Empresas")
        self.setWindowModality(Qt.ApplicationModal)
        self.setSizeGripEnabled(False)
        self.setContentsMargins(10, 10, 10, 10)

        self.empresas = QTableWidget(0, 8)
        self.empresas_error = QLabel("*")
        self.cantidad_empresas = QLabel("0 Empresas")
        self.espaciador = QLabel(" ")

        self.empresas.setHorizontalHeaderLabels(["Id", "Nombre", "Es Asociación", "Facturación Media Anual", "Recursos Financieros", "Experiencia", "Cantidad de Contratos", "Oculto"])
        self.empresas.verticalHeader().setVisible(False)
        self.empresas.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.empresas.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.empresas.horizontalHeader().hideSection(7)
        self.empresas.setSelectionMode(QAbstractItemView.SingleSelection)
        self.empresas.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.empresas.resizeColumnsToContents()
        self.empresas.setColumnWidth(0, self.empresas.columnWidth(0) + 10)
        self.empresas.setColumnWidth(1, self.empresas.columnWidth(1) + 150)
        self.empresas.setColumnWidth(4, self.empresas.columnWidth(3))
        self.empresas.setColumnWidth(5, self.empresas.columnWidth(3))
        self.empresas.resize(self.empresas.sizeHint())
        self.empresas.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.empresas.setFixedHeight(self.empresas.height() + 100)
        self.empresas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.empresas.cellChanged.connect(self.marcar_empresas_erroneas)
        self.empresas.setToolTip("Empresas participantes de la licitación")
        self.empresas.doubleClicked.connect(self.editar_empresa)
        self.empresas_error.setStyleSheet("QLabel {color : red}")
        self.empresas_error.setVisible(False)
        self.empresas_error.setFixedWidth(10)
        #self.cantidad_empresas.setFixedWidth(self.empresas.columnWidth(0))

        boton_continuar = QPushButton(QIcon("iconos/right-arrow.png"), "")
        boton_continuar.clicked.connect(self.continuar)
        boton_continuar.setDefault(True)
        boton_continuar.setMinimumSize(50, 10)
        boton_continuar.setToolTip("Continuar al ingreso de Ofertas")
        boton_retroceder = QPushButton(QIcon("iconos/left-arrow.png"), "")
        boton_retroceder.clicked.connect(self.retroceder)
        boton_retroceder.setMinimumSize(50, 10)
        boton_retroceder.setToolTip("Retroceder al ingreso de Lotes")
        boton_agregar_empresa = QPushButton(QIcon("iconos/plus.png"), "")
        boton_agregar_empresa.clicked.connect(self.agregar_empresa)
        boton_agregar_empresa.setMinimumSize(50, 10)
        boton_agregar_empresa.setToolTip("Agregar nueva Empresa")
        boton_eliminar_empresa = QPushButton(QIcon("iconos/minus.png"), "")
        boton_eliminar_empresa.clicked.connect(self.eliminar_empresa)
        boton_eliminar_empresa.setMinimumSize(50, 10)
        boton_eliminar_empresa.setToolTip("Eliminar Empresa seleccionada")
        boton_editar_empresa = QPushButton(QIcon("iconos/edit.png"), "")
        boton_editar_empresa.clicked.connect(self.editar_empresa)
        boton_editar_empresa.setMinimumSize(50, 10)
        boton_editar_empresa.setToolTip("Editar Empresa seleccionada")
        caja_botones = QVBoxLayout()
        caja_botones.addStretch(1)
        caja_botones.addWidget(boton_agregar_empresa)
        caja_botones.addWidget(boton_eliminar_empresa)
        caja_botones.addWidget(boton_editar_empresa)
        caja_botones.addStretch(5)
        caja_totales = QHBoxLayout()
        caja_totales.addWidget(self.cantidad_empresas)
        caja_totales.addStretch(1)

        grilla = QGridLayout()
        grilla.setColumnMinimumWidth(1, 20)
        #grilla.addWidget(QLabel("Lotes"), 0, 0, Qt.AlignTop)
        grilla.addWidget(self.empresas_error, 0, 1, Qt.AlignTop | Qt.AlignRight)
        grilla.addWidget(self.empresas, 0, 2)
        grilla.addLayout(caja_botones, 0, 3)
        grilla.addWidget(self.espaciador, 1, 1)
        grilla.addLayout(caja_totales, 1, 2)
        marco = QGroupBox("Ingrese las empresas que componen la Licitacón")
        marco.setLayout(grilla)

        caja_horizontal = QHBoxLayout()
        caja_horizontal.addStretch(1)
        caja_horizontal.addWidget(boton_retroceder)
        caja_horizontal.addStretch(5)
        caja_horizontal.addWidget(boton_continuar)
        caja_horizontal.addStretch(1)
        caja_horizontal.setContentsMargins(10, 10, 10, 0)
        formulario = QFormLayout(self)
        formulario.addRow(marco)
        formulario.addRow(caja_horizontal)
        self.resize(self.sizeHint())
        #self.setMinimumHeight(self.height() + 100)
        self.setMinimumSize(self.size())
        self.setMaximumSize(self.size())
    
    def continuar(self):
        self.marcar_campos_erroneos()
        if self.empresas.rowCount() == 0:
            self.empresas.setFocus()
        else:
            self.estado = Estados.E_CONTINUAR
            self.accept()
    
    def retroceder(self):
        self.estado = Estados.E_RETROCEDER
        self.accept()
    
    #Es para evitar que se cierre el Dilog con la tecla ESC
    def reject(self):
        self.close()
    
    def marcar_campos_erroneos(self):
        self.marcar_empresas_erroneas()
    
    def marcar_empresas_erroneas(self):
        if self.empresas.rowCount() == 0:
            self.empresas_error.setVisible(True)
        else:
            self.empresas_error.setVisible(False)
    
    def agregar_empresa(self):
        mensaje = QMessageBox(self)
        mensaje.setWindowTitle("Empresa/Asociación")
        mensaje.setText("Indique si desea dar de alta una Empresa o una Asociación")
        boton_empresa = mensaje.addButton("Empresa", QMessageBox.YesRole)
        boton_asociacion = mensaje.addButton("Asociación", QMessageBox.NoRole)
        boton_cancelar = mensaje.addButton("Cancelar", QMessageBox.RejectRole)
        a = QPushButton()
        mensaje.setDefaultButton(boton_empresa)
        mensaje.exec()
        if mensaje.clickedButton() == boton_empresa:
            dialogo_empresa = DialogoEmpresa(parent=self, id_sugerido=self.id_sugerido(), universo_empresas=self.array_empresas)
            if dialogo_empresa.exec() == QDialog.Accepted:
                empresa = dialogo_empresa.obtener_empresa()
                self.cargar_linea_empresa(self.empresas.rowCount())
                self.cargar_datos_empresa(self.empresas.rowCount() - 1, empresa)
                self.empresas.setFocus()
                self.empresas.setCurrentItem(self.empresas.item(self.empresas.rowCount() -1, 0))
        elif mensaje.clickedButton() == boton_asociacion:
            dialogo_asociacion = DialogoAsociacion(parent=self, id_sugerido=self.id_sugerido(), universo_empresas=self.array_empresas)
            if dialogo_asociacion.exec() == QDialog.Accepted:
                empresa = dialogo_asociacion.obtener_asociacion()
                self.cargar_linea_empresa(self.empresas.rowCount())
                self.cargar_datos_empresa(self.empresas.rowCount() - 1, empresa)
                self.empresas.setFocus()
                self.empresas.setCurrentItem(self.empresas.item(self.empresas.rowCount() -1, 0))
        
    def cargar_linea_empresa(self, fila):
        #self.empresas.setSortingEnabled(False)
        self.empresas.insertRow(fila)
        item_id = QTableWidgetItem()
        item_nombre = QTableWidgetItem()
        item_es_asociacion = QTableWidgetItem()
        item_facturacion_media_anual = QTableWidgetItem()
        item_recursos_financieros = QTableWidgetItem()
        item_experiencia = QTableWidgetItem()
        item_cantidad_contratos = QTableWidgetItem()
        item_empresa = QTableWidgetItemEmpresa(None)

        item_es_asociacion.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

        self.empresas.setItem(fila, 0, item_id)
        self.empresas.setItem(fila, 1, item_nombre)
        self.empresas.setItem(fila, 2, item_es_asociacion)
        self.empresas.setItem(fila, 3, item_facturacion_media_anual)
        self.empresas.setItem(fila, 4, item_recursos_financieros)
        self.empresas.setItem(fila, 5, item_experiencia)
        self.empresas.setItem(fila, 6, item_cantidad_contratos)
        self.empresas.setItem(fila, 7, item_empresa)
        #self.empresas.setSortingEnabled(True)
    
    def cargar_datos_empresa(self, fila, empresa):
        self.array_empresas.append(empresa)

        item_id = self.empresas.item(fila, 0)
        item_nombre = self.empresas.item(fila, 1)
        item_es_asociacion = self.empresas.item(fila, 2)
        item_facturacion_media_anual = self.empresas.item(fila, 3)
        item_recursos_financieros = self.empresas.item(fila, 4)
        item_experiencia = self.empresas.item(fila, 5)
        item_cantidad_contratos = self.empresas.item(fila, 6)
        item_empresa = self.empresas.item(fila, 7)

        item_id.setText(str(empresa.id))
        item_nombre.setText(empresa.nombre)
        if empresa.es_asociacion():
            item_es_asociacion.setCheckState(Qt.Checked)
        else:
            item_es_asociacion.setCheckState(Qt.Unchecked)
        item_facturacion_media_anual.setText("{0:,.3f}".format(empresa.facturacion_media_anual()))
        item_recursos_financieros.setText("{0:,.3f}".format(empresa.recursos_financieros()))
        item_experiencia.setText("{0:,.3f}".format(sum(contrato.valor for contrato in empresa.contratos())))
        item_cantidad_contratos.setText(str(empresa.cantidad_contratos()))
        item_empresa.empresa = empresa
        self.actualizar_totales()

    def eliminar_empresa(self):
        if self.empresas.rowCount() != 0:
            self.array_empresas.remove(self.empresas.item(self.empresas.currentRow(), 7).empresa)
            self.empresas.removeRow(self.empresas.currentRow())
        self.marcar_empresas_erroneas()
        self.actualizar_totales()

    def editar_empresa(self):
        if self.empresas.rowCount() != 0:
            empresa = self.empresas.item(self.empresas.currentRow(), 7).empresa
            if empresa.es_asociacion():
                dialogo_asociacion = DialogoAsociacion(parent=self, asociacion=empresa, universo_empresas=self.array_empresas)
                if dialogo_asociacion.exec() == QDialog.Accepted:
                    self.array_empresas.remove(empresa)
                    empresa = dialogo_asociacion.obtener_asociacion()
                    self.cargar_datos_empresa(self.empresas.currentRow(), empresa)
            else:
                dialogo_empresa = DialogoEmpresa(parent=self, empresa=empresa, universo_empresas=self.array_empresas)
                if dialogo_empresa.exec() == QDialog.Accepted:
                    self.array_empresas.remove(empresa)
                    empresa = dialogo_empresa.obtener_empresa()
                    self.cargar_datos_empresa(self.empresas.currentRow(), empresa)
    
    def actualizar_totales(self):
        self.actualizar_cantidad_empresas()
    
    def actualizar_cantidad_empresas(self):
        if self.empresas.rowCount() == 1:
            empresa = " Empresa"
        else:
            empresa = " Empresas"
        self.cantidad_empresas.setText(str(self.empresas.rowCount()) + empresa)

    def cargar_empresas(self):
        for empresa in self.array_empresas_a_cargar:
            self.cargar_linea_empresa(self.empresas.rowCount())
            self.cargar_datos_empresa(self.empresas.rowCount() - 1, empresa)
        self.empresas.setFocus()
        self.empresas.setCurrentItem(self.empresas.item(self.empresas.rowCount()-1, 0))

    def obtener_empresas(self):
        return sorted(self.array_empresas, key=attrgetter("id"))
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Salir', "Está a punto de salir.\nEstá seguro que desea salir?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.estado = Estados.E_SALIR
            event.accept()
        else:
            event.ignore()
        
    def id_sugerido(self):
        id = None
        for i in range(1,100):
            if all(i != empresa.id for empresa in set.union(*[set(empresa.empresas_involucradas()) for empresa in self.array_empresas] + [set()])):
                id = i
                break
        return id
    
    def obtener_estado(self):
        return self.estado


if __name__ == '__main__':
    app = QApplication(sysargv)
    ex = DialogoEmpresas()
    while ex.exec() == QDialog.Accepted:
        empresas = ex.obtener_empresas()
        for empresa in empresas:
            print("--------------------")
            print(empresa.id)
            print(empresa.nombre)
            print(empresa.facturacion_media_anual())
            print(empresa.recursos_financieros())
            print(sum(contrato.valor for contrato in empresa.contratos()))
        ex = DialogoEmpresas()
    empresas = [Empresa(1, "Empresa 1", 1, 1, [Contrato(2017, 1), Contrato(2017, 1)]), Empresa(2, "Empresa 2", 2, 2, [Contrato(2017, 2), Contrato(2017, 2)]), Empresa(3, "Empresa 3", 3, 3, [Contrato(2017, 3), Contrato(2017, 3)]), Asociacion(1, "Asociacion 1",  [Empresa(10, "Empresa 10", 1, 1, [Contrato(2017, 1), Contrato(2017, 1)]), Empresa(20, "Empresa 20", 2, 2, [Contrato(2017, 2), Contrato(2017, 2)]), Empresa(30, "Empresa 30", 3, 3, [Contrato(2017, 3), Contrato(2017, 3)])])]
    ex = DialogoEmpresas(empresas=empresas)
    while ex.exec() == QDialog.Accepted:
        empresas1 = ex.obtener_empresas()
        for empresa in empresas1:
            print("--------------------")
            print(empresa.id)
            print(empresa.nombre)
            print(empresa.facturacion_media_anual())
            print(empresa.recursos_financieros())
            print(sum(contrato.valor for contrato in empresa.contratos()))
        ex = DialogoEmpresas(empresas=empresas)