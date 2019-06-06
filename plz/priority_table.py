class PriorityTable(object):
    def __init__(self):
        self.priority_table = {
            0: {'(', '{', 'if', 'repeat', 'start'},
            1: {')', '}', 'or', 'until', 'finish', 'goto', '\\n', ':', 'int', 'float', 'cin', 'echo'},
            2: {'='},
            3: {'and'},
            4: {'not'},
            5: {'<', '>', '<=', '>=', '==', '!='},
            6: {'+', '-'},
            7: {'*', '/'}
        }

    def get_priority(self, lex):
        for key, value in self.priority_table.items():
            if lex in value:
                return key
        return False
