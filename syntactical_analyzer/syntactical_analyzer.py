
from syntactical_analyzer.syntactical_exceptions import *

class SyntacticalAnalyzer(object):

    def __init__(self, output_table_lexems):
        self.lexems = output_table_lexems
        self.errors = SyntacticalExceptions()
        self.index = 0

    def run(self):
        self.program()

    def get_errors(self):
        return self.errors.get_errors()

    def __cheack_index_in_range(self):
        if self.index <= (len(self.lexems) - 1):
            return True
        else:
            return False

    def __get_valid_number_of_line(self):
        if self.__cheack_index_in_range():
            line = self.lexems[self.index].line_number
            return line
        else:
            if self.lexems[self.index - 1].code_lexem != 31:
                line = self.lexems[self.index - 1].line_number
            else:
                line = self.lexems[self.index - 1].line_number + 1
            return line

    def __get_line_for_lexem_after_enter(self):
        if self.__cheack_index_in_range():
            line = self.lexems[self.index].line_number
            return line
        else:
            line = self.lexems[self.index - 1].line_number + 1
            return line

    def program(self) -> bool:
        if self.lexems[self.index].lexem == 'tiger':
            self.index += 1
            if self.__cheack_index_in_range() and self.lexems[self.index].code_lexem == 100:
                self.index += 1
                if self.__cheack_index_in_range() and self.lexems[self.index].code_lexem == 31:
                    self.index += 1
                    if self.__cheack_index_in_range() and self.lexems[self.index].lexem == '{':
                        self.index += 1
                        if self.__cheack_index_in_range() and self.lexems[self.index].code_lexem == 31:
                            self.index += 1
                            if self.__cheack_index_in_range() and self.__list_declaration():
                                    if self.__cheack_index_in_range() and self.lexems[self.index].lexem == 'start':
                                        self.index += 1
                                        if self.__cheack_index_in_range() and self.lexems[self.index].code_lexem == 31:
                                            self.index += 1
                                            if self.__cheack_index_in_range() and self.__list_operation():
                                                    if self.__cheack_index_in_range() and self.lexems[self.index].lexem == 'finish':
                                                        self.index += 1
                                                        if self.__cheack_index_in_range() and self.lexems[self.index].code_lexem == 31:
                                                            self.index += 1
                                                            if self.__cheack_index_in_range() and self.lexems[self.index].lexem == '}':
                                                                return True
                                                            else:
                                                                self.errors.add_exeption('Closing bracket expected on line {line}'.format(
                                                                    line = self.__get_line_for_lexem_after_enter()))
                                                                return False
                                                        else:
                                                            self.errors.add_exeption('Delimiter expected(enter) on line {line}'.format(
                                                                line = self.__get_valid_number_of_line()))
                                                            return False
                                                    else:
                                                        self.errors.add_exeption("Wrong program finished. Expect keyword 'finish' after list of operation on line {line}".format(
                                                            line = self.__get_valid_number_of_line()))
                                                        return False
                                            else:
                                                self.errors.add_exeption("Invalid statement list on line {line}".format(
                                                    line = self.__get_valid_number_of_line()
                                                ))
                                                return False
                                        else:
                                            self.errors.add_exeption('Delimiter expected(enter) on line {line}'.format(
                                                line = self.__get_valid_number_of_line()))
                                            return False
                                    else:
                                        self.errors.add_exeption(
                                            "Wrong program started. Expect keyword 'start' on line {line}".format(
                                                line = self.__get_line_for_lexem_after_enter()))
                                        return False
                            else:
                                self.errors.add_exeption("Invalid declaration list on line {line}".format(
                                    line = self.__get_valid_number_of_line()
                                ))
                                return False
                        else:
                            self.errors.add_exeption('Delimiter expected(enter) on line {line}'.format(
                                line = self.__get_valid_number_of_line()))
                            return False
                    else:
                        self.errors.add_exeption('Opening bracket expected on line {line}'.format(
                            line = self.__get_line_for_lexem_after_enter()))
                        return False
                else:
                    self.errors.add_exeption('Delimiter expected(enter) after progran name on line {line}'.format(
                        line = self.__get_valid_number_of_line()))
                    return False
            else:
                self.errors.add_exeption("Expected name program on line {line}".format(
                    line = self.__get_valid_number_of_line()
                ))
                return False
        else:
            self.errors.add_exeption("Expected keyword 'tiger' on line {line}".format(
                line = self.__get_valid_number_of_line()
            ))
            return False


    def __list_declaration(self) -> bool:
        if self.__cheack_index_in_range() and self.__declaration():
            if self.__cheack_index_in_range() and self.lexems[self.index].code_lexem == 31:
                self.index += 1
                while self.__cheack_index_in_range() and self.lexems[self.index].lexem != 'start':
                    if self.__cheack_index_in_range() and self.__declaration():
                        if self.__cheack_index_in_range() and self.lexems[self.index].code_lexem == 31:
                            self.index += 1
                            continue
                        else:
                            self.errors.add_exeption(
                                'Delimiter expected(enter) after declaration on line {line}'.format(
                                    line = self.__get_valid_number_of_line()))
                            return False
                    else:
                        return False #see
                return True
            else:
                self.errors.add_exeption('Delimiter expected(enter) after declaration on line {line}'.format(
                    line = self.__get_valid_number_of_line()))
                return False
        else:
            self.errors.add_exeption("No identifiers are declared after opening bracket on line {line}".format(
                line = self.__get_valid_number_of_line()
            ))
            return False


    def __declaration(self) -> bool:
        if self.__cheack_index_in_range() and self.__type():
            if self.__cheack_index_in_range() and self.__id_list():
                return True
            else:
                self.errors.add_exeption('Expected identifier on line {line}'.format(
                    line = self.__get_valid_number_of_line()))
                return False
        else:
            self.errors.add_exeption(
                'Expected type identifiers on line {line}'.format(line = self.__get_valid_number_of_line()))
            return False


    def __id_list(self) -> bool:
        if  self.lexems[self.index].code_lexem == 100:
            self.index += 1
            while self.__cheack_index_in_range() and self.lexems[self.index].lexem == ',':
                self.index += 1
                if self.__cheack_index_in_range() and self.lexems[self.index].code_lexem == 100:
                    self.index += 1
                else:
                    self.errors.add_exeption('Expected identifier after coma on line {line}'.format(
                        line=self.__get_valid_number_of_line()))
                    return False
            return True
        else:
            return False


    def __type(self) -> bool:
        if self.__cheack_index_in_range() and (self.lexems[self.index].lexem == 'int' or self.lexems[self.index].lexem == 'float'):
            self.index += 1
            return True
        else:
            self.errors.add_exeption('No type of variables found on line {line}'.format(
                line = self.__get_valid_number_of_line()
            ))
            return False


    def __operation(self) -> bool:
        is_valid_index = self.__cheack_index_in_range()
        if is_valid_index:
            if self.__input_operator():
                return True
            elif self.__output_operator():
                return True
            elif self.__operator_assignment():
                return True
            elif self.__operator_loop():
                return True
            elif self.__operator_conditional_jump():
                return True
            else:
                return False
        else:
            return False


    def __list_operation(self) -> bool:
        if self.__cheack_index_in_range() and not self.__is_label_before_operation():
            return False
        if self.__cheack_index_in_range() and self.__operation():
            # while self.__cheack_index_in_range() and not (self.lexems[self.index].lexem in ['finish', 'until']):
            while self.__cheack_index_in_range() and self.lexems[self.index].code_lexem == 31:
                    self.index += 1
                    if self.__cheack_index_in_range() and not self.__is_label_before_operation():
                        return False
                    if self.__cheack_index_in_range() and self.__operation():
                       continue
                    else:
                        self.errors.add_exeption("Expected operator on line {line}".format(
                            line = self.__get_valid_number_of_line()
                        ))
                        return False
                # else:
                #     return True
            return True
        else:
            return False


    def __is_label_before_operation(self) -> bool:
        if self.__cheack_index_in_range() and self.lexems[self.index].code_lexem == 102:
            self.index += 1
            if self.__cheack_index_in_range() and self.lexems[self.index].lexem == ':':
                self.index += 1
                return True
            else:
                self.errors.add_exeption("Expected keysymbol ':' after label {label} on line {line}".format(
                    label = self.lexems[self.index - 1].lexem, line=self.__get_valid_number_of_line()
                ))
                return False
        else:
            return True


    def __input_operator(self) -> bool:
        if self.__cheack_index_in_range() and self.lexems[self.index].lexem == 'cin':
            self.index += 1
            if self.__cheack_index_in_range() and self.lexems[self.index].lexem == '>>':
                self.index += 1
                if self.__cheack_index_in_range() and self.lexems[self.index].code_lexem == 100:
                    self.index += 1
                    while self.__cheack_index_in_range() and self.lexems[self.index].lexem == '>>':
                        self.index += 1
                        if self.__cheack_index_in_range() and self.lexems[self.index].code_lexem == 100:
                            self.index += 1
                        else:
                            self.errors.add_exeption("Expected identifier after '>>' on line {line}".format(
                                line = self.__get_valid_number_of_line()
                            ))
                            return False
                    return True
                else:
                    self.errors.add_exeption("Expected identifier after '>>' on line {line}".format(
                        line = self.__get_valid_number_of_line()
                    ))
                    return False
            else:
                self.errors.add_exeption("Expected symbol '>>' after keyword 'cin' on line {line}".format(
                    line = self.__get_valid_number_of_line()
                ))
                return False
        else:
            return False

    def __output_operator(self) -> bool:
        if self.__cheack_index_in_range() and self.lexems[self.index].lexem == 'echo':
            self.index += 1
            if self.__cheack_index_in_range() and self.lexems[self.index].lexem == '<<':
                self.index += 1
                if self.__cheack_index_in_range() and self.lexems[self.index].code_lexem == 100:
                    self.index += 1
                    while self.__cheack_index_in_range() and self.lexems[self.index].lexem == '<<':
                        self.index += 1
                        if self.__cheack_index_in_range() and self.lexems[self.index].code_lexem == 100:
                            self.index += 1
                        else:
                            self.errors.add_exeption("Expected identifier after '<<' on line {line}".format(
                                line = self.__get_valid_number_of_line()
                            ))
                            return False
                    return True
                else:
                    self.errors.add_exeption("Expected identifier after '<<' on line {line}".format(
                        line = self.__get_valid_number_of_line()
                    ))
                    return False
            else:
                self.errors.add_exeption("Expected symbol '<<' after keyword 'echo' on line {line}".format(
                    line = self.__get_valid_number_of_line()
                ))
                return False
        else:
            return False

    def __operator_assignment(self) -> bool:
        if self.__cheack_index_in_range() and self.lexems[self.index].code_lexem == 100:
            self.index += 1
            if self.__cheack_index_in_range() and self.lexems[self.index].lexem  == '=':
                self.index += 1
                if self.__cheack_index_in_range() and self.__expression():
                    return True
                else:
                    self.errors.add_exeption("Expected expression after '{symbol}' on line {line}".format(
                        symbol = self.lexems[self.index - 1].lexem, line = self.__get_valid_number_of_line()
                    ))
                    return False
            else:
                self.errors.add_exeption("Expected '=' after '{id}' on line {line}".format(
                    id = self.lexems[self.index - 1].lexem, line = self.__get_valid_number_of_line()
                ))
                return False
        else:
            return False


    def __expression(self) -> bool:
        if self.__term():
            while self.__cheack_index_in_range() and self.lexems[self.index].lexem in ['+', '-']:
                self.index += 1
                if self.__cheack_index_in_range() and self.__term():
                    pass
                else:
                    self.errors.add_exeption('Expected term on line {line}'.format(
                        line = self.__get_valid_number_of_line()
                    ))
                    return False
            return True
        else:
            self.errors.add_exeption('Expected term on line {line}'.format(
                line = self.__get_valid_number_of_line()
            ))
            return False


    def __term(self) -> bool:
        if self.__cheack_index_in_range() and self.__multiplier():
            while self.__cheack_index_in_range() and self.lexems[self.index].lexem in ['*', '/']:
                self.index += 1
                if self.__cheack_index_in_range() and self.__multiplier():
                    pass
                else:
                    self.errors.add_exeption('Expected multiplier on line {line}'.format(
                        line = self.__get_valid_number_of_line()
                    ))
                    return False
            return True
        else:
            self.errors.add_exeption('Expected multiplier on line {line}'.format(
                line = self.__get_valid_number_of_line()
            ))
            return False


    def __multiplier(self) -> bool:
        if self.__cheack_index_in_range() and self.lexems[self.index].lexem == '(':
            self.index += 1
            if self.__cheack_index_in_range() and self.__expression():
                if self.__cheack_index_in_range() and self.lexems[self.index].lexem == ')':
                    self.index += 1
                    return True
                else:
                    self.errors.add_exeption('Closing bracket expected on line {line}'.format(
                        line = self.__get_valid_number_of_line()
                    ))
                    return False
            else:
                self.errors.add_exeption("Expected expression after '(' on line {line}".format(
                    line = self.__get_valid_number_of_line()
                ))
                return False
        elif self.__cheack_index_in_range() and self.lexems[self.index].code_lexem in [100, 101]:
            self.index += 1
            return True
        else:
            return False


    def __operator_loop(self) -> bool:
        if self.__cheack_index_in_range() and self.lexems[self.index].lexem == 'repeat':
            self.index += 1
            if self.__cheack_index_in_range() and self.__list_operation():
                if self.__cheack_index_in_range() and self.lexems[self.index].lexem == 'until':
                    self.index += 1
                    if self.__cheack_index_in_range() and self.__logical_expression():
                        return True
                    else:
                        self.errors.add_exeption("Expected logical expression after keyword 'until'")
                        return False
                else:
                    self.errors.add_exeption("Expected keyword 'until' after list of expression on line {line}".format(
                        line = self.__get_valid_number_of_line()
                    ))
                    return False
            else:
                self.errors.add_exeption("Expected list of expression after keyword 'repeat' on line {line}".format(
                    line = self.__get_valid_number_of_line()
                ))
                return False
        else:
            return False



    def __logical_expression(self) -> bool:
        if self.__get_valid_number_of_line() and self.__logical_term():
            while self.__cheack_index_in_range() and self.lexems[self.index].lexem == 'or':
                self.index += 1
                if self.__cheack_index_in_range() and self.__logical_term():
                    pass
                else:
                    self.errors.add_exeption('Expected logical term on line {line}'.format(
                        line = self.__get_valid_number_of_line()
                    ))
                    return False
            return True
        else:
            self.errors.add_exeption('Expected logical term on line {line}'.format(
                line = self.__get_valid_number_of_line()
            ))
            return False


    def __logical_term(self) -> bool:
        if self.__cheack_index_in_range() and self.__logical_multiplier():
            while self.__cheack_index_in_range() and self.lexems[self.index].lexem == 'and':
                self.index += 1
                if self.__cheack_index_in_range() and self.__logical_multiplier():
                    pass
                else:
                    self.errors.add_exeption('Expected logical multiplier on line5 {line}'.format(
                        line = self.__get_valid_number_of_line()
                    ))
                    return False
            return True
        else:
            self.errors.add_exeption('Expected logical multiplier on line {line}'.format(
                line = self.__get_valid_number_of_line()
            ))
            return False

    def __logical_multiplier(self) -> bool:
        if self.__cheack_index_in_range() and self.lexems[self.index].lexem == 'not':
            self.index += 1
            if self.__cheack_index_in_range() and self.__logical_multiplier():
                return True
            else:
                self.errors.add_exeption("Expected logical multiplier after keyword 'not' on line {line}".format(
                    line = self.__get_valid_number_of_line()
                ))
                return False
        elif self.__cheack_index_in_range() and self.lexems[self.index].lexem == '(':
            self.index += 1
            if self.__cheack_index_in_range() and self.__logical_expression():
                if self.__cheack_index_in_range() and self.lexems[self.index].lexem == ')':
                    self.index += 1
                    return True
                else:
                    self.errors.add_exeption("Closing bracket expected after logical expression on line {line}".format(
                        line = self.__get_valid_number_of_line()))
                    return False
            else:
                self.errors.add_exeption("Expected logical expression after opening bracket on line {line}".format(
                    line = self.__get_valid_number_of_line()))
                return False
        elif self.__cheack_index_in_range() and self.__logical_relation():
            return True
        else:
            return False



    def __logical_relation(self) -> bool:
        if self.__cheack_index_in_range() and self.__expression():
            if self.__cheack_index_in_range() and self.__sign_relation():
                if self.__cheack_index_in_range() and self.__expression():
                    return True
                else:
                    self.errors.add_exeption("Expected expression after sign relation on line {line}".format(
                        line = self.__get_valid_number_of_line()
                    ))
                    return False
            else:
                self.errors.add_exeption("Expected sign relation after expression on line {line}".format(
                    line = self.__get_valid_number_of_line()
                ))
                return False
        else:
            self.errors.add_exeption("Expected expression on line {line}".format(
                line = self.__get_valid_number_of_line()
            ))
            return False


    def __sign_relation(self) -> bool:
        if self.__cheack_index_in_range() and self.lexems[self.index].lexem in ['>', '<', '>=', '<=', '==', '!=']:
            self.index += 1
            return True
        else:
            return False

    def __operator_conditional_jump(self) -> bool:
        if self.__cheack_index_in_range() and self.lexems[self.index].lexem == 'if':
            self.index += 1
            if self.__cheack_index_in_range() and self.__logical_expression():
                if self.__cheack_index_in_range() and self.lexems[self.index].lexem == 'goto':
                    self.index += 1
                    if self.__cheack_index_in_range() and self.lexems[self.index].code_lexem == 102:
                        self.index += 1
                        return True
                    else:
                        self.errors.add_exeption("Expected label  after keyword 'goto' on line {line}".format(
                            line = self.__get_valid_number_of_line()
                        ))
                        return False
                else:
                    self.errors.add_exeption("Expected keyword 'goto' after logical expression on line {line}".format(
                        line = self.__get_valid_number_of_line()
                    ))
                    return False
            else:
                self.errors.add_exeption("Expected logical expression after keyword 'if' on line {line}".format(
                    line = self.__get_valid_number_of_line()
                ))
                return False
        else:
            return False


    def show_errors(self):
        if len(self.errors.get_errors()) > 0:
            errors = self.errors.get_errors()
            for error in errors:
                print(error)
