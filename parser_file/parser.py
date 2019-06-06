
class ParserFile(object):
    def __init__(self, file_name):
        self.file = open(file_name)
        self.terminal = []
        self.non_terminal = []
        self.rule_grammar = {}
        self.union_dict = []
        self.table_relation = {}
        self.all_non_terminals = []
        self.all_grammar = ''
        self.errors = []

    def get_terminal(self):
        return self.terminal

    def get_non_terminal(self):
        return self.non_terminal

    def get_rule_grammar(self):
        return self.rule_grammar

    def get_table_relation(self):
        return self.table_relation

    def run(self):
        self.__all_non_terminals()
        rule_grammar = self.file.readline()
        while rule_grammar:
            self.all_grammar += rule_grammar
            parts_rule_grammar = rule_grammar.rstrip('\n').split('::=')
            self.__add_rule(parts_rule_grammar)
            self.__add_non_terminal(parts_rule_grammar[0].strip(' '))
            alternative_parts_right_side_rule = parts_rule_grammar[1].split('|')
            for i in range(len(alternative_parts_right_side_rule)):
                union_dict = alternative_parts_right_side_rule[i].strip(' ').split(' ')
                for j in range(len(union_dict)):
                    if self.is_non_terminal(union_dict[j].lstrip(' ').rstrip(' ')):
                        if union_dict[j].lstrip(' ').rstrip(' ') in self.all_non_terminals:
                            self.__add_non_terminal(union_dict[j].lstrip(' ').rstrip(' '))
                        else:
                            self.errors.append("You use not defined non_terminal '{non_terminal}'".format(
                                non_terminal=union_dict[j].lstrip(' ').rstrip(' ')
                            ))
                            break
                    else:
                        self.__add_terminal(union_dict[j].lstrip(' ').rstrip(' '))

            rule_grammar = self.file.readline()
        self.union_dict = self.non_terminal + self.terminal
        self.__build_empty_table_relation()
        self.file.close()

    def is_non_terminal(self, part_grammar_rule):
        len_str = len(part_grammar_rule)
        if len_str > 0 and part_grammar_rule[0] == '<' and part_grammar_rule[len_str - 1] == '>':
            return True
        return False

    def __is_in_non_terminal_dict(self, part_grammar_rule):
        if part_grammar_rule not in self.non_terminal:
            return False
        return True

    def __add_non_terminal(self, non_terminal):
        if not self.__is_in_non_terminal_dict(non_terminal):
            self.non_terminal.append(non_terminal)

    def __is_in_terminal_dict(self, part_grammar_rule):
        if part_grammar_rule not in self.terminal:
            return False
        return True

    def __add_terminal(self, terminal):
        if not self.__is_in_terminal_dict(terminal):
            self.terminal.append(terminal)

    def __add_rule(self, parts_rule_grammar):
        self.rule_grammar[parts_rule_grammar[0].strip(' ')] = parts_rule_grammar[1].strip(' ').split('|')

    def __all_non_terminals(self):
        grammar = self.file.read()
        rules = grammar.split('\n')
        for i in range(len(rules)):
            if rules[i] != '':
                if self.is_non_terminal(rules[i].split('::=')[0].strip(' ')):
                    self.all_non_terminals.append(rules[i].split('::=')[0].strip(' '))
                else:
                    self.errors.append("We detected not non_terminal '{detected}'. Expected non_terminal.".format(
                        detected=rules[i].split('::=')[0].strip(' ')
                    ))
        self.file.seek(0)

    def get_parse_errors(self):
        return self.errors

    def __build_empty_table_relation(self):
        len_table = len(self.union_dict)
        for i in range(len_table):
            self.table_relation[self.union_dict[i]] = {}
            for j in range(len_table):
                self.table_relation[self.union_dict[i]][self.union_dict[j]] = 0