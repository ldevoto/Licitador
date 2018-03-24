from sys import argv as sysargv, exit as sysexit
from time import sleep
from threading import Thread
from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, 
                             QStyle, QTableWidget, QGridLayout, QLabel, QVBoxLayout, QHeaderView, 
                             QAbstractItemView, QTableWidgetItem, QAbstractScrollArea, QFrame, 
                             QMainWindow, QWidget, QLayout, QMessageBox, QGroupBox, QShortcut, QStyleFactory)
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator, QKeySequence, QFont
from PyQt5.QtCore import Qt, QModelIndex, QMimeData
from clases import Asociacion, Empresa, Contrato, Combinacion, Licitador
from widgets_ocultos import Estados, MensajeSalida
from dialogo_empresas import DialogoEmpresas
from dialogo_lotes import DialogoLotes
from dialogo_ofertas import DialogoOfertas
from dialogo_adicionales import DialogoAdicionales
from dialogo_cargando import DialogoCargando
from dialogo_datos import DialogoDatos, DialogoCargaDatos
from dialogo_resultados import DialogoResultados
from persistencia import obtener_licitaciones, licitacion_existente, eliminar_licitacion
from splash_screen import SplashScreen


class PantallaPrincipal(QDialog):
    A_CREAR = 1
    A_CARGAR = 2
    A_ELIMINAR = 3
    A_SALIR = 0
    A_INDEFINIDO = 99

    def __init__(self):
        super().__init__()
        self.dibujar_IU()
        self.accion = PantallaPrincipal.A_INDEFINIDO
        self.nombre_licitacion = ""

    def dibujar_IU(self):
        self.setWindowTitle("LicitaSoft")

        boton_crear_nueva_licitacion = QPushButton("Crear nueva licitación")
        boton_cargar_licitacion_preexistente = QPushButton("Cargar licitación")
        boton_eliminar_licitacion = QPushButton("Eliminar licitación")
        boton_salir = QPushButton("Salir")

        boton_crear_nueva_licitacion.setContentsMargins(10, 10, 10, 10)
        boton_crear_nueva_licitacion.clicked.connect(self.crear_nueva_licitacion)
        boton_cargar_licitacion_preexistente.setContentsMargins(10, 10, 10, 10)
        boton_cargar_licitacion_preexistente.clicked.connect(self.cargar_licitacion_preexistente)
        boton_eliminar_licitacion.setContentsMargins(10, 10, 10, 10)
        boton_eliminar_licitacion.clicked.connect(self.eliminar_licitacion)
        boton_salir.setContentsMargins(10, 10, 10, 10)
        boton_salir.clicked.connect(self.close)

        caja = QVBoxLayout()
        caja.setContentsMargins(15, 15, 15, 15)
        caja.addStretch(1)
        caja.addWidget(boton_crear_nueva_licitacion)
        caja.addWidget(boton_cargar_licitacion_preexistente)
        caja.addWidget(boton_eliminar_licitacion)
        caja.addStretch(3)
        caja.addWidget(boton_salir)
        caja.addStretch(1)
        marco = QGroupBox()
        marco.setLayout(caja)
        caja2 = QVBoxLayout()
        caja2.addWidget(marco)
        self.setLayout(caja2)

        #self.resize(self.sizeHint())
        self.setFixedSize(300, 300)
    
    def crear_nueva_licitacion(self):
        dialogo_datos = DialogoDatos(self)
        if dialogo_datos.exec() == QDialog.Accepted:
            self.nombre_licitacion = dialogo_datos.obtener_nombre_licitacion()
            self.accion = PantallaPrincipal.A_CREAR
            self.accept()
    
    def cargar_licitacion_preexistente(self):
        licitaciones = obtener_licitaciones("Licitaciones.db")
        dialogo_datos = DialogoCargaDatos(self, licitaciones=licitaciones)
        if dialogo_datos.exec() == QDialog.Accepted:
            print(dialogo_datos.obtener_nombre_licitacion())
            self.nombre_licitacion = dialogo_datos.obtener_nombre_licitacion()
            self.accion = PantallaPrincipal.A_CARGAR
            self.accept()
        
    def eliminar_licitacion(self):
        licitaciones = obtener_licitaciones("Licitaciones.db")
        dialogo_datos = DialogoCargaDatos(self, licitaciones=licitaciones)
        if dialogo_datos.exec() == QDialog.Accepted:
            mensaje = QMessageBox(self)
            mensaje.setWindowTitle("Eliminar")
            mensaje.setText('Está a punto de eliminar de forma permanente la licitación "{0}"'.format(dialogo_datos.obtener_nombre_licitacion()))
            mensaje.setInformativeText("Está seguro que desea continuar?")
            boton_si = mensaje.addButton("Si", QMessageBox.YesRole)
            boton_no = mensaje.addButton("No", QMessageBox.NoRole)
            mensaje.setDefaultButton(boton_no)
            mensaje.exec()
            if mensaje.clickedButton() == boton_si:
                print(dialogo_datos.obtener_nombre_licitacion())
                self.nombre_licitacion = dialogo_datos.obtener_nombre_licitacion()
                self.accion = PantallaPrincipal.A_ELIMINAR
                self.accept()
    
    def obtener_nombre_licitacion(self):
        return self.nombre_licitacion
    
    def obtener_accion(self):
        return self.accion

    #Es para evitar que se cierre el Dilog con la tecla ESC
    def reject(self):
        self.close()
    
    def closeEvent(self, event):
        mensaje = MensajeSalida(self)
        mensaje.exec()
        if mensaje.clickedButton() == mensaje.boton_si:
            self.accion = PantallaPrincipal.A_SALIR
            event.accept()
        else:
            event.ignore()
    

class ThreadLicitador(Thread):
    def __init__(self, licitador, dialogo):
        super().__init__()
        self.dialogo = dialogo
        self.licitador = licitador
    
    def run(self):
        #sleep(0.2)
        self.dialogo.setear_texto("Generando Posibilidades de oferta para cada empresa...")
        self.licitador.calcular_posibilidades_empresas()
        sleep(3)
        self.dialogo.setear_texto("Calculando combinaciones posibles...")
        self.licitador.calcular_combinaciones()
        sleep(3)
        self.dialogo.setear_texto("Reduciendo el número de combinaciones...")
        self.licitador.reducir_combinaciones()
        sleep(3)
        self.dialogo.setear_texto("Ordenando combinaciones según valor...")
        self.licitador.ordenar_combinaciones()
        sleep(3)
        self.dialogo.mostrar_boton_confirmar()



def crear_objeto_licitador(nombre_licitacion, lotes, empresas, ofertas, adicionales):
    licitador = Licitador(nombre_licitacion)
    for lote in lotes:
        licitador.agregar_lote(lote)
    for empresa in empresas:
        licitador.agregar_empresa(empresa)
    return licitador


def datos_licitacion(licitacion, lotes, empresas, ofertas, adicionales):
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
        licitador = crear_objeto_licitador(licitacion.nombre, lotes, empresas, ofertas, adicionales)
    return licitador

def crear_nueva_licitacion(licitacion):
    lotes = []
    empresas = []
    ofertas = []
    adicionales = []
    licitacion.lotes = lotes
    licitacion.empresas = empresas

    return datos_licitacion(licitacion, lotes, empresas, ofertas, adicionales)


def cargar_licitacion_preexistente(licitacion):
    licitacion.cargar_licitacion()
    lotes = licitacion.lotes
    empresas = licitacion.empresas
    ofertas = []
    adicionales = []
    for empresa in licitacion.empresas:
        for oferta in empresa.conjunto_ofertas.ofertas:
            ofertas.append(oferta)
        for adicional in empresa.adicionales:
            if not adicional.es_nulo():
                adicionales.append(adicional)
    
    return datos_licitacion(licitacion, lotes, empresas, ofertas, adicionales)

if __name__ == '__main__':
    app = QApplication(sysargv)
    #app.setAttribute(Qt.AA_NativeWindows, True)
    #print(QStyleFactory.keys())
    app.setStyle(QStyleFactory().create("Fusion"))
    fuente = QFont()
    fuente.setFamily("Cantarell")
    app.setFont(fuente)
    pantalla_principal = PantallaPrincipal()
    splash = SplashScreen()
    splash.finish(pantalla_principal)
    while pantalla_principal.exec() == QDialog.Accepted:
        accion = pantalla_principal.obtener_accion()
        if accion == PantallaPrincipal.A_CREAR:
            print("Crear")
            licitador = crear_nueva_licitacion(Licitador(pantalla_principal.obtener_nombre_licitacion()))
            Combinacion.maxima = 0
            if licitador == None:
                continue
            else:
                licitador.guardar_licitacion()
            dialogo_cargando = DialogoCargando()
            thread = ThreadLicitador(licitador, dialogo_cargando)
            thread.start()
            dialogo_cargando.exec()
            ganador = licitador.combinacion_ganadora()
            print("------------GANADORRRRR--------------")
            print(ganador.to_json())
            dialogo_resultado = DialogoResultados(licitador)
            dialogo_resultado.exec()
        elif accion == PantallaPrincipal.A_CARGAR:
            print("Cargar")
            licitador = cargar_licitacion_preexistente(Licitador(pantalla_principal.obtener_nombre_licitacion()))
            Combinacion.maxima = 0
            if licitador == None:
                continue
            else:
                mensaje = QMessageBox()
                mensaje.setWindowTitle("Opciones de Guardado")
                mensaje.setText("Seleccione la opción de guardado que desee:")
                boton_sobreescribir = mensaje.addButton("Sobreescribir", QMessageBox.YesRole)
                boton_guardar = mensaje.addButton("Guardar con otro nombre", QMessageBox.NoRole)
                boton_cancel = mensaje.addButton("No Guardar", QMessageBox.RejectRole)
                mensaje.setDefaultButton(boton_cancel)
                mensaje.exec()
                if mensaje.clickedButton() == boton_sobreescribir:
                    print("Sobreescribir")
                    licitador.sobreescribir_licitacion()
                elif mensaje.clickedButton() == boton_guardar:
                    print("Guardar")
                    dialogo_datos = DialogoDatos()
                    while dialogo_datos.exec() != QDialog.Accepted:
                        dialogo_datos = DialogoDatos()
                    licitador.nombre = dialogo_datos.obtener_nombre_licitacion()
                    licitador.guardar_licitacion()
                else:
                    print("Continuar sin guardar")
            dialogo_cargando = DialogoCargando()
            thread = ThreadLicitador(licitador, dialogo_cargando)
            thread.start()
            dialogo_cargando.exec()
            ganador = licitador.combinacion_ganadora()
            print("------------GANADORRRRR--------------")
            print(ganador.to_json())
            dialogo_resultado = DialogoResultados(licitador)
            dialogo_resultado.exec()
        elif accion == PantallaPrincipal.A_ELIMINAR:
            print("eliminar")
            eliminar_licitacion("Licitaciones.db", Licitador(pantalla_principal.obtener_nombre_licitacion()))
            mensaje = QMessageBox()
            mensaje.setWindowTitle("Eliminar")
            mensaje.setText('Se ha eliminado la licitación "{0}" correctamente'.format(pantalla_principal.obtener_nombre_licitacion()))
            mensaje.exec()
        else:
            pass
        pantalla_principal = PantallaPrincipal()
    print("Adios!")
