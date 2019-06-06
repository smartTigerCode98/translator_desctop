import re
import tkinter

from lexical_analyzer.identifier import Identifier
from tkinter import *
from plz.label import *


class PLZExecutor(object):
    def __init__(self, plz, label_table, id_table):
        self.stack = []
        self.plz = plz
        self.label_table = label_table
        self.id_table = id_table
        self.error = ''

    def run(self):
        len_plz = len(self.plz)
        i = 0
        while i <= len_plz - 1:
            if self.plz[i].find('m') == 0 and self.plz[i+1] == 'УПХ':
                logical_result = self.stack.pop()
                if logical_result is False:
                    i = Label.find_label(self.label_table, self.plz[i]).value - 2
                else:
                    if i + 2 <= len_plz - 1:
                        i = i + 1
                    else:
                        break
            elif self.plz[i].find('$') == 0 and i+1 < len_plz and self.plz[i+1] == 'БП':
                i = Label.find_label(self.label_table, self.plz[i]).value - 2
            elif (self.is_variable(self.plz[i]) or self.is_number(self.plz[i])) \
                    and self.plz[i] not in ['int', 'float', 'echo', 'cin', 'not', 'or', 'and']:
                self.stack.append(self.plz[i])
            elif self.plz[i] in ['int', 'float']:
                self.stack.clear()
            elif self.is_binary_arithmetic_operator(self.plz[i]):
                second_operand = self.stack.pop()
                first_operand = self.stack.pop()
                if self.is_variable(str(first_operand)):
                    first_operand = Identifier.get_value(self.id_table, first_operand)
                    if first_operand is None:
                        self.error = "Variable is used without value"
                        print(self.error)
                        break
                if self.is_variable(str(second_operand)):
                    second_operand = Identifier.get_value(self.id_table, second_operand)
                    if second_operand is None:
                        self.error = "Variable is used without value"
                        break
                result_calculate = self.__calculate(first_operand, second_operand, self.plz[i])
                if result_calculate is not None:
                    self.stack.append(result_calculate)
                else:
                    self.error = "Divide on zero"
                    break
            elif self.plz[i] == '=':
                value = self.stack.pop()
                name_variable = self.stack.pop()
                Identifier.set_value(self.id_table, name_variable, value)

            elif self.plz[i] == 'echo':
                result = ''
                while len(self.stack) > 0:
                    head_element_from_stack = self.stack.pop()
                    if self.is_variable(str(head_element_from_stack)):
                        head_element_from_stack = Identifier.get_value(self.id_table, head_element_from_stack)
                        if head_element_from_stack is None:
                            self.error = "Variable is used without value"
                            break
                        else:
                            result = str(head_element_from_stack) + '\n' + result
                self.__output_window(result)

            elif self.plz[i] == 'cin':
                while len(self.stack) > 0:
                    is_number = False
                    variable = self.stack.pop()
                    value = 0
                    while not is_number:
                        value = self.inputbox('input window', 'Please, input value of variable {var}'.format(var=variable),
                                              'input')
                        is_number = self.is_number(value)
                    Identifier.set_value(self.id_table, variable, value)

            elif self.is_relation_sign(self.plz[i]):
                second_operand = self.stack.pop()
                first_operand = self.stack.pop()
                if self.is_variable(str(first_operand)):
                    first_operand = Identifier.get_value(self.id_table, first_operand)
                    if first_operand is None:
                        self.error = "Variable is used without value"
                        print(self.error)
                        break
                if self.is_variable(str(second_operand)):
                    second_operand = Identifier.get_value(self.id_table, second_operand)
                    if second_operand is None:
                        self.error = "Variable is used without value"
                        break
                logical_result = self.__finding_out_the_truth(float(first_operand), float(second_operand), self.plz[i])
                print(logical_result)
                self.stack.append(logical_result)

            elif self.is_logical_operator(self.plz[i]):
                if self.plz[i] == 'not':
                    operand = self.stack.pop()
                    result_operation = self.execute_logical_operation(self.plz[i], operand)
                    self.stack.append(result_operation)
                else:
                    second_operand = self.stack.pop()
                    first_operand = self.stack.pop()
                    result_operation = self.execute_logical_operation(self.plz[i], first_operand, second_operand)
                    print("Result " + str(result_operation))
                    self.stack.append(result_operation)

            i += 1



        print(Identifier.table_lexes_to_string(self.id_table))


    def is_variable(self, element_plz):
        format = re.compile("^[a-z]+[a-z0-9]*$")
        is_variable = re.match(format, element_plz)
        return is_variable

    def is_number(self, element):
        format = re.compile("^([-]?[1-9][0-9]*[.][0-9]+)$|^([-]?[0-9]+)$|^[-]?[0][.][0-9]+$")
        is_number = re.match(format, element)
        return is_number

    def is_binary_arithmetic_operator(self, element_plz):
        if element_plz in ['+', '-', '*', '/']:
            return element_plz
        return False

    def is_relation_sign(self, element_plz):
        if element_plz in ['>', '<', '==', '!=', '>=', '<=']:
            return element_plz
        return False

    def is_logical_operator(self, element_plz):
        print("PLDDDDDDDDDDD")
        if element_plz in ['not', 'and', 'or']:
            return element_plz
        return False

    def execute_logical_operation(self, logical_operator, first_operand, second_operand=None) -> bool:
        print("F " + str(first_operand))
        print("S " + str(second_operand))
        if logical_operator == 'not':
            return not first_operand
        elif logical_operator == 'and' and second_operand is not None:
            return first_operand and second_operand
        else:
            return first_operand or second_operand

    def __calculate(self, first_operand, second_operand, operator):
        first_operand = self.__convert_type(first_operand)
        second_operand = self.__convert_type(second_operand)
        if operator == '+':
            return first_operand + second_operand
        elif operator == '-':
            return first_operand - second_operand
        elif operator == '*':
            return first_operand * second_operand
        else:
            if second_operand != 0:
                return first_operand / second_operand
            else:
                return None

    def __convert_type(self, operand):
        converted_operand = operand
        if type(operand) == str:
            if '.' in operand:
                converted_operand = float(operand)
            else:
                converted_operand = int(operand)
        return converted_operand

    def __finding_out_the_truth(self, first_operand, second_operand, operator) -> bool:
        if operator == '>':
            return True if first_operand > second_operand else False
        elif operator == '<':
            return True if first_operand < second_operand else False
        elif operator == '==':
            return True if first_operand == second_operand else False
        elif operator == '!=':
            return True if first_operand != second_operand else False
        elif operator == '>=':
            return True if first_operand >= second_operand else False
        else:
            return True if first_operand <= second_operand else False

    def __output_window(self, data):
        root = Tk()
        root.title("Execution result")
        root.geometry("400x300")
        output = Text(root, width=20, height=20)
        output.insert(1.0, str(data))
        output.config(state=DISABLED)
        output.insert(1.0, 'ase')
        output.pack()
        root.mainloop()

    def inputbox(self, title, message, button_text):
        root = tkinter.Tk()
        root.title(title)
        root.resizable(False, False)

        label = tkinter.Label(text=message)
        label.pack()

        text = ''

        def on_return(e=None):
            nonlocal text
            text = textbox.get()
            root.destroy()

        textbox = tkinter.Entry(width=40)
        textbox.bind('<Return>', on_return)
        textbox.pack()
        textbox.focus_set()

        button = tkinter.Button(text=button_text, command=on_return)
        button.pack()

        root.mainloop()

        return text