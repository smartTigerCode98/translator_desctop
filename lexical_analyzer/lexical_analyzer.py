from lexical_analyzer.constant import *
from lexical_analyzer.identifier import *
from lexical_analyzer.label import *
from lexical_analyzer.lexem import *
from lexical_analyzer.symbol_classes import *
from lexical_analyzer.table_tokens import *
from lexical_analyzer.lexical_exeptions import *


class LexicalAnalyzer(object):

    def __init__(self, program_text):
        self.ch = ''
        self.lex = ''
        self.state = 1
        self.has_to_read = True
        self.current_line = 1
        self.table_tokens = TableTokens()
        self.program_text = program_text
        self.collection_records_lexem = []
        self.collection_records_idn = []
        self.collection_records_con = []
        self.collection_records_label = []
        self.errors = LexicalExeptions()

        self.is_goto = False
        self.index_labels_without_declareted = 5

    def __next_char(self):
        if len(self.program_text) > 0:
            self.ch = self.program_text[0]
            if len(self.program_text) >= 2:
                self.program_text = self.program_text[1:]
            else:
                self.program_text = ''
        else:
            self.ch = ''


    def __lexemic_growth(self):
        self.lex += self.ch

    def __lexemic_growth_and_read_next_char(self):
        self.__lexemic_growth()
        self.__next_char()

    def which_line(self, symbol):
        if symbol == '\n':
            self.current_line =  self.current_line + 1

    def has_errors(self):
        if len(self.errors.get_errors()) > 0:
            return True
        return False

    def get_errors(self):
        return self.errors.get_errors()

    def get_output_lexems(self):
        return self.collection_records_lexem

    def get_id_table(self):
        return self.collection_records_idn

    def get_constants_table(self):
        return self.collection_records_con

    def get_labels_table(self):
        return self.collection_records_label

    def __err_for_not_defined_labels(self, all_labels_in_used_but_not_declareted):
        count = len(all_labels_in_used_but_not_declareted)
        print(count)
        if  count >  0:
            for i in range(count):
                self.errors.add_exeption('You use not defined label {label} on line {line}'.format(
                    label=all_labels_in_used_but_not_declareted[i],
                    line=Lexem.get_number_line_for_lexem(self.collection_records_lexem, all_labels_in_used_but_not_declareted[i])))

    def __label_in_err_labels(self, label, err_labels):
        count = len(err_labels)
        if count > 0:
            for i in range(count):
                if label == err_labels[i]:
                    return True
        return False


    def run(self):
        all_labels_in_used_but_not_declareted = []
        while len(self.program_text) >= 0:
            if self.state == 1:
                if self.has_to_read:
                    self.__next_char()
                while SymbolClasses.white_separator(self.ch):
                    self.__next_char()
                self.lex = ''
                if SymbolClasses.letter(self.ch):
                    self.__lexemic_growth_and_read_next_char()
                    self.state = 2
                elif SymbolClasses.number(self.ch):
                    self.__lexemic_growth_and_read_next_char()
                    self.state = 3
                elif SymbolClasses.plus(self.ch):
                    self.__lexemic_growth_and_read_next_char()
                    self.state = 6
                elif SymbolClasses.dot(self.ch):
                    self.__lexemic_growth_and_read_next_char()
                    self.state = 4
                elif SymbolClasses.single_character_splitters(self.ch):
                    self.__lexemic_growth()
                    self.has_to_read = True

                    if (self.ch == '\n'):
                        Lexem.add_lex(self.collection_records_lexem, self.current_line, '\\n', self.table_tokens.get_code(self.lex))
                    else:
                        Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, self.table_tokens.get_code(self.lex))

                    self.which_line(self.ch)

                    self.state = 1
                elif SymbolClasses.less(self.ch):
                    self.__lexemic_growth_and_read_next_char()
                    self.state = 7
                elif SymbolClasses.more(self.ch):
                    self.__lexemic_growth_and_read_next_char()
                    self.state = 8
                elif SymbolClasses.equally(self.ch):
                    self.__lexemic_growth_and_read_next_char()
                    self.state = 9
                elif SymbolClasses.exclamation(self.ch):
                    self.__lexemic_growth_and_read_next_char()
                    self.state = 10
                elif SymbolClasses.dollar(self.ch):
                    self.__lexemic_growth_and_read_next_char()
                    self.state = 11
                else:
                    if self.ch:
                        self.errors.add_exeption("Your symbol '{symbol}' on line {line} is not valid".format(
                            symbol = self.ch, line = self.current_line))
                    break

            elif self.state == 2:
                if SymbolClasses.letter(self.ch) or SymbolClasses.number(self.ch):
                    self.state = 2
                    self.__lexemic_growth_and_read_next_char()
                else:
                    if not self.table_tokens.get_code(self.lex):
                        code_idn = Identifier.find_idn(self.lex, self.collection_records_idn)
                        if not code_idn:
                            current_code_idn = len(self.collection_records_idn)
                            type_idn = Lexem.find_type_idn(self.collection_records_lexem)
                            if type_idn:
                                Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, 100, current_code_idn + 1)
                                Identifier.add_idn(self.collection_records_idn, current_code_idn + 1, self.lex, type_idn)
                            else:
                                self.errors.add_exeption("You use not defined identificator {id} on line {line}".format(
                                    id = self.lex, line = self.current_line))
                                break

                        else:
                            type_idn = Lexem.find_type_idn(self.collection_records_lexem)
                            if type_idn:
                                self.errors.add_exeption('You duplicate variable {var} on line {line}'.format(
                                    var = self.lex, line = self.current_line))
                                break
                            else:
                                Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, 100, code_idn)
                    else:
                        if self.lex == 'goto':
                            self.is_goto = True
                        Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, self.table_tokens.get_code(self.lex))
                    self.has_to_read = False
                    self.state = 1


            elif self.state == 3:
                if SymbolClasses.number(self.ch):
                    self.__lexemic_growth_and_read_next_char()
                    self.state = 3
                elif SymbolClasses.dot(self.ch):
                    self.__lexemic_growth_and_read_next_char()
                    self.state = 5
                else:
                    Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, 101, code_con = len(self.collection_records_con) + 1)
                    Constant.add_con(self.collection_records_con, len(self.collection_records_con) + 1, self.lex, Constant.type_con(self.lex))
                    self.state = 1
                    self.has_to_read = False


            elif self.state == 4:
                if SymbolClasses.number(self.ch):
                    self.__lexemic_growth_and_read_next_char()
                    self.state = 5
                else:
                    self.errors.add_exeption('You have not entered the fractional part of the constant. line = {line}'.format(
                        line = self.current_line))
                    break


            elif self.state == 5:
                if SymbolClasses.number(self.ch):
                    self.__lexemic_growth_and_read_next_char()
                    self.state = 5
                else:
                    Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, 101, code_con = len(self.collection_records_con) + 1)
                    Constant.add_con(self.collection_records_con, len(self.collection_records_con) + 1, self.lex, Constant.type_con(self.lex))
                    self.state = 1
                    self.has_to_read = False


            elif self.state == 6:
                if self.collection_records_lexem[len(self.collection_records_lexem) - 1].code_lexem == 101 or self.collection_records_lexem[len(self.collection_records_lexem) - 1].code_lexem == 100 or self.collection_records_lexem[len(self.collection_records_lexem) - 1].code_lexem == 25:
                    Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, self.table_tokens.get_code(self.lex))
                    self.state = 1
                    self.has_to_read = False
                elif SymbolClasses.number(self.ch):
                    self.__lexemic_growth_and_read_next_char()
                    self.state = 3
                elif SymbolClasses.dot(self.ch):
                    self.__lexemic_growth_and_read_next_char()
                    self.state = 4
                else:
                    self.errors.add_exeption('You have not entered a constant on line {line}'.format(line = self.current_line))
                    break


            elif self.state == 7:
                if SymbolClasses.less(self.ch):
                    self.__lexemic_growth()
                    Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, self.table_tokens.get_code(self.lex))
                    self.has_to_read = True
                elif SymbolClasses.equally(self.ch):
                    self.__lexemic_growth()
                    Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, self.table_tokens.get_code(self.lex))
                    self.has_to_read = True
                else:
                    Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, self.table_tokens.get_code(self.lex))
                    self.has_to_read = False
                self.state = 1


            elif self.state == 8:
                if SymbolClasses.more(self.ch):
                    self.__lexemic_growth()
                    Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, self.table_tokens.get_code(self.lex))
                    self.has_to_read = True
                elif SymbolClasses.equally(self.ch):
                    self.__lexemic_growth()
                    Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, self.table_tokens.get_code(self.lex))
                    self.has_to_read = True
                else:
                    Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, self.table_tokens.get_code(self.lex))
                    self.has_to_read = False
                self.state = 1

            elif self.state == 9:
                if SymbolClasses.equally(self.ch):
                    self.__lexemic_growth()
                    Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, self.table_tokens.get_code(self.lex))
                    self.has_to_read = True
                else:
                    Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, self.table_tokens.get_code(self.lex))
                    self.has_to_read = False
                self.state = 1

            elif self.state == 10:
                if SymbolClasses.equally(self.ch):
                    self.__lexemic_growth()
                    Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, self.table_tokens.get_code(self.lex))
                    self.has_to_read = True
                    self.state = 1
                else:
                    self.errors.add_exeption('Error. You must enter != on line {line}'.format(line = self.current_line))
                    break

            elif self.state == 11:
                if SymbolClasses.letter(self.ch):
                    self.__lexemic_growth_and_read_next_char()
                    self.state = 12
                else:
                    self.errors.add_exeption('Error label')
                    break

            elif self.state == 12:
                if SymbolClasses.letter(self.ch):
                    self.__lexemic_growth_and_read_next_char()
                    self.state = 12
                elif SymbolClasses.number(self.ch):
                    self.__lexemic_growth_and_read_next_char()
                    self.state = 12
                else:
                    code_label = Label.find_label(self.lex, self.collection_records_label)
                    if (not code_label or code_label == 0) and not self.is_goto and self.ch == ':':
                        if len(all_labels_in_used_but_not_declareted) > 0:
                            if self.__label_in_err_labels(self.lex, all_labels_in_used_but_not_declareted):
                                self.index_labels_without_declareted = all_labels_in_used_but_not_declareted.index(self.lex)
                            if self.index_labels_without_declareted >= 0:
                                index_label = Label.find_not_defined_label(all_labels_in_used_but_not_declareted.pop(self.index_labels_without_declareted), self.collection_records_label)
                                self.collection_records_label[index_label].code = index_label + 1
                                Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, 102,
                                              code_label = index_label + 1)
                                Lexem.set_code_for_label(self.lex, index_label + 1, self.collection_records_lexem)
                        else:
                            Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, 102,
                                           code_label = len(self.collection_records_label) + 1)
                            Label.add_label(self.collection_records_label, len(self.collection_records_label) + 1, self.lex)
                        self.index_labels_without_declareted = -1
                    elif not code_label and code_label != 0 and (self.is_goto or not self.ch == ':'):
                        Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, 102,
                                      code_label = len(self.collection_records_label) + 1)
                        Label.add_label(self.collection_records_label, 0, self.lex)
                        all_labels_in_used_but_not_declareted.append(self.lex)
                        self.is_goto = False
                    elif code_label and not self.is_goto and self.ch == ':':
                        self.errors.add_exeption('You duplicate label {label} on line {line}'.format(label = self.lex, line = self.current_line))
                        break
                    else:
                        Lexem.add_lex(self.collection_records_lexem, self.current_line, self.lex, 102, code_label = code_label)
                        self.is_goto = False
                    self.has_to_read = False
                    self.state = 1

            else:
                self.errors.add_exeption('Error')
        self.__err_for_not_defined_labels(all_labels_in_used_but_not_declareted)


    def show_output_table(self):
        Lexem.show_lexes(self.collection_records_lexem)
        Identifier.show_idn(self.collection_records_idn)
        Constant.show_con(self.collection_records_con)
        Label.show_label(self.collection_records_label)