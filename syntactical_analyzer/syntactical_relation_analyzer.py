
from relation_anxiety.relation_anxiety import *
from beautifultable import BeautifulTable


class ParseTable(object):
    def __init__(self, number, stack, relation, input_row):
        self.number = number
        self.stack = stack
        self.relation = relation
        self.input_row = input_row


class PreparedInputRow(object):
    def __init__(self, lexem, code_lexem):
        self.lexem = lexem
        self.code_lexem = code_lexem


class SyntacticalRelationAnalyzer(object):
    def __init__(self, lexical_table):
        self.stack = []
        self.parse_table = []
        self.lexical_table = lexical_table
        self.rel_table_obj = RelationAnxiety("F://translator_desctop//grammar.txt")
        self.rel_table_obj.set_the_relation_of_anxiety()
        self.rel_table = self.rel_table_obj.get_relation_table()
        self.input_row = self.__prepare_row()
        self.error = ''

    def get_parse_table_for_gui(self):
        return self.get_parse_table()

    def get_error(self):
        return self.error

    def run(self):
        self.stack.append('#')
        index = 0
        while self.error == '':
            stack = self.stack
            relation = self.__find_relation(self.__get_last_el_from_stack(),
                                            self.__check_id_or_const_or_label(self.input_row[index]))
            if relation in ['=', '<']:
                self.parse_table.append(ParseTable(number=len(self.parse_table) + 1, stack=self.__stack_to_sting(),
                                                   relation=relation, input_row=self.__input_row(index)))
                self.stack.append(self.__check_id_or_const_or_label(self.input_row[index]))
                index += 1
            elif relation == '>':
                foundation = ''
                self.parse_table.append(ParseTable(number=len(self.parse_table) + 1, stack=self.__stack_to_sting(),
                                                   relation=relation, input_row=self.__input_row(index)))
                for i in range(len(self.stack) - 1, 0, -1):
                    relation_sign = self.__find_relation(self.stack[i-1], self.stack[i])
                    if relation_sign != '<':
                        foundation = self.__add_part_foundation(foundation, i)
                    else:
                        foundation = self.__add_part_foundation(foundation, i)
                        left_part = self.__find_left_part_rule(foundation)
                        if left_part:
                            self.__change_stack(left_part, i)
                        else:
                            self.error = "Unexpected {lex} on line {line}".format(lex=self.lexical_table[index].lexem,
                                                                                  line=self.lexical_table[index].
                                                                                  line_number)
                            print('syka')
                            break

                        # print(foundation)
                        break
            else:
                self.error = "Unexpected {lex} on line {line}".format(lex=self.input_row[index].lexem,
                                                                      line=self.lexical_table[index].line_number)
                print(self.error)
                break

            if len(self.stack) == 2 and self.stack[0] == '#' and self.stack[1] == '<програма>':
                self.parse_table.append(ParseTable(number=len(self.parse_table) + 1, stack=self.__stack_to_sting(),
                                                   relation=relation, input_row=self.__input_row(index)))
                break
        print(self.get_parse_table())

    def __input_row(self, index):
        input_row = ''
        if index > 0:
            for i in range(index, len(self.lexical_table) - 1):
                input_row += self.lexical_table[i].lexem + ' '
        return input_row + '#'

    def __find_relation(self, first_el, second_el):
        if first_el == '#':
            return '<'
        if second_el == '#':
            return '>'
        relation_sign = self.rel_table[first_el][second_el]
        if relation_sign != 0:
            return relation_sign
        return False

    def __get_last_el_from_stack(self):
        if len(self.stack) > 0:
            return self.stack[len(self.stack) - 1]

    def __stack_to_sting(self):
        str_stack = ''
        for i in range(len(self.stack)):
            str_stack += self.stack[i] + ' '
        return str_stack

    def __check_id_or_const_or_label(self, lexem):
        code_lexem = lexem.code_lexem
        if code_lexem == 100:
            return 'id'
        elif code_lexem == 101:
            return 'const'
        elif code_lexem == 102:
            return 'label'
        elif code_lexem == 31:
            return '¶'
        else:
            return lexem.lexem

    def __change_stack(self, new_element, index):
        if 0 < index:
            self.stack = self.stack[0:index]
            self.stack.append(new_element)
        else:
            self.stack = []
            self.stack.append(new_element)

    def __find_left_part_rule(self, right_part):
        grammar_rules = self.rel_table_obj.rule_grammar
        for key, value in grammar_rules.items():
            for i in range(len(value)):
                if value[i] == right_part:
                    return key

        return False

    def __prepare_row(self):
        prepare_row = []
        for i in range(len(self.lexical_table)):
            prepare_row.append(PreparedInputRow(self.lexical_table[i].lexem, self.lexical_table[i].code_lexem))
        prepare_row.append(PreparedInputRow('#', 0))
        return prepare_row

    def get_parse_table(self):
        count = len(self.parse_table)
        if count > 0:
            table = BeautifulTable()
            table._max_table_width = 200
            table.column_headers = ["     №     ", "        Stack         ", "     Relation    ",
                                    "         Input row           "]
            for i in range(0, count):
                table.append_row([self.parse_table[i].number,
                                  self.parse_table[i].stack,
                                  self.parse_table[i].relation,
                                  self.parse_table[i].input_row])
            return str(table)

        return ''

    def __add_part_foundation(self, foundation, i):
        if len(foundation) > 0:
            foundation = self.stack[i] + ' ' + foundation
        else:
            foundation = self.stack[i]
        return foundation






