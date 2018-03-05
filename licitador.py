import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt

class Principal(QWidget):
    def __init__(self):
        super().__init__()
        self.iniciar_componente()

    def iniciar_componente(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setGeometry(300, 300, 400, 400)
        self.centrar()
        self.setWindowTitle("Licitador LePibet V1.0")

        boton_abrir_nueva_licitacion = QPushButton("Abrir nueva Licitación")
        boton_abrir_nueva_licitacion.setToolTip("Clickee en esta opción si desea abrir/crear una nueva licitación")
        boton_abrir_nueva_licitacion.resize(boton_abrir_nueva_licitacion.sizeHint())
        boton_abrir_nueva_licitacion.clicked.connect(self.abrir_nueva_licitacion)
        boton_cargar_licitacion_existente = QPushButton("Cargar una Licitacion Preexistente")
        boton_cargar_licitacion_existente.setToolTip("Clickee en esta opción si desea cargar una licitación realizada con anterioridad")
        boton_cargar_licitacion_existente.resize(boton_cargar_licitacion_existente.sizeHint())
        boton_cargar_licitacion_existente.clicked.connect(self.cargar_licitacion_existente)
        boton_salir = QPushButton("Salir")
        boton_salir.setToolTip("Clickee en esta opción si desea salir")
        boton_salir.resize(boton_salir.sizeHint())
        boton_salir.clicked.connect(self.salir)
        caja_vertical = QVBoxLayout()
        caja_vertical.addStretch(1)
        caja_vertical.addWidget(boton_abrir_nueva_licitacion)
        caja_vertical.addWidget(boton_cargar_licitacion_existente)
        caja_vertical.addStretch(2)
        caja_vertical.addWidget(boton_salir)
        caja_vertical.addStretch(1)
        self.setLayout(caja_vertical)

        self.show()
    
    def abrir_nueva_licitacion(self):
        print("Nueva licitacion abierta!")
        self.hide()
        lotes = PantallaLotes()
        lotes.exec_()
        self.show()
        pass

    def cargar_licitacion_existente(self):
        print("Carga de nueva licitacion")
        pass

    def salir(self):
        self.closeEvent()
        pass
    
    def centrar(self):
        frame = self.frameGeometry()
        centro = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(centro)
        self.move(frame.topLeft())
    
    def closeEvent(self, event):
        #reply = QMessageBox.question(self, 'Salir', "Está a punto de salir.\nEstá seguro que desea salir?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        #if reply == QMessageBox.Yes:
        event.accept()
        #else:
        #    event.ignore()
        
    

class PantallaLotes(QWidget):
    def __init__(self):
        super().__init__()
        self.iniciar_componente()
    
    def iniciar_componente(self):
        caja_vertical1 = QVBoxLayout()
        caja_horizontal1 = QHBoxLayout()
        titulo = QLabel("LOTES")
        caja_horizontal1.addStretch(1)
        caja_horizontal1.addWidget(titulo)
        caja_horizontal1.addStretch(1)
        caja_vertical1.addLayout(caja_horizontal1)

        caja_horizontal2 = QHBoxLayout()
        grilla = QGridLayout()
        tabla_lotes = QTableWidget() 
        tabla_lotes.setColumnCount(5)  
        tabla_lotes.setRowCount(1)
        tabla_lotes.setHorizontalHeaderLabels(["Id", "Descripcion", "Facturacion Media Anual", "Recursos Financieros", "Experiencia"])
        tabla_lotes.horizontalHeaderItem(0).setToolTip("Id del lote")
        tabla_lotes.horizontalHeaderItem(1).setToolTip("Breve descripción o nombre del lote")
        tabla_lotes.horizontalHeaderItem(2).setToolTip("Facturación media anual requerida por el lote")
        tabla_lotes.horizontalHeaderItem(3).setToolTip("Recursos financieros requeridos por el lote")
        tabla_lotes.horizontalHeaderItem(4).setToolTip("Experiencia requerida por el lote")
    
        # Set the alignment to the headers
        tabla_lotes.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        tabla_lotes.horizontalHeaderItem(1).setTextAlignment(Qt.AlignLeft)
        tabla_lotes.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)
        tabla_lotes.horizontalHeaderItem(3).setTextAlignment(Qt.AlignRight)
        tabla_lotes.horizontalHeaderItem(4).setTextAlignment(Qt.AlignRight)
    
        # Fill the first line
        #table.setItem(0, 0, QTableWidgetItem("Text in column 1"))
        #table.setItem(0, 1, QTableWidgetItem("Text in column 2"))
        #table.setItem(0, 2, QTableWidgetItem("Text in column 3"))
    
        # Do the resize of the columns by content
        tabla_lotes.resizeColumnsToContents()
        #tabla_lotes.resize(tabla_lotes.sizeHint())
    
        grilla.addWidget(tabla_lotes, 0, 0)

        #caja_horizontal2.addWidget(tabla_lotes)
        caja_horizontal2.addLayout(grilla)
        caja_vertical2 = QVBoxLayout()
        boton_agregar_lote = QPushButton(QIcon("png/plus.png"), "")
        boton_eliminar_lote = QPushButton(QIcon("png/minus.png"), "")
        caja_vertical2.addStretch(1)
        caja_vertical2.addWidget(boton_agregar_lote)
        caja_vertical2.addWidget(boton_eliminar_lote)
        caja_vertical2.addStretch(5)
        caja_horizontal2.addLayout(caja_vertical2)
        caja_vertical1.addLayout(caja_horizontal2)

        caja_horizontal3 = QHBoxLayout()
        boton_regresar = QPushButton(QIcon("png/left-arrows.png"), "")
        boton_continuar = QPushButton(QIcon("png/right-arrows.png"), "")
        caja_horizontal3.addWidget(boton_regresar)
        caja_horizontal3.addStretch(1)
        caja_horizontal3.addWidget(boton_continuar)
        caja_vertical1.addLayout(caja_horizontal3)
        self.setLayout(caja_vertical1)
        self.resize(self.sizeHint())
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Principal()
    sys.exit(app.exec_())