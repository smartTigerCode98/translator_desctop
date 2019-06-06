from syntactical_analyzer.syntactical_exceptions import *
from syntactical_analyzer.parse_row import *
from syntactical_analyzer.input_automatic_table import *
from beautifultable import BeautifulTable


class AutomaticMachine(object):
    def __init__(self, output_table_lexems):
        self.lexems = output_table_lexems
        self.input_automatic_table = InputAutomaticTable()
        self.stack = []
        self.state = 1
        self.index = 0
        self.parse_table = []
        self.errors = SyntacticalExceptions()

    def __cheack_index_in_range(self):
        if self.index <= (len(self.lexems) - 1):
            return True
        else:
            return False

    def get_parse_table_str(self):
        table = ''
        if len(self.parse_table) > 0:
            for i in range(len(self.parse_table)):
                table += self.parse_table[i].to_str()

        print(table)

    def get_errors(self):
        return self.errors.get_errors()

    def get_stack_to_str(self):
        stack_str = ''
        if len(self.stack) > 0:
            for i in range(len(self.stack)):
                stack_str += str(self.stack[i]) + ', '
        return stack_str

    def get_parse_table(self):
        count = len(self.parse_table)
        if count > 0:
            table = BeautifulTable()
            table._max_table_width = 400
            table.column_headers = ["        Configuration            ", "  Current state  ", "Lexem", " Goto ",
                                    "        Stack         "]
            for i in range(0, count):
                table.append_row([self.parse_table[i].number_of_configuration,
                                  self.parse_table[i].current_state,
                                  self.parse_table[i].lexem,
                                  self.parse_table[i].state,
                                  self.parse_table[i].stack])
            return str(table)

        return ''

    def get_input_table(self):
        return self.input_automatic_table.input_table_to_string()

    def run(self):
        while True:
            row_input_table = self.input_automatic_table.get_row(self.state)
            if self.__cheack_index_in_range():
                lexem = self.lexems[self.index].lexem
                if self.lexems[self.index].code_lexem in [100, 101, 102]:
                    if self.lexems[self.index].code_lexem == 100:
                        lexem = 'id'
                    elif self.lexems[self.index].code_lexem == 101:
                        lexem = 'const'
                    else:
                        lexem = 'label'
            else:
                break

            if lexem in row_input_table.transition_label:
                if len(row_input_table.transition_label) != len(row_input_table.beta):
                    current_state = self.state
                    self.state = row_input_table.beta[0]
                    if row_input_table.stack[0] is not None:
                        self.stack = [row_input_table.stack[0]] + self.stack
                else:
                    index_of_state = row_input_table.transition_label.index(lexem)
                    if row_input_table.stack[index_of_state] is not None:
                        self.stack = [row_input_table.stack[index_of_state]] + self.stack
                    current_state = self.state
                    self.state = row_input_table.beta[index_of_state]

                self.parse_table.append(ParseRow(len(self.parse_table)+1, current_state, self.lexems[self.index].lexem,
                                                 self.state, self.get_stack_to_str()))
                self.index += 1
            else:
                semantic_routine = row_input_table.semantic_subroutine
                if semantic_routine.get('error'):
                    self.errors.add_exeption(semantic_routine.get('error') + str(self.lexems[self.index].line_number))
                    break
                elif semantic_routine.get('beta') and semantic_routine.get('beta') is not None:
                    current_state = self.state
                    self.state = semantic_routine.get('beta')
                    if semantic_routine.get('stack'):
                        self.stack = [semantic_routine.get('stack')] + self.stack
                    self.parse_table.append(
                        ParseRow(len(self.parse_table) + 1, current_state, '', self.state, self.get_stack_to_str())
                    )
                else:
                    current_state = self.state
                    if len(self.stack) > 0:
                        self.state = self.stack.pop(0)
                        self.parse_table.append(ParseRow(len(self.parse_table) + 1, current_state, '', self.state,
                                                         self.get_stack_to_str()))
        if self.state == 16:
            next_state = self.input_automatic_table.get_row(self.state).beta[0]
            self.parse_table.append(ParseRow(len(self.parse_table) + 1, self.state, '', next_state, self.get_stack_to_str()))

        if self.state != 16 and len(self.errors.get_errors()) == 0:

            err = self.input_automatic_table.get_row(self.state).semantic_subroutine.get('error')

            if err:

                line = self.__get_number_of_line()

                self.errors.add_exeption(err + str(line))

            else:

                state = self.input_automatic_table.get_row(self.state).semantic_subroutine.get('beta')

                if state:

                    err = self.input_automatic_table.get_row(state).semantic_subroutine.get('error')

                    if err:

                        line = self.__get_number_of_line()

                        self.errors.add_exeption(err + str(line))

                else:

                    len_stack = len(self.stack)

                    for i in range(len_stack):

                        state = self.stack[i]

                        err = self.input_automatic_table.get_row(state).semantic_subroutine.get('error')

                        if err:

                            line = self.__get_number_of_line()

                            self.errors.add_exeption(err + str(line))

                            break

    def __get_number_of_line(self):

        if self.input_automatic_table.get_row(self.state).transition_label[0] in ['\n', 'label', 'start', '{', '}']:
            return self.lexems[self.index - 1].line_number + 1

        else:
            return self.lexems[self.index - 1].line_number













