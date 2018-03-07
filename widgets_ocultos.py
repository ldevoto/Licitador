from PyQt5.QtWidgets import QTableWidgetItem

class QTableWidgetItemEmpresa(QTableWidgetItem):
    def __init__(self, empresa):
        super().__init__()
        self.empresa = empresa

class QTableWidgetItemLote(QTableWidgetItem):
    def __init__(self, lote):
        super().__init__()
        self.lote = lote
    