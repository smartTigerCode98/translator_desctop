# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ouput_table.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(984, 617)
        Form.setStyleSheet("background-color: rgb(19, 84, 41)")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(280, 40, 191, 41))
        self.pushButton.setStyleSheet("background-color: rgb(0, 116, 0)")
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(50, 110, 881, 461))
        self.textEdit.setStyleSheet("background-color: white")
        self.textEdit.setObjectName("textEdit")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 40, 191, 41))
        self.pushButton_2.setStyleSheet("background-color: rgb(0, 116, 0)")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(510, 40, 201, 41))
        self.pushButton_3.setStyleSheet("background-color: rgb(0, 116, 0)")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(750, 40, 181, 41))
        self.pushButton_4.setStyleSheet("background-color: rgb(0, 116, 0)")
        self.pushButton_4.setObjectName("pushButton_4")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Identifiers"))
        self.pushButton_2.setText(_translate("Form", "Lexems"))
        self.pushButton_3.setText(_translate("Form", "Constants"))
        self.pushButton_4.setText(_translate("Form", "Labels"))

