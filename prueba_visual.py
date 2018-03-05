from sys import argv as sysargv, exit as sysexit
from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, QStyle, QTableWidget, QGridLayout, QLabel, QVBoxLayout, QHeaderView, QAbstractItemView, QTableWidgetItem, QAbstractScrollArea, QFrame
from dialogo_lote import DialogoLote
from dialogo_empresa import DialogoEmpresa
from dialogo_asociacion import DialogoAsociacion
from clases import Lote, Contrato, Empresa, Asociacion

if __name__ == '__main__':
    app = QApplication(sysargv)
    ex = DialogoLote()
    while ex.exec() == QDialog.Accepted:
        lote = ex.obtener_lote()
        print(lote)
        ex = DialogoLote()
    lote = Lote(2, 3000.943, 30000.23, 3000.11)
    lote.descripcion = "Soy el lote 2"
    ex = DialogoLote(lote=lote)
    while ex.exec() == QDialog.Accepted:
        lote = ex.obtener_lote()
        print(lote.id)
        print(lote.descripcion)
        ex = DialogoLote(lote=lote)
    ex = DialogoEmpresa()
    while ex.exec() == QDialog.Accepted:
        empresa = ex.obtener_empresa()
        print(empresa)
        ex = DialogoEmpresa()
    empresa = Empresa(2, "Empresa 2 del pebet", 34234.234, 2343.234, [Contrato(2017, 25365.25), Contrato(2018, 2323.25)])
    ex = DialogoEmpresa(empresa=empresa)
    if ex.exec() == QDialog.Accepted:
        empresa = ex.obtener_empresa()
        print(empresa.id)
        print(empresa.nombre)
        ex = DialogoEmpresa(empresa=empresa)
    ex = DialogoAsociacion()
    while ex.exec() == QDialog.Accepted:
        asociacion = ex.obtener_asociacion()
        print(asociacion)
        ex = DialogoAsociacion()
    asociacion = Asociacion(2, "Asociacion WTF 2", [Empresa(1, "Empresa 1", 2000.03, 3000.02, [Contrato(2017, 1235.25)]), Empresa(3, "Empresa 3", 11111.11, 222222.22, [Contrato(2018, 3333.33), Contrato(2019, 44444.444)])])
    ex = DialogoAsociacion(asociacion=asociacion)
    if ex.exec() == QDialog.Accepted:
        asociacion = ex.obtener_asociacion()
        print(asociacion.id)
        print(asociacion.nombre)
        print(asociacion.socios)
        print(asociacion.facturacion_media_anual())
        print(asociacion.recursos_financieros())
        ex = DialogoAsociacion(asociacion=asociacion)

