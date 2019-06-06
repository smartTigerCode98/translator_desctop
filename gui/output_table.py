from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(1284, 617)
        Form.setStyleSheet("background-color: rgb(19, 84, 41)")

        self.pushButton_1 = QtWidgets.QPushButton(Form)
        self.pushButton_1.setGeometry(QtCore.QRect(280, 40, 191, 41))
        self.pushButton_1.setStyleSheet("background-color: grey")
        self.pushButton_1.setObjectName("pushButton_1")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(50, 110, 1181, 461))
        self.textEdit.setStyleSheet("background-color: white")
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(True)
        self.textEdit.setFont(QtGui.QFont("Consolas", 10))
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textEdit.setLineWrapColumnOrWidth(400)
        self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 40, 191, 41))
        self.pushButton_2.setStyleSheet("background-color: grey")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(510, 40, 201, 41))
        self.pushButton_3.setStyleSheet("background-color: grey")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(750, 40, 181, 41))
        self.pushButton_4.setStyleSheet("background-color: grey")
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(960, 40, 130, 41))
        self.pushButton_5.setStyleSheet("background-color: grey")
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(1105, 40, 130, 41))
        self.pushButton_6.setStyleSheet("background-color: grey")
        self.pushButton_6.setObjectName("pushButton_5")


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_1.setText(_translate("Form", "Lexems"))
        self.pushButton_2.setText(_translate("Form", "Identifiers"))
        self.pushButton_3.setText(_translate("Form", "Constants"))
        self.pushButton_4.setText(_translate("Form", "Labels"))
        self.pushButton_5.setText(_translate("Form", "Grammar"))
        self.pushButton_6.setText(_translate("Form", "Parse table"))






