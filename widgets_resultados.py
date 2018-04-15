from sys import argv as sysargv, exit as sysexit
from time import sleep
from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, 
                             QStyle, QTableWidget, QGridLayout, QLabel, QVBoxLayout, QHeaderView, 
                             QAbstractItemView, QTableWidgetItem, QAbstractScrollArea, QFrame, 
                             QMainWindow, QWidget, QLayout, QMessageBox, QGroupBox, QShortcut, QStackedWidget, QScrollArea, QSizePolicy, QCheckBox)
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator, QKeySequence, QFont, QClipboard, QGuiApplication
from PyQt5.QtCore import Qt, QModelIndex, QMimeData, QSize, QEvent
from clases import Asociacion, Empresa, Contrato, Combinacion, Licitador
from widgets_ocultos import Estados, MensajeSalida
from io import StringIO
from csv import writer

class QWidgetPrincipal(QWidget):
    def __init__(self, licitacion, titulo, widget_principal, parent=None):
        super().__init__(parent=parent)
        self.licitacion = licitacion
        self.titulo = titulo
        self.widget_principal = widget_principal
        self.dibujar_IU()
    
    def dibujar_IU(self):
        contenedor = QHBoxLayout()
        marco_general = QGroupBox(self.titulo)
        self.caja_general = QVBoxLayout()
        self.scroll_general = QScrollArea()

        self.scroll_general.setWidget(self.widget_principal)
        self.caja_general.addWidget(self.scroll_general)
        marco_general.setLayout(self.caja_general)
        contenedor.addWidget(marco_general)
        self.setLayout(contenedor)

        self.scroll_general.setObjectName("Scroll")
        self.widget_principal.setObjectName("WidgetPrincipal")
        self.scroll_general.setStyleSheet("#Scroll {border:0px solid black; background:transparent}")
        self.widget_principal.setStyleSheet("#WidgetPrincipal {background:transparent}")

        self.resize(self.sizeHint())


class WidgetCombinacionGanadora(QWidget):
    def __init__(self, licitacion, parent=None):
        super().__init__(parent=parent)
        self.licitacion = licitacion
        self.combinacion_ganadora = self.licitacion.combinacion_ganadora()
        self.caja_principal = QVBoxLayout()
        self.marco_lote = QGroupBox("Por Lote")
        self.caja_lote = QGridLayout()
        self.tabla_lote = QTableWidget(5, 1)
        self.marco_totales = QGroupBox("Totales")
        self.caja_totales = QHBoxLayout()
        self.formulario_totales = QFormLayout()

        self.llenar_tabla_lote()
        self.llenar_formulario_totales()
        self.tabla_lote.setStyleSheet("QTableWidget {border:0px solid transparent}")
        self.tabla_lote.horizontalHeader().setVisible(False)
        self.tabla_lote.verticalHeader().setVisible(False)
        self.tabla_lote.setEnabled(True)
        self.tabla_lote.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tabla_lote.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tabla_lote.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla_lote.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.installEventFilter(self)
        self.formulario_totales.setHorizontalSpacing(25)
        self.resizeColumnsToMaximumContent()

        self.caja_lote.addWidget(self.tabla_lote, 0, 0)
        self.caja_lote.setColumnStretch(1, 1)
        self.marco_totales.setLayout(self.caja_totales)
        self.caja_totales.addLayout(self.formulario_totales)
        self.caja_totales.addStretch(1)
        self.marco_lote.setLayout(self.caja_lote)
        self.caja_principal.addWidget(self.marco_lote)
        self.caja_principal.addWidget(self.marco_totales)
        self.caja_principal.addStretch(1)
        self.setLayout(self.caja_principal)
        self.resize(self.sizeHint())

    def llenar_tabla_lote(self):
        fuente_negrita = QFont()
        print(fuente_negrita.family())
        #fuente_negrita.setBold(True)
        item_lotes = QTableWidgetItem("Lote")
        item_lotes.setFont(fuente_negrita)
        item_empresas = QTableWidgetItem("Empresa")
        item_empresas.setFont(fuente_negrita)
        item_ofertas = QTableWidgetItem("Oferta")
        item_ofertas.setFont(fuente_negrita)
        item_descuentos = QTableWidgetItem("Descuento")
        item_descuentos.setFont(fuente_negrita)
        item_ofertas_finales = QTableWidgetItem("Oferta Final")
        item_ofertas_finales.setFont(fuente_negrita)
        self.tabla_lote.setItem(0, 0, item_lotes)
        self.tabla_lote.setItem(1, 0, item_empresas)
        self.tabla_lote.setItem(2, 0, item_ofertas)
        self.tabla_lote.setItem(3, 0, item_descuentos)
        self.tabla_lote.setItem(4, 0, item_ofertas_finales)
        for lote in self.licitacion.lotes:
            self.tabla_lote.setColumnCount(self.tabla_lote.columnCount() + 1)
            columna = self.tabla_lote.columnCount() - 1
            item_lote = QTableWidgetItem(lote.obtener_descripcion())
            item_lote.setTextAlignment(Qt.AlignCenter)
            self.tabla_lote.setItem(0, columna, item_lote)
            for posibilidad in self.licitacion.combinacion_ganadora().posibilidades:
                if posibilidad.lote_contenido(lote):
                    for oferta in posibilidad.conjunto_ofertas.ofertas:
                        if oferta.lote == lote:
                            item_empresa = QTableWidgetItem(oferta.empresa.nombre)
                            item_empresa.setTextAlignment(Qt.AlignCenter)
                            self.tabla_lote.setItem(1, columna, item_empresa)
                            item_oferta = QTableWidgetItem("{0:,.3f}".format(oferta.valor))
                            item_oferta.setTextAlignment(Qt.AlignCenter)
                            self.tabla_lote.setItem(2, columna, item_oferta)
                            if posibilidad.adicional.es_nulo() or not posibilidad.adicional.conjunto_ofertas.oferta_contenida(oferta):
                                item_descuento = QTableWidgetItem("{0:.3f}%".format(0))
                                item_descuento.setTextAlignment(Qt.AlignCenter)
                                self.tabla_lote.setItem(3, columna, item_descuento)
                                item_oferta_final = QTableWidgetItem("{0:,.3f}".format(oferta.valor))
                                item_oferta_final.setTextAlignment(Qt.AlignCenter)
                                self.tabla_lote.setItem(4, columna, item_oferta_final)
                            else:
                                item_descuento = QTableWidgetItem("{0:.2f}%".format(abs(posibilidad.adicional.porcentaje)))
                                item_descuento.setTextAlignment(Qt.AlignCenter)
                                self.tabla_lote.setItem(3, columna, item_descuento)
                                item_oferta_final = QTableWidgetItem("{0:,.3f}".format(oferta.valor + posibilidad.adicional.valor_en_oferta(oferta)))
                                item_oferta_final.setTextAlignment(Qt.AlignCenter)
                                self.tabla_lote.setItem(4, columna, item_oferta_final)
                            break
                    break
    
    def llenar_formulario_totales(self):
        cantidad_de_lotes_totales = len(self.licitacion.lotes)
        cantidad_de_lotes_adjudicados = self.combinacion_ganadora.cantidad_lotes_ofertados()
        cantidad_de_empresas_totales = len(self.licitacion.empresas)
        cantidad_de_empresas_ganadoras = self.combinacion_ganadora.cantidad_empresas_ganadoras()
        valor_total_sin_descuento = self.combinacion_ganadora.valor()
        descuentos_realizados = ""
        for adicional in self.combinacion_ganadora.adicionales_aplicados():
            descuentos_realizados += "{0:.2f}%, ".format(abs(adicional.porcentaje))
        descuentos_realizados = descuentos_realizados[:-2].strip()
        if descuentos_realizados == "":
            descuentos_realizados = "Ninguno"
        valor_total_con_descuento = self.combinacion_ganadora.valor_con_adicional()

        etiqueta_cantidad_de_lotes_totales = QLabel("Cantidad de lotes totales:")
        etiqueta_cantidad_de_lotes_adjudicados = QLabel("Cantidad de lote adjudicados:")
        etiqueta_cantidad_de_empresas_totales = QLabel("Cantidad de empresas totales:")
        etiqueta_cantidad_de_empresas_ganadoras = QLabel("Cantidad de empresas ganadoras:")
        etiqueta_valor_total_sin_descuento = QLabel("Valor total sin descuento:")
        etiqueta_descuentos_realizados = QLabel("Descuentos realizados:")
        etiqueta_valor_total_con_descuento = QLabel("Valor total con descuento:")
        campo_cantidad_de_lotes_totales = QLabel(str(cantidad_de_lotes_totales))
        campo_cantidad_de_lotes_adjudicados = QLabel(str(cantidad_de_lotes_adjudicados))
        campo_cantidad_de_empresas_totales = QLabel(str(cantidad_de_empresas_totales))
        campo_cantidad_de_empresas_ganadoras = QLabel(str(cantidad_de_empresas_ganadoras))
        campo_valor_sin_descuento = QLabel("{0:,.3f}".format(valor_total_sin_descuento))
        campo_valor_con_descuento = QLabel("{0:,.3f}".format(valor_total_con_descuento))
        campo_descuentos_realizados = QLabel(str(descuentos_realizados))

        self.formulario_totales.addRow(etiqueta_cantidad_de_lotes_totales, campo_cantidad_de_lotes_totales)
        self.formulario_totales.addRow(etiqueta_cantidad_de_lotes_adjudicados, campo_cantidad_de_lotes_adjudicados)
        self.formulario_totales.addRow(etiqueta_cantidad_de_empresas_totales, campo_cantidad_de_empresas_totales)
        self.formulario_totales.addRow(etiqueta_cantidad_de_empresas_ganadoras, campo_cantidad_de_empresas_ganadoras)
        self.formulario_totales.addRow(etiqueta_valor_total_sin_descuento, campo_valor_sin_descuento)
        self.formulario_totales.addRow(etiqueta_descuentos_realizados, campo_descuentos_realizados)
        self.formulario_totales.addRow(etiqueta_valor_total_con_descuento, campo_valor_con_descuento)

    def resizeColumnsToMaximumContent(self):
        self.tabla_lote.resizeColumnsToContents()
        maximo = max([self.tabla_lote.columnWidth(i) for i in range(self.tabla_lote.columnCount())])
        for i in range(0, self.tabla_lote.columnCount()):
            self.tabla_lote.setColumnWidth(i, maximo)

    def tocado(self):
        self.tabla_lote.setRowCount(5)
        self.tabla_empresa.setRowCount(5)

    def eventFilter(self, source, event):
        if (event.type() == QEvent.KeyPress and
            event.matches(QKeySequence.Copy)):
            self.copySelection()
            return True
        return super().eventFilter(source, event)
    
    def copySelection(self):
        selection = self.tabla_lote.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = StringIO()
            writer(stream, delimiter='\t').writerows(table)
            QGuiApplication.clipboard().setText(stream.getvalue())


class WidgetCombinaciones(QWidget):
    def __init__(self, licitacion, con_descuento, parent=None):
        super().__init__(parent=parent)
        self.licitacion = licitacion
        self.caja_principal = QVBoxLayout()
        self.mostrar_descuentos = con_descuento
        self.tabla_combinaciones = QTableWidget(0, len(self.licitacion.lotes) + 4)

        self.mostrar_descuentos.setCheckState(Qt.Checked)
        self.mostrar_descuentos.stateChanged.connect(self.cambio_estado)
        self.llenar_tabla_combinaciones()
        self.tabla_combinaciones.verticalHeader().setVisible(False)
        self.tabla_combinaciones.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tabla_combinaciones.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tabla_combinaciones.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tabla_combinaciones.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tabla_combinaciones.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla_combinaciones.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.installEventFilter(self)
        self.resizeColumnsToMaximumContent()

        self.caja_principal.addWidget(self.tabla_combinaciones)
        self.setLayout(self.caja_principal)
    
    def llenar_tabla_combinaciones(self):
        titulos = []
        titulos.append("N°")
        titulos.append("")
        for lote in self.licitacion.lotes:
            titulos.append(lote.obtener_descripcion())
        titulos.append("Valor Final")
        titulos.append("Descuento")
        self.tabla_combinaciones.setHorizontalHeaderLabels(titulos)
        self.tabla_combinaciones.horizontalHeaderItem(self.tabla_combinaciones.columnCount()-1).setToolTip("Se aplicó algún descuento?")
        self.tabla_combinaciones.horizontalHeaderItem(self.tabla_combinaciones.columnCount()-2).setToolTip("Valor final con los descuentos aplicados")
        self.tabla_combinaciones.horizontalHeaderItem(1).setIcon(QIcon("iconos/toggle.png"))
        self.tabla_combinaciones.horizontalHeader().sectionClicked.connect(self.seccion_clickeada)
        self.tabla_combinaciones.cellClicked.connect(self.item_clickeado)
        for i, combinacion in enumerate(self.licitacion.combinaciones_reducidas):
            fila = self.tabla_combinaciones.rowCount()
            self.tabla_combinaciones.setRowCount(fila + 1)
            item_numero = QTableWidgetItem("{0}".format(i+1))
            self.tabla_combinaciones.setItem(fila, 0, item_numero)
            item_toggle = QTableWidgetItem(QIcon("iconos/toggle.png"), "")
            item_toggle.setTextAlignment(Qt.AlignCenter)
            item_toggle.setFlags(Qt.ItemIsEnabled)
            self.tabla_combinaciones.setItem(fila, 1, item_toggle)
            for j, lote in enumerate(self.licitacion.lotes):
                for posibilidad in combinacion.posibilidades:
                    if posibilidad.lote_contenido(lote):
                        oferta = posibilidad.oferta_de_lote(lote)
                        item_lote = QTableWidgetItemToggle(posibilidad, oferta, self.mostrar_descuentos)
                        item_lote.setTextAlignment(Qt.AlignCenter)
                        self.tabla_combinaciones.setItem(fila, j+2, item_lote)
                        break
            item_valor_final = QTableWidgetItem("{0:,.3f}".format(combinacion.valor_con_adicional()))
            item_valor_final.setTextAlignment(Qt.AlignCenter)
            self.tabla_combinaciones.setItem(fila, self.tabla_combinaciones.columnCount() - 2, item_valor_final)
            item_con_descuento = QTableWidgetItem()
            if combinacion.valor() != combinacion.valor_con_adicional():
                item_con_descuento.setCheckState(Qt.Checked)
            else:
                item_con_descuento.setCheckState(Qt.Unchecked)
            item_con_descuento.setTextAlignment(Qt.AlignCenter)
            item_con_descuento.setFlags(Qt.ItemIsEnabled)
            self.tabla_combinaciones.setItem(fila, self.tabla_combinaciones.columnCount() - 1, item_con_descuento)
    
    def item_clickeado(self, fila, columna):
        if columna == 1:
            self.toggle(fila)
        
    def seccion_clickeada(self, indice):
        if indice == 1:
            self.toggle_all()

    def toggle(self, fila):
        for i in range(2, self.tabla_combinaciones.columnCount() - 2):
            item_lote = self.tabla_combinaciones.item(fila, i)
            if item_lote != None:
                item_lote.toggle()
                
    def toggle_all(self):
        for fila in range(self.tabla_combinaciones.rowCount()):
            self.toggle(fila)
    
    def cambio_estado(self, estado):
        self.actualizar_todo()

    def actualizar_fila(self, fila):
        for columna in range(2, self.tabla_combinaciones.columnCount() - 2):
            item_lote = self.tabla_combinaciones.item(fila, columna)
            if item_lote != None:
                item_lote.actualizar_texto()

    def actualizar_todo(self):
        for fila in range(self.tabla_combinaciones.rowCount()):
            self.actualizar_fila(fila)

    def resizeColumnsToMaximumContent(self):
        self.tabla_combinaciones.resizeColumnsToContents()
        maximo = max([self.tabla_combinaciones.columnWidth(i) for i in range(self.tabla_combinaciones.columnCount())])
        for i in range(2, self.tabla_combinaciones.columnCount()):
            self.tabla_combinaciones.setColumnWidth(i, maximo + 10)
        self.tabla_combinaciones.setColumnWidth(1, 22)
        self.tabla_combinaciones.setColumnWidth(self.tabla_combinaciones.columnCount() - 1, 80)
        self.tabla_combinaciones.updateGeometry()
        self.tabla_combinaciones.adjustSize()
        self.adjustSize()
    
    def eventFilter(self, source, event):
        if (event.type() == QEvent.KeyPress and
            event.matches(QKeySequence.Copy)):
            self.copySelection()
            return True
        return super().eventFilter(source, event)
    
    def copySelection(self):
        selection = self.tabla_combinaciones.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = StringIO()
            writer(stream, delimiter='\t').writerows(table)
            QGuiApplication.clipboard().setText(stream.getvalue())
    
class QTableWidgetItemToggle(QTableWidgetItem):
    def __init__(self, posibilidad, oferta, item_con_descuento):
        super().__init__()
        self.oferta = oferta
        self.posibilidad = posibilidad
        self.adicional = posibilidad.adicional
        self.muestra_valor = False
        self.item_con_descuento = item_con_descuento
        self.actualizar_texto()
    
    def toggle(self):
        self.muestra_valor = not self.muestra_valor
        self.actualizar_texto()
    
    def actualizar_texto(self):
        if self.muestra_valor:
            if self.adicional.es_nulo():
                if self.item_con_descuento.isChecked():
                    self.setText("{0:,.3f}  (0.00%)".format(self.oferta.valor))
                else:
                    self.setText("{0:,.3f}".format(self.oferta.valor))
            else:
                if self.item_con_descuento.isChecked():
                    if self.adicional.conjunto_ofertas.oferta_contenida(self.oferta):
                        self.setText("{0:,.3f}  ({1:.2f}%)".format(self.oferta.valor + self.posibilidad.adicional.valor_en_oferta(self.oferta), abs(self.adicional.porcentaje)))
                    else:
                        self.setText("{0:,.3f}  (0.00%)".format(self.oferta.valor))
                else:
                    if self.adicional.conjunto_ofertas.oferta_contenida(self.oferta):
                        self.setText("{0:,.3f}".format(self.oferta.valor + self.posibilidad.adicional.valor_en_oferta(self.oferta)))
                    else:
                        self.setText("{0:,.3f}".format(self.oferta.valor))
                        
        else:
            self.setText(self.oferta.empresa.nombre)
    


class CombinacionGanadora(QWidgetPrincipal):
    def __init__(self, licitacion, parent=None):
        super().__init__(licitacion, "Combinación Ganadora", WidgetCombinacionGanadora(licitacion), parent=parent)

class Combinaciones(QWidgetPrincipal):
    def __init__(self, licitacion, parent=None):
        marco = QFrame()
        caja = QHBoxLayout()
        self.mostrar_descuentos = QCheckBox("Mostrar Descuentos")
        widget_combinaciones = WidgetCombinaciones(licitacion, self.mostrar_descuentos)
        self.boton_ajustar_tamanio = QPushButton(QIcon("iconos/adjust_size.png"), "")
        self.boton_ajustar_tamanio.setToolTip("Ajustar tamaño de la grilla")
        self.boton_ajustar_tamanio.clicked.connect(widget_combinaciones.resizeColumnsToMaximumContent)
        super().__init__(licitacion, "Combinaciones", widget_combinaciones, parent=parent)
        caja.addWidget(self.mostrar_descuentos)
        caja.addStretch(1)
        caja.addWidget(self.boton_ajustar_tamanio)
        marco.setLayout(caja)
        self.caja_general.insertWidget(0, marco)


if __name__ == "__main__":
    app = QApplication(sysargv)
    #a = Resultados()
    #a.show()
    #c = QWidgetPrincipal(None, "HOLA")
    #c.show()
    d = CombinacionGanadora(Licitador("Hola Mundo"))
    d.show()
    sysexit(app.exec_())
    