from sys import argv as sysargv, exit as sysexit
from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, 
                             QStyle, QTableWidget, QGridLayout, QLabel, QVBoxLayout, QHeaderView, 
                             QAbstractItemView, QTableWidgetItem, QAbstractScrollArea, QFrame, 
                             QMainWindow, QWidget, QLayout, QMessageBox, QGroupBox, QShortcut)
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator, QKeySequence
from PyQt5.QtCore import Qt, QModelIndex, QMimeData
from clases import Asociacion, Empresa, Contrato, Licitador
from widgets_ocultos import Estados
from dialogo_empresas import DialogoEmpresas
from dialogo_lotes import DialogoLotes
from dialogo_ofertas import DialogoOfertas
from dialogo_adicionales import DialogoAdicionales


class PantallaPrincipal(QDialog):
    A_CREAR = 1
    A_CARGAR = 2
    A_SALIR = 0
    A_INDEFINIDO = 99

    def __init__(self):
        super().__init__()
        self.dibujar_IU()
        self.accion = PantallaPrincipal.A_INDEFINIDO

    def dibujar_IU(self):
        self.setWindowTitle("LicitaSoft")

        boton_crear_nueva_licitacion = QPushButton("Crear nueva licitación")
        boton_cargar_licitacion_preexistente = QPushButton("Cargar licitación preexistente")
        boton_salir = QPushButton("Salir")

        boton_crear_nueva_licitacion.setContentsMargins(10, 10, 10, 10)
        boton_crear_nueva_licitacion.clicked.connect(self.crear_nueva_licitacion)
        boton_cargar_licitacion_preexistente.setContentsMargins(10, 10, 10, 10)
        boton_cargar_licitacion_preexistente.clicked.connect(self.cargar_licitacion_preexistente)
        boton_salir.setContentsMargins(10, 10, 10, 10)
        boton_salir.clicked.connect(self.close)

        caja = QVBoxLayout()
        caja.setContentsMargins(15, 15, 15, 15)
        caja.addStretch(1)
        caja.addWidget(boton_crear_nueva_licitacion)
        caja.addWidget(boton_cargar_licitacion_preexistente)
        caja.addStretch(3)
        caja.addWidget(boton_salir)
        caja.addStretch(1)
        marco = QGroupBox()
        marco.setLayout(caja)
        caja2 = QVBoxLayout()
        caja2.addWidget(marco)
        self.setLayout(caja2)

        self.resize(self.sizeHint() * 2)
    
    def crear_nueva_licitacion(self):
        self.accion = PantallaPrincipal.A_CREAR
        self.accept()
    
    def cargar_licitacion_preexistente(self):
        self.accion = PantallaPrincipal.A_CARGAR
        self.accept()
    
    def obtener_accion(self):
        return self.accion

    #Es para evitar que se cierre el Dilog con la tecla ESC
    def reject(self):
        self.close()
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Salir', "Está a punto de salir.\nEstá seguro que desea salir?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.accion = PantallaPrincipal.A_SALIR
            event.accept()
        else:
            event.ignore()


def obtener_empresas():
    dialogo_empresas = DialogoEmpresas()
    while dialogo_empresas.exec() == QDialog.Accepted:
        empresas = dialogo_empresas.obtener_empresas()
        print(empresas.count())
        if dialogo_empresas.obtener_estado() == Estados.E_CONTINUAR:
            return empresas
    exit()


def crear_objeto_licitador(lotes, empresas, ofertas, adicionales):
    licitador = Licitador()
    for oferta in ofertas:
        oferta.empresa.conjunto_ofertas.agregar_oferta(oferta)
    for adicional in adicionales:
        adicional.empresa.agregar_adicional(adicional)
    for lote in lotes:
        licitador.agregar_lote(lote)
    for empresa in empresas:
        licitador.agregar_empresa(empresa)
    return licitador

def crear_nueva_licitacion():
    lotes = []
    empresas = []
    ofertas = []
    adicionales = []
    carga_terminada = False
    salir = False
    falta_cargar_lotes = True
    falta_cargar_empresas = False
    falta_cargar_ofertas = False
    falta_cargar_adicionales = False
    while not carga_terminada and not salir:
        if (falta_cargar_lotes):
            dialogo_lotes = DialogoLotes(lotes=lotes)
            if dialogo_lotes.exec() == QDialog.Accepted:
                lotes = dialogo_lotes.obtener_lotes()
                if dialogo_lotes.obtener_estado() == Estados.E_CONTINUAR:
                    falta_cargar_lotes = False
                    falta_cargar_empresas = True
                    falta_cargar_ofertas = False
                    falta_cargar_adicionales = False
                    salir = False
                else:
                    falta_cargar_lotes =True 
                    falta_cargar_empresas = False
                    falta_cargar_ofertas = False
                    falta_cargar_adicionales = False
                    salir = True
            else:
                falta_cargar_lotes = False
                falta_cargar_empresas = False
                falta_cargar_ofertas = False
                falta_cargar_adicionales = False
                salir = True
        if (falta_cargar_empresas):
            dialogo_empresas = DialogoEmpresas(empresas=empresas)
            if dialogo_empresas.exec() == QDialog.Accepted:
                empresas = dialogo_empresas.obtener_empresas()
                if dialogo_empresas.obtener_estado() == Estados.E_CONTINUAR:
                    falta_cargar_lotes = False
                    falta_cargar_empresas = False
                    falta_cargar_ofertas = True
                    falta_cargar_adicionales = False
                    salir = False
                else:
                    falta_cargar_lotes = True
                    falta_cargar_empresas = False
                    falta_cargar_ofertas = False
                    falta_cargar_adicionales = False
                    salir = False
            else:
                falta_cargar_lotes = False
                falta_cargar_empresas = False
                falta_cargar_ofertas = False
                falta_cargar_adicionales = False
                salir = True
        if (falta_cargar_ofertas):
            dialogo_ofertas = DialogoOfertas(ofertas=ofertas, lotes=lotes, empresas=empresas)
            if dialogo_ofertas.exec() == QDialog.Accepted:
                ofertas = dialogo_ofertas.obtener_ofertas()
                if dialogo_ofertas.obtener_estado() == Estados.E_CONTINUAR:
                    falta_cargar_lotes = False
                    falta_cargar_empresas = False
                    falta_cargar_ofertas = False
                    falta_cargar_adicionales = True
                    salir = False
                else:
                    falta_cargar_lotes = False
                    falta_cargar_empresas = True
                    falta_cargar_ofertas = False
                    falta_cargar_adicionales = False
                    salir = False
            else:
                falta_cargar_lotes = False
                falta_cargar_empresas = False
                falta_cargar_ofertas = False
                falta_cargar_adicionales = False
                salir = True
        if (falta_cargar_adicionales):
            dialogo_adicionales = DialogoAdicionales(lotes=lotes, empresas=empresas, ofertas=ofertas, adicionales=adicionales)
            if dialogo_adicionales.exec() == QDialog.Accepted:
                adicionales = dialogo_adicionales.obtener_adicionales()
                if dialogo_adicionales.obtener_estado() == Estados.E_CONTINUAR:
                    falta_cargar_lotes = False
                    falta_cargar_empresas = False
                    falta_cargar_ofertas = False
                    falta_cargar_adicionales = False
                    salir = False
                else:
                    falta_cargar_lotes = False
                    falta_cargar_empresas = False
                    falta_cargar_ofertas = True
                    falta_cargar_adicionales = False
                    salir = False
            else:
                falta_cargar_lotes = False
                falta_cargar_empresas = False
                falta_cargar_ofertas = False
                falta_cargar_adicionales = False
                salir = True
            if (falta_cargar_lotes or falta_cargar_empresas or falta_cargar_ofertas or falta_cargar_adicionales):
                carga_terminada = False
            else:
                carga_terminada = True
    licitador = None
    if salir:
        if falta_cargar_lotes:
            print("Quiso salir al menu principal")
        else:
            print("Quiso salir!")
            exit()
    else:
        print("Esta todo listo para empezar la licitación!")
        licitador = crear_objeto_licitador(lotes, empresas, ofertas, adicionales)
    return licitador



def cargar_licitacion_preexistente():
    pass


if __name__ == '__main__':
    app = QApplication(sysargv)
    pantalla_principal = PantallaPrincipal()
    while pantalla_principal.exec() == QDialog.Accepted:
        accion = pantalla_principal.obtener_accion()
        if accion == PantallaPrincipal.A_CREAR:
            print("Crear")
            licitador = crear_nueva_licitacion()
            '''
            for empresa in licitador.empresas:
                print()
                print("-----------Empresa---------------")
                print(empresa.id)
                print(empresa.nombre)
                print("Ofertas:")
                for oferta in empresa.conjunto_ofertas.ofertas:
                    print(oferta.lote.id)
                    print(oferta.valor)
                print("Adicionales:")
                for adicional in empresa.adicionales:
                    if type(adicional).__name__ != "AdicionalNulo":
                        print(adicional.porcentaje)
                        print("Conjunto ofertas:")
                        for oferta in adicional.conjunto_ofertas.ofertas:
                            print(oferta.lote.id)
            print("-------------Lotes----------------")
            for lote in licitador.lotes:
                print(lote.id)
                print(lote.descripcion)
            '''
            dialogo_cargando = DialogoCargando()
            licitador.iniciar_licitacion()
            ganador = licitador.combinacion_ganadora()
            print("------------GANADORRRRR--------------")
            print(ganador.valor_con_adicional())
            for posibilidad in ganador.posibilidades:
                print(posibilidad.empresa.nombre)
                for oferta in posibilidad.conjunto_ofertas.ofertas:
                    print(oferta.lote.id)
                    print(oferta.valor)
        elif accion == PantallaPrincipal.A_CARGAR:
            print("Cargar")
            cargar_licitacion_preexistente()
            pass
        else:
            pass
        pantalla_principal = PantallaPrincipal()
    print("Adios!")
    #sysexit(app.exec_())
    #print("hola mundo!")
