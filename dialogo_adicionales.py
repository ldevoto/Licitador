from sys import argv as sysargv, exit as sysexit
from operator import itemgetter, attrgetter
from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, 
                             QStyle, QTableWidget, QGridLayout, QLabel, QVBoxLayout, QHeaderView, 
                             QAbstractItemView, QTableWidgetItem, QAbstractScrollArea, QFrame, 
                             QMainWindow, QWidget, QLayout, QMessageBox, QGroupBox, QShortcut)
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QModelIndex, QMimeData
from clases import Asociacion, Empresa, Contrato, Lote, ConjuntoOfertas, Oferta, Adicional
from dialogo_oferta import DialogoOferta
from dialogo_adicional import DialogoAdicional
from widgets_ocultos import QTableWidgetItemEmpresa, Estados

class DialogoAdicionales(QDialog):
    def __init__(self, parent=None, lotes=None, empresas=None, ofertas=None, adicionales=None):
        super().__init__(parent=parent)
        self.estado = Estados.E_INDETERMINADO
        self.array_lotes = sorted(lotes, key=attrgetter("id"))
        self.array_empresas = sorted(empresas, key=attrgetter("id"))
        self.array_ofertas = ofertas
        self.array_adicionales = []
        self.array_adicionales_a_cargar = adicionales
        self.dibujar_IU()
        if self.array_adicionales_a_cargar != None:
            self.array_adicionales_a_cargar = sorted(adicionales, key=attrgetter("empresa.id"))
            self.cargar_adicionales()
            if self.adicionales.rowCount() != 0:
                self.adicionales.setFocus()
                self.adicionales.setCurrentItem(self.adicionales.item(0, 0))

    def dibujar_IU(self):
        self.setWindowTitle("Ingreso de Descuentos")
        self.setWindowModality(Qt.ApplicationModal)
        self.setSizeGripEnabled(False)
        self.setContentsMargins(10, 10, 10, 10)

        self.adicionales = QTableWidget(0, len(self.array_lotes) + 3)
        self.adicionales_error = QLabel("*")
        self.cantidad_adicionales = QLabel("0 Descuentos")
        self.espaciador = QLabel(" ")

        self.adicionales.verticalHeader().setVisible(False)
        self.adicionales.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.adicionales.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.adicionales.horizontalHeader().hideSection(2)
        self.adicionales.setSelectionMode(QAbstractItemView.SingleSelection)
        self.adicionales.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.adicionales.setMaximumWidth(1000)
        self.adicionales.resizeColumnsToContents()
        self.adicionales.setColumnWidth(0, 250)
        self.adicionales.setColumnWidth(1, 100)
        encabezados = ["Empresa/Asociación", "Porcentaje", "Oculto"]
        for i,lote in enumerate(self.array_lotes):
            if lote.descripcion != "":
                encabezados.append("{0}".format(lote.descripcion.strip()))
            else:
                encabezados.append("Lote {0}".format(lote.id))
            self.adicionales.setColumnWidth(i+3, 100)
        self.adicionales.setHorizontalHeaderLabels(encabezados)
        self.adicionales.resize(self.adicionales.sizeHint())
        self.adicionales.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.adicionales.setFixedHeight(self.adicionales.height() + 100)
        self.adicionales.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.adicionales.cellChanged.connect(self.marcar_ofertas_erroneas)
        self.adicionales.setToolTip("Descuentos ofrecidos por las Empresas por un conjunto de Lotes adjudicado")
        self.adicionales.doubleClicked.connect(self.editar_adicional)
        self.adicionales_error.setStyleSheet("QLabel {color : red}")
        self.adicionales_error.setVisible(False)
        self.adicionales_error.setFixedWidth(10)

        boton_continuar = QPushButton(QIcon("iconos/right-arrow.png"), "")
        boton_continuar.clicked.connect(self.continuar)
        boton_continuar.setDefault(True)
        boton_continuar.setMinimumSize(50, 10)
        boton_continuar.setToolTip("Continuar al ingreso de Descuentos")
        boton_retroceder = QPushButton(QIcon("iconos/left-arrow.png"), "")
        boton_retroceder.clicked.connect(self.retroceder)
        boton_retroceder.setMinimumSize(50, 10)
        boton_retroceder.setToolTip("Retroceder al ingreso de Empresas")
        boton_agregar_adicional = QPushButton(QIcon("iconos/plus.png"), "")
        boton_agregar_adicional.clicked.connect(self.agregar_adicional)
        boton_agregar_adicional.setMinimumSize(50, 10)
        boton_agregar_adicional.setToolTip("Agregar nueva Oferta")
        boton_eliminar_adicional = QPushButton(QIcon("iconos/minus.png"), "")
        boton_eliminar_adicional.clicked.connect(self.eliminar_adicional)
        boton_eliminar_adicional.setMinimumSize(50, 10)
        boton_eliminar_adicional.setToolTip("Eliminar Oferta seleccionada")
        boton_editar_adicional = QPushButton(QIcon("iconos/edit.png"), "")
        boton_editar_adicional.clicked.connect(self.editar_adicional)
        boton_editar_adicional.setMinimumSize(50, 10)
        boton_editar_adicional.setToolTip("Editar Empresa seleccionada")
        caja_botones = QVBoxLayout()
        caja_botones.addStretch(1)
        caja_botones.addWidget(boton_agregar_adicional)
        caja_botones.addWidget(boton_eliminar_adicional)
        caja_botones.addWidget(boton_editar_adicional)
        caja_botones.addStretch(5)
        caja_totales = QHBoxLayout()
        caja_totales.addWidget(self.cantidad_adicionales)
        caja_totales.addStretch(1)

        grilla = QGridLayout()
        grilla.setColumnMinimumWidth(1, 20)
        #grilla.addWidget(QLabel("Lotes"), 0, 0, Qt.AlignTop)
        grilla.addWidget(self.adicionales_error, 0, 1, Qt.AlignTop)
        grilla.addWidget(self.adicionales, 0, 2)
        grilla.addLayout(caja_botones, 0, 3)
        grilla.addWidget(self.espaciador, 1, 1)
        grilla.addLayout(caja_totales, 1, 2)
        marco = QGroupBox("Ingrese los Descuentos ofrecidos por las Empresas")
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
        #if self.adicionales.rowCount() == 0:
        #    self.adicionales.setFocus()
        #else:
        self.estado = Estados.E_CONTINUAR
        self.accept()
    
    def retroceder(self):
        self.estado = Estados.E_RETROCEDER
        self.accept()
    
    #Es para evitar que se cierre el Dilog con la tecla ESC
    def reject(self):
        self.close()
    
    def marcar_campos_erroneos(self):
        #self.marcar_ofertas_erroneas()
        pass
    
    def marcar_ofertas_erroneas(self):
        if self.adicionales.rowCount() == 0:
            self.adicionales_error.setVisible(True)
        else:
            self.adicionales_error.setVisible(False)
    
    def agregar_adicional(self):
        dialogo_adicional = DialogoAdicional(parent=self, lotes=self.array_lotes, empresas=self.array_empresas, ofertas=self.array_ofertas, adicionales=self.array_adicionales)
        if dialogo_adicional.exec() == QDialog.Accepted:
            adicional = dialogo_adicional.obtener_adicional()
            self.cargar_linea_adicional(self.adicionales.rowCount())
            self.cargar_datos_adicional(self.adicionales.rowCount() - 1, adicional)
            self.adicionales.setFocus()
            self.adicionales.setCurrentItem(self.adicionales.item(self.adicionales.rowCount() -1, 0))
        
    def cargar_linea_adicional(self, fila):
        self.adicionales.insertRow(fila)
        item_empresa = QTableWidgetItem()
        item_porcentaje = QTableWidgetItem()
        item_adicional = QTableWidgetItem()

        self.adicionales.setItem(fila, 0, item_empresa)
        self.adicionales.setItem(fila, 1, item_porcentaje)
        self.adicionales.setItem(fila, 2, item_adicional)

        for i,lote in enumerate(self.array_lotes):
            item_lote = QTableWidgetItem()
            item_lote.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.adicionales.setItem(fila, i+3, item_lote)
    
    def cargar_datos_adicional(self, fila, adicional):
        self.array_adicionales.append(adicional)

        item_empresa = self.adicionales.item(fila, 0)
        item_porcentaje = self.adicionales.item(fila, 1)
        item_adicional = self.adicionales.item(fila, 2)

        item_empresa.setText(adicional.empresa.nombre.strip())
        item_porcentaje.setText(str(adicional.porcentaje * -1))
        item_adicional.setData(1, adicional)

        for i, lote in enumerate(self.array_lotes):
            item_lote = self.adicionales.item(fila, i+3)
            if adicional.conjunto_ofertas.lote_contenido(lote):
                item_lote.setCheckState(Qt.Checked)
            else:
                item_lote.setCheckState(Qt.Unchecked)

        self.actualizar_totales()

    def eliminar_adicional(self):
        if self.adicionales.rowCount() != 0:
            self.array_adicionales.remove(self.adicionales.item(self.adicionales.currentRow(), 2).data(1))
            self.adicionales.removeRow(self.adicionales.currentRow())
        self.marcar_ofertas_erroneas()
        self.actualizar_totales()

    def editar_adicional(self):
        if self.adicionales.rowCount() != 0:
            adicional = self.adicionales.item(self.adicionales.currentRow(), 2).data(1)
            dialogo_adicional = DialogoAdicional(parent=self, adicional=adicional, lotes=self.array_lotes, empresas=self.array_empresas, ofertas=self.array_ofertas, adicionales=self.array_adicionales)
            if dialogo_adicional.exec() == QDialog.Accepted:
                self.array_adicionales.remove(adicional)
                adicional = dialogo_adicional.obtener_adicional()
                self.cargar_datos_adicional(self.adicionales.currentRow(), adicional)

    def actualizar_totales(self):
        self.actualizar_cantidad_adicionales()
    
    def actualizar_cantidad_adicionales(self):
        if self.adicionales.rowCount() == 1:
            adicional = " Adicional"
        else:
            adicional = " Adicionales"
        self.cantidad_adicionales.setText(str(self.adicionales.rowCount()) + adicional)

    def cargar_adicionales(self):
        self.normalizar_adicionales()
        for adicional in self.array_adicionales_a_cargar:
            self.cargar_linea_adicional(self.adicionales.rowCount())
            self.cargar_datos_adicional(self.adicionales.rowCount() - 1, adicional)
        self.adicionales.setFocus()
        self.adicionales.setCurrentItem(self.adicionales.item(self.adicionales.rowCount()-1, 0))

    def normalizar_adicionales(self):
        adicionales_a_eliminar = set()
        for adicional in self.array_adicionales_a_cargar:
            for oferta in adicional.conjunto_ofertas.ofertas:
                if oferta not in self.array_ofertas:
                    if (oferta.lote.id, oferta.empresa.id) not in [(oferta1.lote.id, oferta1.empresa.id) for oferta1 in self.array_ofertas]:
                        adicionales_a_eliminar.add(adicional)
                        break
            if all(empresa != adicional.empresa for empresa in self.array_empresas):
                if all(empresa.id != adicional.empresa.id for empresa in self.array_empresas):
                    adicionales_a_eliminar.add(adicional)
                    continue
                else:
                    for empresa in self.array_empresas:
                        if empresa.id == adicional.empresa.id:
                            adicional.empresa = empresa
                            for oferta in adicional.conjunto_ofertas.ofertas:
                                oferta.empresa = empresa
                            break
            for oferta in adicional.conjunto_ofertas.ofertas:
                if any(oferta.lote.id == oferta1.lote.id for oferta1 in self.array_ofertas):
                    for oferta_del_array in self.array_ofertas:
                        if oferta.lote.id == oferta_del_array.lote.id:
                            if oferta.lote != oferta_del_array.lote:
                                oferta.lote = oferta_del_array.lote
                else:
                    adicionales_a_eliminar.add(adicional)
                    continue
        for adicional in adicionales_a_eliminar:
            self.array_adicionales_a_cargar.remove(adicional)

    def obtener_adicionales(self):
        return sorted(self.array_adicionales, key=attrgetter("empresa.id"))
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Salir', "Está a punto de salir.\nEstá seguro que desea salir?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.estado = Estados.E_SALIR
            event.accept()
        else:
            event.ignore()
        
    def obtener_conjunto_ofertas(self):
        conjunto_ofertas = ConjuntoOfertas()
        for oferta in self.array_adicionales:
            conjunto_ofertas.agregar_adicional(oferta)
        return conjunto_ofertas
    
    def obtener_estado(self):
        return self.estado


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
    ex = DialogoAdicionales(lotes=lotes, empresas=empresas, ofertas=ofertas)
    while ex.exec() == QDialog.Accepted:
        adicionales1 = ex.obtener_adicionales()
        for adicional in adicionales1:
            print("--------------------")
            print(adicional.empresa.nombre)
            print(adicional.porcentaje)
            for lote in adicional.conjunto_ofertas.lotes_ofertados():
                print(lote.id)
        ex = DialogoAdicionales(lotes=lotes, empresas=empresas, ofertas=ofertas)
    ex = DialogoAdicionales(lotes=lotes, empresas=empresas, ofertas=ofertas, adicionales=[adicional1, adicional2])
    while ex.exec() == QDialog.Accepted:
        adicionales1 = ex.obtener_adicionales()
        for adicional in adicionales1:
            print("--------------------")
            print(adicional.empresa.nombre)
            print(adicional.porcentaje)
            for lote in adicional.conjunto_ofertas.lotes_ofertados():
                print(lote.id)
        ex = DialogoAdicionales(lotes=lotes, empresas=empresas, ofertas=ofertas, adicionales=[adicional1, adicional2])
