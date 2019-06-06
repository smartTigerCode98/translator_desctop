

class ParseRow(object):
    def __init__(self, number_of_configuration, current_state, lexem, state, stack):
        self.number_of_configuration = number_of_configuration
        self.current_state = current_state
        self.lexem = lexem
        self.state = state
        self.stack = stack



    def to_str(self):
        inf = 'conf: ' + str(self.number_of_configuration) + ' current_state: ' + str(self.current_state) + ' lexem: ' + str(self.lexem) + ' next_state: ' + str(self.state) + ' stack: ' + str(self.stack)
        inf += '\n'
        return inf
