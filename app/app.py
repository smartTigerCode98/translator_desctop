
import sys
from gui.interface import *
from gui.output_table import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QWidget, QGridLayout, QTableWidget
from PyQt5.QtCore import QSize, Qt

from lexical_analyzer.lexical_analyzer import *
from plz.plz_builder import PLZBuilder
from plz.plz_executor import PLZExecutor
from syntactical_analyzer.syntactical_analyzer import *
from syntactical_analyzer.automatic_machine import *
from syntactical_analyzer.syntactical_relation_analyzer import *


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.count_line = 1

        self.ui.textEdit.installEventFilter(self)
        self.ui.textEdit_2.append(str(self.count_line))

        self.ui.pushButton.clicked.connect(self.clear_code_space)
        self.ui.pushButton_1.clicked.connect(self.openProgramFile)
        self.ui.pushButton_2.clicked.connect(self.saveProgramFile)
        self.ui.pushButton_3.clicked.connect(self.show_output_table)
        self.ui.pushButton_4.clicked.connect(self.analyze_text_program)

        self.ui.pushButton_3.setEnabled(False)



    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return:
                self.count_line += 1
                self.ui.textEdit_2.append(str(self.count_line))
                return False
            if event.key() == QtCore.Qt.Key_Backspace:
                text = self.ui.textEdit.toPlainText()
                splited_text = text.split('\n')
                if splited_text[len(splited_text)-1] == '':
                    count_enter_in_code = len(splited_text) - 2
                else:
                    count_enter_in_code = len(splited_text) - 1
                if count_enter_in_code >= 0:
                    if (self.count_line - count_enter_in_code) > 1:
                        self.count_line = count_enter_in_code + 1
                        self.ui.textEdit_2.clear()
                        for i in range(1, self.count_line + 1):
                            self.ui.textEdit_2.append(str(i))
                return False
        return False

    def openProgramFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file')[0]
        if fname:
            text_program = ''
            file_with_code = open(fname, 'r')
            for line in file_with_code:
                text_program += line
            self.ui.textEdit.clear()
            self.ui.textEdit_2.clear()
            self.count_line = len(text_program.split('\n'))
            print(self.count_line)
            for i in range(1, self.count_line + 1):
                self.ui.textEdit_2.append(str(i))
            self.ui.textEdit.append(text_program)
            file_with_code.close()


    def saveProgramFile(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file')[0]
        if fname:
            text_program = self.ui.textEdit.toPlainText()
            file_for_code = open(fname, 'w')
            file_for_code.write(text_program)
            file_for_code.close()


    def analyze_text_program(self):
        text_program = self.ui.textEdit.toPlainText()
        if text_program:
            self.ui.pushButton_3.setEnabled(True)
        self.ui.textEdit_3.clear()
        if text_program:
            lexical_analyzer = LexicalAnalyzer(text_program)
            lexical_analyzer.run()
            lexical_analyzer.show_output_table()
            self.lexical_analyzer = lexical_analyzer
            if lexical_analyzer.has_errors():
                errors = lexical_analyzer.get_errors()
                for err in errors:
                    print(err)
                    self.ui.textEdit_3.append(err)
            else:
                syntaxical_analazer = AutomaticMachine(lexical_analyzer.get_output_lexems())
                syntaxical_analazer.run()
                self.input_table = syntaxical_analazer.get_input_table()
                self.parse_table = syntaxical_analazer.get_parse_table()
                errors = syntaxical_analazer.get_errors()
                if errors:
                    for err in errors:
                        self.ui.textEdit_3.append(err)
                else:
                    self.ui.textEdit_3.append("The program successfully passed the lexical and syntactic analysis.")
                    self.plz_builder = PLZBuilder(lexical_analyzer.get_output_lexems())
                    self.plz_builder.run()
                    self.plz_executor = PLZExecutor(self.plz_builder.plz, self.plz_builder.label_table,
                                                    lexical_analyzer.get_id_table())
                    self.plz_executor.run()

    def clear_code_space(self):
        self.ui.textEdit.clear()
        self.ui.textEdit_2.clear()
        self.ui.textEdit_3.clear()
        self.count_line = 1
        self.ui.textEdit_2.append(str(self.count_line))

    def show_output_table(self):
        # self.ui.open_window_with_table()
        self.window = QtWidgets.QMainWindow()
        self.table_window = Ui_Form()
        self.table_window.setupUi(self.window)
        self.window.show()
        self.table_window.pushButton_1.clicked.connect(self.show_lexem)
        self.table_window.pushButton_2.clicked.connect(self.show_idn)
        self.table_window.pushButton_3.clicked.connect(self.show_con)
        self.table_window.pushButton_4.clicked.connect(self.show_label)

        self.table_window.pushButton_5.clicked.connect(self.show_input_tabel)
        self.table_window.pushButton_6.clicked.connect(self.show_parse_tabel)

    def show_parse_tabel(self):
        self.table_window.textEdit.clear()
        self.table_window.textEdit.append(self.plz_builder.show_plz_table())
        self.table_window.textEdit.append("Result poliz: " + self.plz_builder.plz_to_str())
        self.table_window.textEdit.append(self.parse_table)
        cursor = self.table_window.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Start)
        self.table_window.textEdit.setTextCursor(cursor)

    def show_input_tabel(self):
        self.table_window.textEdit.clear()
        grammar = ""
        file = open('F://translator_desctop//gr.txt')
        if file:
            grammar = file.read()
        file.close()
        self.table_window.textEdit.append(grammar)
        cursor = self.table_window.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Start)
        self.table_window.textEdit.setTextCursor(cursor)




    def show_lexem(self):
        self.table_window.textEdit.clear()
        self.table_window.textEdit.append(Lexem.table_lexes_to_string(self.lexical_analyzer.get_output_lexems()))
        cursor = self.table_window.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Start)
        self.table_window.textEdit.setTextCursor(cursor)

    def show_idn(self):
        self.table_window.textEdit.clear()
        self.table_window.textEdit.append(Identifier.table_lexes_to_string(self.lexical_analyzer.get_id_table()))
        cursor = self.table_window.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Start)
        self.table_window.textEdit.setTextCursor(cursor)

    def show_con(self):
        self.table_window.textEdit.clear()
        self.table_window.textEdit.append(Constant.table_lexes_to_string(self.lexical_analyzer.get_constants_table()))
        cursor = self.table_window.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Start)
        self.table_window.textEdit.setTextCursor(cursor)

    def show_label(self):
        self.table_window.textEdit.clear()
        self.table_window.textEdit.append(Label.table_lexes_to_string(self.lexical_analyzer.get_labels_table()))
        cursor = self.table_window.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Start)
        self.table_window.textEdit.setTextCursor(cursor)



    @staticmethod
    def run():
        app = QtWidgets.QApplication(sys.argv)
        my_app = MyWin()
        my_app.show()
        sys.exit(app.exec_())

