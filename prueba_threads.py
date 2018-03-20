from threading import *
from time import sleep
from sys import argv as sysargv, exit as sysexit
from dialogo_cargando import DialogoCargando
from PyQt5.QtWidgets import QApplication

class miThread(Thread):
    def __init__(self, nombre, tiempo, objeto):
        super().__init__(name=nombre)
        self.tiempo = tiempo
        self.objeto = objeto
    
    def run(self):
        sleep(self.tiempo)
        print("hola soy {}".format(self.name))
        self.objeto.setear_texto("Me muerooooo")
        sleep(self.tiempo)
        self.objeto.close()


app = QApplication(sysargv)
dialogo = DialogoCargando()
nuevo_thread = miThread("Jose", 1, dialogo)
nuevo_thread.start()
sleep(3)
dialogo.setear_texto("Me muero yooooo")
sleep(1)
dialogo.close()
dialogo.exec()
#sysexit(app.exec_())
