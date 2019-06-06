class SyntacticalExceptions(object):
    def __init__(self):
        self.msg = []

    def add_exeption(self, msg):
        self.msg.append('Syntactical errors number {number}: '.format(number = len(self.msg) + 1) + msg)

    def get_errors(self):
        return self.msg