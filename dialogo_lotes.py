from sys import argv as sysargv, exit as sysexit
from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, 
                             QStyle, QTableWidget, QGridLayout, QLabel, QVBoxLayout, QHeaderView, 
                             QAbstractItemView, QTableWidgetItem, QAbstractScrollArea, QFrame, 
                             QMainWindow, QWidget, QLayout, QMessageBox, QGroupBox)
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QModelIndex, QMimeData
from clases import Asociacion, Empresa, Contrato, Lote
from dialogo_lote import DialogoLote
from widgets_ocultos import QTableWidgetItemLote

class DialogoLotes(QDialog):
    def __init__(self, parent=None, lotes=None):
        super().__init__(parent=parent)
        self.dibujar_IU()
        self.array_lotes = []
        self.array_lotes_a_cargar = lotes
        if self.array_lotes_a_cargar != None:
            self.cargar_lotes()
            if self.lotes.rowCount() != 0:
                self.lotes.setFocus()
                self.lotes.setCurrentItem(self.lotes.item(0, 0))

    def dibujar_IU(self):
        self.setWindowTitle("Ingreso de Lotes")
        self.setWindowModality(Qt.ApplicationModal)
        self.setSizeGripEnabled(False)
        self.setContentsMargins(10, 10, 10, 10)

        self.lotes = QTableWidget(0, 6)
        self.lotes_error = QLabel("*")
        self.cantidad_lotes = QLabel("0 Lotes")
        self.espaciador = QLabel(" ")

        self.lotes.setHorizontalHeaderLabels(["Id", "Descripción", "Facturación Media Anual", "Recursos Financieros", "Experiencia", "Oculto"])
        self.lotes.verticalHeader().setVisible(False)
        self.lotes.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.lotes.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.lotes.horizontalHeader().hideSection(5)
        self.lotes.setSelectionMode(QAbstractItemView.SingleSelection)
        self.lotes.resizeColumnsToContents()
        self.lotes.setColumnWidth(0, self.lotes.columnWidth(0) + 10)
        self.lotes.setColumnWidth(1, self.lotes.columnWidth(1) + 150)
        self.lotes.setColumnWidth(3, self.lotes.columnWidth(2))
        self.lotes.setColumnWidth(4, self.lotes.columnWidth(2))
        self.lotes.resize(self.lotes.sizeHint())
        self.lotes.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.lotes.setFixedHeight(self.lotes.height() + 100)
        self.lotes.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lotes.cellChanged.connect(self.marcar_lotes_erroneos)
        self.lotes.setToolTip("Lotes que son licitados")
        self.lotes.doubleClicked.connect(self.editar_lote)
        self.lotes_error.setStyleSheet("QLabel {color : red}")
        self.lotes_error.setVisible(False)
        self.lotes_error.setFixedWidth(10)
        #self.cantidad_lotes.setFixedWidth(self.lotes.columnWidth(0))

        boton_continuar = QPushButton(QIcon("iconos/right-arrow.png"), "")
        boton_continuar.clicked.connect(self.continuar)
        boton_continuar.setDefault(True)
        boton_continuar.setMinimumSize(50, 10)
        boton_continuar.setToolTip("Continuar al ingreso de Empresas")
        boton_retroceder = QPushButton(QIcon("iconos/left-arrow.png"), "")
        boton_retroceder.clicked.connect(self.retroceder)
        boton_retroceder.setMinimumSize(50, 10)
        boton_retroceder.setToolTip("Retroceder al Menú Principal")
        boton_agregar_lote = QPushButton(QIcon("iconos/plus.png"), "")
        boton_agregar_lote.clicked.connect(self.agregar_lote)
        boton_agregar_lote.setMinimumSize(50, 10)
        boton_agregar_lote.setToolTip("Agregar nuevo Lote")
        boton_eliminar_lote = QPushButton(QIcon("iconos/minus.png"), "")
        boton_eliminar_lote.clicked.connect(self.eliminar_lote)
        boton_eliminar_lote.setMinimumSize(50, 10)
        boton_eliminar_lote.setToolTip("Eliminar Lote seleccionado")
        boton_editar_lote = QPushButton(QIcon("iconos/edit.png"), "")
        boton_editar_lote.clicked.connect(self.editar_lote)
        boton_editar_lote.setMinimumSize(50, 10)
        boton_editar_lote.setToolTip("Editar Lote seleccionado")
        caja_botones = QVBoxLayout()
        caja_botones.addStretch(1)
        caja_botones.addWidget(boton_agregar_lote)
        caja_botones.addWidget(boton_eliminar_lote)
        caja_botones.addWidget(boton_editar_lote)
        caja_botones.addStretch(5)
        caja_totales = QHBoxLayout()
        caja_totales.addWidget(self.cantidad_lotes)
        caja_totales.addStretch(1)

        grilla = QGridLayout()
        grilla.setColumnMinimumWidth(1, 20)
        #grilla.addWidget(QLabel("Lotes"), 0, 0, Qt.AlignTop)
        grilla.addWidget(self.lotes_error, 0, 1, Qt.AlignTop)
        grilla.addWidget(self.lotes, 0, 2)
        grilla.addLayout(caja_botones, 0, 3)
        grilla.addWidget(self.espaciador, 1, 1)
        grilla.addLayout(caja_totales, 1, 2)
        marco = QGroupBox("Ingrese los lotes que componen la Licitacón")
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
        self.setMinimumSize(self.sizeHint())
        self.setMaximumSize(self.sizeHint())
    
    def continuar(self):
        self.marcar_campos_erroneos()
        if self.lotes.rowCount() == 0:
            self.lotes.setFocus()
        else:
            self.accept()
    
    def retroceder(self):
        self.accept()
    
    #Es para evitar que se cierre el Dilog con la tecla ESC
    def reject(self):
        self.close()
    
    def marcar_campos_erroneos(self):
        self.marcar_lotes_erroneos()
    
    def marcar_lotes_erroneos(self):
        if self.lotes.rowCount() == 0:
            self.lotes_error.setVisible(True)
        else:
            self.lotes_error.setVisible(False)
    
    def agregar_lote(self):
        dialogo_lote = DialogoLote(parent=self, id_sugerido=self.id_sugerido(), universo_lotes=self.array_lotes)
        if dialogo_lote.exec() == QDialog.Accepted:
            lote = dialogo_lote.obtener_lote()
            self.cargar_linea_lote(self.lotes.rowCount())
            self.cargar_datos_lote(self.lotes.rowCount() - 1, lote)
            self.lotes.setFocus()
            self.lotes.setCurrentItem(self.lotes.item(self.lotes.rowCount() -1, 0))
        
    def cargar_linea_lote(self, fila):
        self.lotes.insertRow(fila)
        item_id = QTableWidgetItem()
        item_descripcion = QTableWidgetItem()
        item_facturacion_media_anual = QTableWidgetItem()
        item_recursos_financieros = QTableWidgetItem()
        item_experiencia = QTableWidgetItem()
        item_lote = QTableWidgetItemLote(None)

        self.lotes.setItem(fila, 0, item_id)
        self.lotes.setItem(fila, 1, item_descripcion)
        self.lotes.setItem(fila, 2, item_facturacion_media_anual)
        self.lotes.setItem(fila, 3, item_recursos_financieros)
        self.lotes.setItem(fila, 4, item_experiencia)
        self.lotes.setItem(fila, 5, item_lote)
    
    def cargar_datos_lote(self, fila, lote):
        self.array_lotes.append(lote)

        item_id = self.lotes.item(fila, 0)
        item_descripcion = self.lotes.item(fila, 1)
        item_facturacion_media_anual = self.lotes.item(fila, 2)
        item_recursos_financieros = self.lotes.item(fila, 3)
        item_experiencia = self.lotes.item(fila, 4)
        item_lote = self.lotes.item(fila, 5)

        item_id.setText(str(lote.id))
        item_descripcion.setText(lote.descripcion)
        item_facturacion_media_anual.setText("{0:,.3f}".format(lote.facturacion_media_anual))
        item_recursos_financieros.setText("{0:,.3f}".format(lote.recursos_financieros))
        item_experiencia.setText("{0:,.3f}".format(lote.experiencia))
        item_lote.lote = lote
        self.actualizar_totales()

    def eliminar_lote(self):
        if self.lotes.rowCount() != 0:
            self.array_lotes.remove(self.lotes.item(self.lotes.currentRow(), 5).lote)
            self.lotes.removeRow(self.lotes.currentRow())
        self.marcar_lotes_erroneos()
        self.actualizar_totales()

    def editar_lote(self):
        if self.lotes.rowCount() != 0:
            lote = self.lotes.item(self.lotes.currentRow(), 5).lote
            dialogo_lote = DialogoLote(parent=self, lote=lote, universo_lotes=self.array_lotes)
            if dialogo_lote.exec() == QDialog.Accepted:
                self.array_lotes.remove(lote)
                lote = dialogo_lote.obtener_lote()
                self.cargar_datos_lote(self.lotes.currentRow(), lote)
            

    def actualizar_totales(self):
        self.actualizar_cantidad_lotes()
    
    def actualizar_cantidad_lotes(self):
        if self.lotes.rowCount() == 1:
            lote = " Lote"
        else:
            lote = " Lotes"
        self.cantidad_lotes.setText(str(self.lotes.rowCount()) + lote)

    def cargar_lotes(self):
        for lote in self.array_lotes_a_cargar:
            self.cargar_linea_lote(self.lotes.rowCount())
            self.cargar_datos_lote(self.lotes.rowCount() - 1, lote)
        self.lotes.setFocus()
        self.lotes.setCurrentItem(self.lotes.item(self.lotes.rowCount()-1, 0))

    def obtener_lotes(self):
        return self.array_lotes
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Salir', "Está a punto de salir.\nEstá seguro que desea salir?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    def id_sugerido(self):
        id = None
        for i in range(1,100):
            if all(lote.id != i for lote in self.array_lotes):
                id = i
                break
        return id


if __name__ == '__main__':
    app = QApplication(sysargv)
    ex = DialogoLotes()
    while ex.exec() == QDialog.Accepted:
        lotes = ex.obtener_lotes()
        for lote in lotes:
            print("--------------------")
            print(lote.id)
            print(lote.descripcion)
            print(lote.facturacion_media_anual)
            print(lote.recursos_financieros)
            print(lote.experiencia)
        ex = DialogoLotes()
    lotes = [Lote(1, 1, 1, 1), Lote(2, 2.2, 2.22, 2.222), Lote(3, 3.3, 3.33, 3.333)]
    ex = DialogoLotes(lotes=lotes)
    while ex.exec() == QDialog.Accepted:
        lotes1 = ex.obtener_lotes()
        for lote in lotes1:
            print("--------------------")
            print(lote.id)
            print(lote.descripcion)
            print(lote.facturacion_media_anual)
            print(lote.recursos_financieros)
            print(lote.experiencia)
        ex = DialogoLotes(lotes=lotes)

