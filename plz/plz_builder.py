from plz.label import Label
from plz.plz_table import PLZTable
from plz.priority_table import PriorityTable
from beautifultable import BeautifulTable


class PLZBuilder(object):
    def __init__(self, lex_table):
        self.lex_table = lex_table
        self.priority_table = PriorityTable()
        self.plz = []
        self.stack = []
        self.label_table = []
        self.count_until = 0
        self.plz_table = []

    def run(self):
        for i in range(2, len(self.lex_table)):
            if self.lex_table[i].code_lexem in [100, 101]:
                self.__find_if_label_statement()
                self.plz.append(self.lex_table[i].lexem)
                self.plz_table.append(PLZTable(input_element=self.lex_table[i].lexem, stack=self.__stack_to_str(),
                                               output=self.lex_table[i].lexem))
            elif self.lex_table[i].code_lexem in [10, 12, 13, 30]:
                continue
            elif self.lex_table[i].code_lexem == 102:
                self.__find_if_label_statement()
                if self.lex_table[i-1].lexem == 'goto':
                    self.plz.append(self.lex_table[i].lexem)
                    self.plz_table.append(PLZTable(input_element=self.lex_table[i].lexem, stack=self.__stack_to_str(),
                                                   output=self.lex_table[i].lexem))
                else:
                    self.plz.append(self.lex_table[i].lexem + ':')
                    self.plz_table.append(PLZTable(input_element=self.lex_table[i].lexem, stack=self.__stack_to_str(),
                                                   output=self.lex_table[i].lexem))
                    self.__add_label_to_table(self.lex_table[i].lexem)
            else:
                self.__find_if_label_statement()
                self.__compare_priority_in_stack_and_input_row(i)
        print(self.plz)
        print(self.stack)
        print(self.show_label_table())
        print(self.show_plz_table())

    def __compare_priority_in_stack_and_input_row(self, index_input_element):
        priority_current_lex = self.priority_table.get_priority(self.lex_table[index_input_element].lexem)

        self.plz_table.append(PLZTable(input_element=self.lex_table[index_input_element].lexem))

        if self.lex_table[index_input_element].lexem == 'until':
            self.count_until += 1

        while True:
            if self.stack.__len__() == 0 and self.lex_table[index_input_element].lexem not in [')', '}', 'finish',
                                                                                               '\\n', 'goto', 'repeat',
                                                                                               'until']:
                self.stack.append(self.lex_table[index_input_element].lexem)
                break
            else:
                if self.lex_table[index_input_element].lexem not in ['(', '{', 'start', 'if', 'repeat']:

                    priority_element_from_head_stack = self.priority_table.get_priority(
                        self.__get_head_element_from_stack())

                    if priority_element_from_head_stack is False:
                        if self.lex_table[index_input_element].lexem in ['\\n', 'finish', 'until']:
                            head_stack = self.__get_head_element_from_stack()
                            result_find = -1
                            result_find_repeat = -1
                            if head_stack is not None:
                                result_find = head_stack.find('if m')
                                result_find_repeat = head_stack.find('repeat m')
                            if result_find != - 1:
                                # print(self.__get_head_element_from_stack())
                                # print(self.lex_table[index_input_element].lexem)
                                self.plz.append("БП")
                                self.plz_table[self.__get_last_index()].output += ' ' + str(self.__get_last_el_plz())
                                self.plz.append(self.__get_name_last_service_label() + ':')
                                self.plz_table[self.__get_last_index()].output += ' ' + str(self.__get_last_el_plz())
                                self.label_table[self.__get_index_last_service_label()].value = len(self.plz) + 1
                                self.__pop_element_from_stack()
                            if result_find_repeat != -1 and (((self.count_until > 1 and self.plz[len(self.plz)-1] in
                                 ['<','<=', '>', '>=', '!=', '=='])
                                                              or (self.lex_table[index_input_element].lexem == '\\n'
                                                                                       and self.count_until == 1))):
                                name_label = self.__pop_element_from_stack().split(' ')[1].split(':')[0]
                                self.plz.append(name_label)
                                self.plz_table[self.__get_last_index()].output += ' ' + str(self.__get_last_el_plz())
                                self.plz.append('УПХ')
                                self.plz_table[self.__get_last_index()].output += ' ' + str(self.__get_last_el_plz())
                            break
                        else:
                            head_stack = self.__get_head_element_from_stack()
                            result_find_if_label = -1
                            result_find = -1
                            if head_stack is not None:
                                result_find = head_stack.find('repeat m')
                                result_find_if_label = head_stack.find('if m')
                            if result_find != - 1 and self.lex_table[index_input_element].lexem != 'until':
                                self.stack.append(self.lex_table[index_input_element].lexem)
                            if result_find_if_label != - 1:
                                print(self.__get_head_element_from_stack())
                                print(self.lex_table[index_input_element].lexem)
                                self.plz.append("БП")
                                self.plz_table[self.__get_last_index()].output += ' ' + str(self.__get_last_el_plz())
                                self.plz.append(self.__get_name_last_service_label() + ':')
                                self.plz_table[self.__get_last_index()].output += ' ' + str(self.__get_last_el_plz())
                                self.label_table[self.__get_index_last_service_label()].value = len(self.plz) + 1
                                self.__pop_element_from_stack()

                            self.__is_goto(index_input_element)
                            break

                    elif priority_current_lex <= priority_element_from_head_stack:
                        element_from_stack = self.__pop_element_from_stack()
                        if element_from_stack not in ['(', '{', 'start', 'if', 'goto', 'repeat', None]:
                            self.plz.append(element_from_stack)
                            self.plz_table[self.__get_last_index()].output += ' ' + str(self.__get_last_el_plz())
                        else:
                            break

                    elif self.__priority_like_closing_bracket(self.lex_table[index_input_element].lexem):
                        element_from_stack = self.__pop_element_from_stack()
                        self.__is_goto(index_input_element)
                        if element_from_stack in ['(', '{', 'start', 'if', 'goto', None]:
                            break

                    else:
                        self.stack.append(self.lex_table[index_input_element].lexem)
                        break
                else:
                    if self.lex_table[index_input_element].lexem == 'repeat':
                        name_new_label = 'm' + str(self.__get_next_number_for_label())
                        self.label_table.append(Label(name=name_new_label, value=len(self.plz) + 2))
                        self.plz.append(name_new_label + ':')
                        self.plz_table[self.__get_last_index()].output += ' ' + str(self.__get_last_el_plz())
                        self.stack.append('repeat ' + name_new_label + ':')
                    else:
                        self.stack.append(self.lex_table[index_input_element].lexem)
                    break

        self.plz_table[self.__get_last_index()].stack = self.__stack_to_str()

    def __get_head_element_from_stack(self):
        len_stack = len(self.stack)
        if len_stack > 0:
            return self.stack[len_stack - 1]
        return None

    def __pop_element_from_stack(self):
        element_from_stack = None
        if len(self.stack) != 0:
            element_from_stack = self.stack.pop()
        return element_from_stack

    def __is_goto(self, index_input_element):
        if self.lex_table[index_input_element].lexem == 'goto':
            name_new_label = 'm' + str(self.__get_next_number_for_label())
            self.label_table.append(Label(name=name_new_label))
            self.plz.append(name_new_label)
            self.plz_table[self.__get_last_index()].output += ' ' + str(self.__get_last_el_plz())
            self.plz.append('УПХ')
            self.plz_table[self.__get_last_index()].output += ' ' + str(self.__get_last_el_plz())
            self.stack.append('if ' + name_new_label)
            self.stack.append('goto')
            # pass

    def __priority_like_closing_bracket(self, lex):
        if lex in [')', '}', 'finish', '\\n', 'goto', 'until']:
            return True
        return False

    def __get_next_number_for_label(self):
        next_number = 0
        for i in range(len(self.label_table)):
            if self.label_table[i].name.find('m') != -1:
                next_number += 1
        return next_number + 1

    def __count_repeat_label(self):
        count_repeat_label = 0
        for i in range(len(self.stack)):
            if self.stack[i].find('repeat m'):
                count_repeat_label += 1
        return count_repeat_label

    def show_label_table(self):
        count = len(self.label_table)
        if count > 0:
            table = BeautifulTable()
            table._max_table_width = 100
            table.column_headers = ["    name     ", "        value         "]
            for i in range(0, count):
                table.append_row([self.label_table[i].name,
                                  self.label_table[i].value])
            return str(table)

        return ''

    def __get_name_last_service_label(self):
        for i in range(len(self.label_table)-1, -1, -1):
            if self.label_table[i].name.find('$') == -1:
                return self.label_table[i].name

    def __get_index_last_service_label(self):
        for i in range(len(self.label_table)-1, -1, -1):
            print(self.label_table[i].name)
            if self.label_table[i].name.find('$') == -1:
                return i

    def __add_label_to_table(self, label):
        is_exist = False
        for i in range(len(self.label_table)):
            if self.label_table[i].name == label:
                is_exist = True
                break
        if not is_exist:
            self.label_table.append(Label(name=label, value=len(self.plz) + 1))

    def show_plz_table(self):
        count = len(self.plz_table)
        if count > 0:
            table = BeautifulTable()
            table._max_table_width = 200
            table.column_headers = ["    input     ", "        stack         ", "             output             "]
            for i in range(0, count):
                table.append_row([self.plz_table[i].input,
                                  self.plz_table[i].stack,
                                  self.plz_table[i].output])
            return str(table)

        return ''

    def __stack_to_str(self):
        str_stack = ''
        for i in range(len(self.stack)):
            str_stack += str(self.stack[i]) + ' '
        return str_stack

    def plz_to_str(self):
        plz_str = ''
        for i in range(len(self.plz)):
            plz_str += str(self.plz[i]) + ' '
        return plz_str

    def __get_last_index(self):
        if len(self.plz_table) > 0:
            return len(self.plz_table) - 1
        return None

    def __get_last_el_plz(self):
        if len(self.plz) > 0:
            return self.plz[len(self.plz) - 1]
        return None

    def __find_if_label_statement(self):
        head_stack = self.__get_head_element_from_stack()
        result_find_if_label = -1
        if head_stack is not None:
            result_find_if_label = head_stack.find('if m')
        if result_find_if_label != - 1:
            self.plz.append("БП")
            self.plz_table[self.__get_last_index()].output += ' ' + str(self.__get_last_el_plz())
            self.plz.append(self.__get_name_last_service_label() + ':')
            self.plz_table[self.__get_last_index()].output += ' ' + str(self.__get_last_el_plz())
            self.label_table[self.__get_index_last_service_label()].value = len(self.plz) + 1
            self.__pop_element_from_stack()

