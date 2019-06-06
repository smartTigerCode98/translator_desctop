
from PyQt5 import QtCore, QtGui, QtWidgets

from output_table import *


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(945, 896)
        MainWindow.setFixedSize(945, 815)
        MainWindow.setMinimumSize(QtCore.QSize(945, 0))
        MainWindow.setStyleSheet("background: rgb(0, 85, 127);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(140, 130, 771, 391))
        self.textEdit.setStyleSheet("background-color: white; margin-left: 20px;\n"
                                    "margin-right: 20px;")
        self.textEdit.setObjectName("textEdit")
        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(270, 20, 181, 41))
        self.pushButton_1.setStyleSheet("background: rgb(0, 170, 255)")
        self.pushButton_1.setObjectName("pushButton_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 20, 181, 41))
        self.pushButton_2.setStyleSheet("background: rgb(0, 170, 255)")
        self.pushButton_2.setObjectName("pushButton_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(490, 20, 181, 41))
        self.pushButton_3.setStyleSheet("background: rgb(0, 170, 255)")
        self.pushButton_3.setObjectName("pushButton_4")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(710, 20, 181, 41))
        self.pushButton_4.setStyleSheet("background: rgb(0, 170, 255)")
        self.pushButton_4.setObjectName("pushButton_5")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(50, 130, 101, 391))
        self.textEdit_2.setStyleSheet("background-color: white;")
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setReadOnly(True)
        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(50, 620, 841, 231))
        self.textEdit_3.setStyleSheet("background-color: black; color: green; font-size: 14px")
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_3.setReadOnly(True)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 580, 841, 41))
        self.label.setStyleSheet("background-color: white;\n"
                                 "")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(160, 90, 731, 41))
        self.label_2.setStyleSheet("background-color: grey;")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 90, 101, 41))
        self.label_3.setStyleSheet("background-color: grey")
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 530, 841, 41))
        self.pushButton.setStyleSheet("background-color: rgb(0, 170, 127)")
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 945, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.textEdit.verticalScrollBar().valueChanged.connect(self.textEdit_2.verticalScrollBar().setValue)
        self.textEdit_2.verticalScrollBar().valueChanged.connect(self.textEdit.verticalScrollBar().setValue)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textEdit.setHtml(_translate("MainWindow",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\" bgcolor=\"#ffffff\">\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:70px; margin-right:20px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

        self.pushButton_1.setText(_translate("MainWindow", "Open"))
        self.pushButton_2.setText(_translate("MainWindow", "Save"))
        self.pushButton_3.setText(_translate("MainWindow", "Show output table"))
        self.pushButton_4.setText(_translate("MainWindow", "Analyze program code"))
        self.label.setText(_translate("MainWindow",
                                      "                                                                                                                           Logical console"))
        self.label_2.setText(_translate("MainWindow",
                                        "                                                                                                  Space for entry code"))
        self.label_3.setText(_translate("MainWindow", "        Number line"))
        self.pushButton.setText(_translate("MainWindow", "CLEAR CODE SPACE"))