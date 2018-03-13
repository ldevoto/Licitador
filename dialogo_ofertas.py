from sys import argv as sysargv, exit as sysexit
from operator import itemgetter, attrgetter
from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, 
                             QStyle, QTableWidget, QGridLayout, QLabel, QVBoxLayout, QHeaderView, 
                             QAbstractItemView, QTableWidgetItem, QAbstractScrollArea, QFrame, 
                             QMainWindow, QWidget, QLayout, QMessageBox, QGroupBox, QShortcut)
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QModelIndex, QMimeData
from clases import Asociacion, Empresa, Contrato, Lote, ConjuntoOfertas, Oferta
from dialogo_oferta import DialogoOferta
from widgets_ocultos import QTableWidgetItemEmpresa, Estados

class DialogoOfertas(QDialog):
    def __init__(self, parent=None, ofertas=None, lotes=None, empresas=None):
        super().__init__(parent=parent)
        self.estado = Estados.E_INDETERMINADO
        self.dibujar_IU()
        self.array_lotes = lotes
        self.array_empresas = empresas
        self.array_ofertas = []
        self.array_ofertas_a_cargar = ofertas
        if self.array_ofertas_a_cargar != None:
            self.cargar_ofertas()
            if self.ofertas.rowCount() != 0:
                self.ofertas.setFocus()
                self.ofertas.setCurrentItem(self.ofertas.item(0, 0))

    def dibujar_IU(self):
        self.setWindowTitle("Ingreso de Ofertas")
        self.setWindowModality(Qt.ApplicationModal)
        self.setSizeGripEnabled(False)
        self.setContentsMargins(10, 10, 10, 10)

        self.ofertas = QTableWidget(0, 4)
        self.ofertas_error = QLabel("*")
        self.cantidad_ofertas = QLabel("0 Ofertas")
        self.espaciador = QLabel(" ")

        self.ofertas.setHorizontalHeaderLabels(["Empresa/Asociación", "Lote", "Valor", "Oculto"])
        self.ofertas.verticalHeader().setVisible(False)
        self.ofertas.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.ofertas.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.ofertas.horizontalHeader().hideSection(3)
        self.ofertas.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ofertas.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ofertas.resizeColumnsToContents()
        self.ofertas.setColumnWidth(0, 250)
        self.ofertas.setColumnWidth(1, self.ofertas.columnWidth(0))
        self.ofertas.setColumnWidth(2, 200)
        #self.ofertas.setColumnWidth(5, self.ofertas.columnWidth(3))
        self.ofertas.resize(self.ofertas.sizeHint())
        self.ofertas.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.ofertas.setFixedHeight(self.ofertas.height() + 100)
        self.ofertas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ofertas.cellChanged.connect(self.marcar_ofertas_erroneas)
        self.ofertas.setToolTip("Ofertas de todas las Empresas sobre los lotes")
        self.ofertas.doubleClicked.connect(self.editar_oferta)
        self.ofertas_error.setStyleSheet("QLabel {color : red}")
        self.ofertas_error.setVisible(False)
        self.ofertas_error.setFixedWidth(10)
        #self.cantidad_ofertas.setFixedWidth(self.ofertas.columnWidth(0))

        boton_continuar = QPushButton(QIcon("iconos/right-arrow.png"), "")
        boton_continuar.clicked.connect(self.continuar)
        boton_continuar.setDefault(True)
        boton_continuar.setMinimumSize(50, 10)
        boton_continuar.setToolTip("Continuar al ingreso de Descuentos")
        boton_retroceder = QPushButton(QIcon("iconos/left-arrow.png"), "")
        boton_retroceder.clicked.connect(self.retroceder)
        boton_retroceder.setMinimumSize(50, 10)
        boton_retroceder.setToolTip("Retroceder al ingreso de Empresas")
        boton_agregar_oferta = QPushButton(QIcon("iconos/plus.png"), "")
        boton_agregar_oferta.clicked.connect(self.agregar_oferta)
        boton_agregar_oferta.setMinimumSize(50, 10)
        boton_agregar_oferta.setToolTip("Agregar nueva Oferta")
        boton_eliminar_oferta = QPushButton(QIcon("iconos/minus.png"), "")
        boton_eliminar_oferta.clicked.connect(self.eliminar_oferta)
        boton_eliminar_oferta.setMinimumSize(50, 10)
        boton_eliminar_oferta.setToolTip("Eliminar Oferta seleccionada")
        boton_editar_oferta = QPushButton(QIcon("iconos/edit.png"), "")
        boton_editar_oferta.clicked.connect(self.editar_oferta)
        boton_editar_oferta.setMinimumSize(50, 10)
        boton_editar_oferta.setToolTip("Editar Empresa seleccionada")
        caja_botones = QVBoxLayout()
        caja_botones.addStretch(1)
        caja_botones.addWidget(boton_agregar_oferta)
        caja_botones.addWidget(boton_eliminar_oferta)
        caja_botones.addWidget(boton_editar_oferta)
        caja_botones.addStretch(5)
        caja_totales = QHBoxLayout()
        caja_totales.addWidget(self.cantidad_ofertas)
        caja_totales.addStretch(1)

        grilla = QGridLayout()
        grilla.setColumnMinimumWidth(1, 20)
        #grilla.addWidget(QLabel("Lotes"), 0, 0, Qt.AlignTop)
        grilla.addWidget(self.ofertas_error, 0, 1, Qt.AlignTop)
        grilla.addWidget(self.ofertas, 0, 2)
        grilla.addLayout(caja_botones, 0, 3)
        grilla.addWidget(self.espaciador, 1, 1)
        grilla.addLayout(caja_totales, 1, 2)
        marco = QGroupBox("Ingrese las Ofertas que conforman la licitación")
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
        if self.ofertas.rowCount() == 0:
            self.ofertas.setFocus()
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
        self.marcar_ofertas_erroneas()
    
    def marcar_ofertas_erroneas(self):
        if self.ofertas.rowCount() == 0:
            self.ofertas_error.setVisible(True)
        else:
            self.ofertas_error.setVisible(False)
    
    def agregar_oferta(self):
        dialogo_oferta = DialogoOferta(parent=self, lotes=self.array_lotes, empresas=self.array_empresas, conjunto_ofertas=self.obtener_conjunto_ofertas())
        if dialogo_oferta.exec() == QDialog.Accepted:
            oferta = dialogo_oferta.obtener_oferta()
            self.cargar_linea_oferta(self.ofertas.rowCount())
            self.cargar_datos_oferta(self.ofertas.rowCount() - 1, oferta)
            self.ofertas.setFocus()
            self.ofertas.setCurrentItem(self.ofertas.item(self.ofertas.rowCount() -1, 0))
        
    def cargar_linea_oferta(self, fila):
        self.ofertas.insertRow(fila)
        item_empresa = QTableWidgetItem()
        item_lote = QTableWidgetItem()
        item_valor = QTableWidgetItem()
        item_oferta = QTableWidgetItem()

        self.ofertas.setItem(fila, 0, item_empresa)
        self.ofertas.setItem(fila, 1, item_lote)
        self.ofertas.setItem(fila, 2, item_valor)
        self.ofertas.setItem(fila, 3, item_oferta)
    
    def cargar_datos_oferta(self, fila, oferta):
        self.array_ofertas.append(oferta)

        item_empresa = self.ofertas.item(fila, 0)
        item_lote = self.ofertas.item(fila, 1)
        item_valor = self.ofertas.item(fila, 2)
        item_oferta = self.ofertas.item(fila, 3)

        item_empresa.setText(oferta.empresa.nombre.strip())
        if oferta.lote.descripcion != "":
            item_lote.setText("{0}".format(oferta.lote.descripcion.strip()))
        else:
            item_lote.setText("Lote {0}".format(oferta.lote.id))
        item_valor.setText("{0:,.3f}".format(oferta.valor))
        item_oferta.setData(1, oferta)

        self.actualizar_totales()

    def eliminar_oferta(self):
        if self.ofertas.rowCount() != 0:
            self.array_ofertas.remove(self.ofertas.item(self.ofertas.currentRow(), 3).data(1))
            self.ofertas.removeRow(self.ofertas.currentRow())
        self.marcar_ofertas_erroneas()
        self.actualizar_totales()

    def editar_oferta(self):
        if self.ofertas.rowCount() != 0:
            oferta = self.ofertas.item(self.ofertas.currentRow(), 3).data(1)
            dialogo_oferta = DialogoOferta(parent=self, oferta=oferta, lotes=self.array_lotes, empresas=self.array_empresas, conjunto_ofertas=self.obtener_conjunto_ofertas())
            if dialogo_oferta.exec() == QDialog.Accepted:
                self.array_ofertas.remove(oferta)
                oferta = dialogo_oferta.obtener_oferta()
                self.cargar_datos_oferta(self.ofertas.currentRow(), oferta)

    def actualizar_totales(self):
        self.actualizar_cantidad_ofertas()
    
    def actualizar_cantidad_ofertas(self):
        if self.ofertas.rowCount() == 1:
            oferta = " Oferta"
        else:
            oferta = " Ofertas"
        self.cantidad_ofertas.setText(str(self.ofertas.rowCount()) + oferta)

    def cargar_ofertas(self):
        self.normalizar_ofertas()
        for oferta in self.array_ofertas_a_cargar:
            self.cargar_linea_oferta(self.ofertas.rowCount())
            self.cargar_datos_oferta(self.ofertas.rowCount() - 1, oferta)
        self.ofertas.setFocus()
        self.ofertas.setCurrentItem(self.ofertas.item(self.ofertas.rowCount()-1, 0))

    def normalizar_ofertas(self):
        array_ofertas = []
        ofertas_a_eliminar = set()
        for oferta in self.array_ofertas_a_cargar:
            if all(lote != oferta.lote for lote in self.array_lotes):
                if all(lote.id != oferta.lote.id for lote in self.array_lotes):
                    ofertas_a_eliminar.add(oferta)
                else:
                    for lote in self.array_lotes:
                        if lote.id == oferta.lote.id:
                            oferta.lote = lote
            if all(empresa != oferta.empresa for empresa in self.array_empresas):
                if all(empresa.id != oferta.empresa.id for empresa in self.array_empresas):
                    ofertas_a_eliminar.add(oferta)
                else:
                    for empresa in self.array_empresas:
                        if empresa.id == oferta.empresa.id:
                            oferta.empresa = empresa
        for oferta in ofertas_a_eliminar:
            self.array_ofertas_a_cargar.remove(oferta)

    def obtener_ofertas(self):
        return sorted(self.array_ofertas, key=attrgetter("empresa.id"))
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Salir', "Está a punto de salir.\nEstá seguro que desea salir?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.estado = Estados.E_SALIR
            event.accept()
        else:
            event.ignore()
        
    def obtener_conjunto_ofertas(self):
        conjunto_ofertas = ConjuntoOfertas()
        for oferta in self.array_ofertas:
            conjunto_ofertas.agregar_oferta(oferta)
        return conjunto_ofertas
    
    def obtener_estado(self):
        return self.estado


if __name__ == '__main__':
    app = QApplication(sysargv)
    lotes = [Lote(1, 1, 1, 1), Lote(2, 2.2, 2.22, 2.222), Lote(3, 3.3, 3.33, 3.333)]
    empresas = [Empresa(1, "Empresa 1", 1, 1, [Contrato(2017, 1), Contrato(2017, 1)]), Empresa(2, "Empresa 2", 2, 2, [Contrato(2017, 2), Contrato(2017, 2)]), Empresa(3, "Empresa 3", 3, 3, [Contrato(2017, 3), Contrato(2017, 3)]), Asociacion(1, "Asociacion 1",  [Empresa(10, "Empresa 10", 1, 1, [Contrato(2017, 1), Contrato(2017, 1)]), Empresa(20, "Empresa 20", 2, 2, [Contrato(2017, 2), Contrato(2017, 2)]), Empresa(30, "Empresa 30", 3, 3, [Contrato(2017, 3), Contrato(2017, 3)])])]
    ex = DialogoOfertas(lotes=lotes, empresas=empresas)
    while ex.exec() == QDialog.Accepted:
        ofertas1 = ex.obtener_ofertas()
        for oferta in ofertas1:
            print("--------------------")
            print(oferta.empresa.nombre)
            print(oferta.lote.id)
            print(oferta.valor)
        ex = DialogoOfertas(lotes=lotes, empresas=empresas)
    oferta1 = Oferta(empresas[0], lotes[0], 12312)
    oferta2 = Oferta(empresas[1], lotes[1], 23434)
    ofertas = [oferta1, oferta2]
    ex = DialogoOfertas(ofertas=ofertas, lotes=lotes, empresas=empresas)
    while ex.exec() == QDialog.Accepted:
        ofertas1 = ex.obtener_ofertas()
        for oferta in ofertas1:
            print("--------------------")
            print(oferta.empresa.nombre)
            print(oferta.lote.id)
            print(oferta.valor)
        ex = DialogoOfertas(ofertas=ofertas, lotes=lotes, empresas=empresas)
