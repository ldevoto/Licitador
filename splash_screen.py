from sys import argv as sysargv, exit as sysexit
from time import sleep
from threading import Thread
from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QApplication, QPushButton, QHBoxLayout, QSplashScreen)
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QRegExpValidator, QKeySequence, QPixmap
from PyQt5.QtCore import Qt, QModelIndex, QMimeData

class SplashScreen(QSplashScreen):
    def __init__(self, parent=None):
        self.imagen = QPixmap("splash_screen.png")
        super().__init__(pixmap=self.imagen)
        self.show()