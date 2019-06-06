from parser_file.parser import *
from beautifultable import BeautifulTable


class RelationAnxiety(object):

    def __init__(self, file_name):
        self.parser = ParserFile(file_name=file_name)
        self.parser.run()
        self.table_relation = self.parser.get_table_relation()
        self.rule_grammar = self.parser.get_rule_grammar()
        self.conflicts = []

    def get_conflict(self):
        return self.conflicts

    def set_the_relation_of_anxiety(self):
        if len(self.parser.get_parse_errors()) == 0:
            self.__set_relation_equal()
            if self.__set_relation_less():
                self.__set_relation_more()

    def __set_relation_equal(self):
        for non_terminal in self.rule_grammar:
            alternative_definition = self.rule_grammar[non_terminal]
            count_alternative_definition = len(alternative_definition)
            for i in range(count_alternative_definition):
                elem_from_alter_def = alternative_definition[i].split(' ')
                if len(elem_from_alter_def) >= 2:
                    for j in range(len(elem_from_alter_def) - 1):
                        self.__set_relation(elem_from_alter_def[j].strip(' '), elem_from_alter_def[j+1].strip(' '), '=')

    def __set_relation_more(self):
        for first_element in self.table_relation:
            el_from_last_plus = []
            if self.parser.is_non_terminal(first_element):
                for second_element in self.table_relation[first_element]:
                    if self.__is_equal(first_element, second_element):
                        el_from_last_plus = self.__last_plus(first_element, el_from_last_plus)
                        # if not self.parser.is_non_terminal(second_element):
                        if len(el_from_last_plus) > 0:
                                for i in range(len(el_from_last_plus)):
                                    result = self.__set_relation(el_from_last_plus[i], second_element, '>')
                                    if not result:
                                        return False
                        # else:
                        if self.parser.is_non_terminal(second_element):
                            el_from_first_plus = []
                            el_from_first_plus = self.__first_plus(second_element, el_from_first_plus)
                            for i in range(len(el_from_last_plus)):
                                for j in range(len(el_from_first_plus)):
                                    result = self.__set_relation(el_from_last_plus[i], el_from_first_plus[j], '>')
                                    if not result:
                                        return False
                    else:
                        continue
            else:
                break
        return True

    def __set_relation_less(self):
        for first_element in self.table_relation:
            el_from_first_plus = []
            for second_element in self.table_relation[first_element]:
                if self.parser.is_non_terminal(second_element):
                    if self.__is_equal(first_element, second_element):
                        el_from_first_plus = self.__first_plus(second_element, el_from_first_plus)
                        if len(el_from_first_plus) > 0:
                            for i in range(len(el_from_first_plus)):
                                result = self.__set_relation(first_element, el_from_first_plus[i], '<')
                                if not result:
                                    return False
                    else:
                        continue
                else:
                    break

        return True

    def __is_equal(self, first_element, second_element):
        if self.table_relation[first_element][second_element] == '=':
            return True
        return False

    def __first_plus(self, non_terminal, list_of_element):
        if self.parser.is_non_terminal(non_terminal):
            alternative_def = self.rule_grammar[non_terminal]
            for i in range(len(alternative_def)):
                first_element = alternative_def[i].split(' ')[0].strip(' ')
                if first_element not in list_of_element:
                    list_of_element.append(first_element)
                if self.parser.is_non_terminal(first_element) and non_terminal != first_element:
                    self.__first_plus(first_element, list_of_element)
            return list_of_element

    def __last_plus(self, non_terminal, list_of_element):
        if self.parser.is_non_terminal(non_terminal):
            alternative_def = self.rule_grammar[non_terminal]
            for i in range(len(alternative_def)):
                elements = alternative_def[i].split(' ')
                len_elements = len(elements)
                last_element = elements[len_elements - 1].strip(' ')
                if last_element not in list_of_element:
                    list_of_element.append(last_element)
                if self.parser.is_non_terminal(last_element) and non_terminal != last_element:
                    self.__last_plus(last_element, list_of_element)
            return list_of_element

    def __set_relation(self, first_element, second_element, sign_relation):
        if self.table_relation[first_element][second_element] in [sign_relation, 0]:
            self.table_relation[first_element][second_element] = sign_relation
            return True
        else:
            self.conflicts.append(
                "Conflict situation with '{first}' and '{second}', new sign is {sign}, current sign is {cur}. "
                "Pleas,stratify your grammar.".format(
                      first=first_element, second=second_element, sign=sign_relation,
                      cur=self.table_relation[first_element][second_element]))
            return False

    def show_table(self):
        for record in self.table_relation:
            print(record + " : " + str(self.table_relation[record]))

    def get_relation_table(self):
        return self.table_relation

    def build_table(self):
        count = len(self.table_relation)
        if count > 0:
            table = BeautifulTable()
            table._max_table_width = 800
            table.column_headers = [' '] + self.parser.union_dict
            row = []
            for non_terminal in self.table_relation:
                current_row = self.table_relation[non_terminal]
                row.clear()
                row.append(non_terminal)
                for key in current_row:
                    row.append(current_row[key])
                table.append_row(row)
            print(table)

    def get_first_column(self):
        count = len(self.parser.union_dict)
        if count > 0:
            table = BeautifulTable()
            table._max_table_width = 800
            for i in range(count):
                table.append_row([self.parser.union_dict[i]])
            return str(table)

    def get_table_for_gui(self):
        count = len(self.table_relation)
        if count > 0:
            table = BeautifulTable()
            table._max_table_width = 800
            table.column_headers = self.parser.union_dict
            row = []
            for non_terminal in self.table_relation:
                current_row = self.table_relation[non_terminal]
                row.clear()
                for key in current_row:
                    row.append(current_row[key])
                table.append_row(row)

            return table

    def get_header(self):
        table = self.get_table_for_gui()
        parts = str(table).split('\n')
        header = parts[0] + '\n' + parts[1] + '\n' + parts[2]
        return header

    def get_only_value_from_table(self):
        table = self.get_table_for_gui()
        parts = str(table).split('\n')
        value = ''
        for i in range(2, len(parts)):
            value += parts[i]
            if i != len(parts) - 1:
                value += '\n'
        return value
