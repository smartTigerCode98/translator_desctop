from syntactical_analyzer.input_automatic_row import InputAutomaticRow
from beautifultable import BeautifulTable
import json


class InputAutomaticTable(object):
    def __init__(self):
        self.table = []
        self.__initialization_table()

    def __initialization_table(self):
        file = open('C:\\Users\\UraN\\Desktop\\input_table.json')
        table = json.loads(file.read())
        file.close()
        len_table = len(table)
        for i in range(len_table):
            self.table.append(
                InputAutomaticRow(
                    alfa=table[i]["alfa"],
                    transition_label=table[i]["transition_label"],
                    beta=table[i]["beta"],
                    stack=table[i]["stack"],
                    semantic_subroutine=table[i]["semantic_subroutine"]
                )
            )

    def get_row(self, alfa):
        for i in range(len(self.table)):
            if self.table[i].alfa == alfa:
                return self.table[i]

    def input_table_to_string(self):
        count = len(self.table)
        if count > 0:
            table = BeautifulTable()
            table._max_table_width = 400
            table.column_headers = [" alfa ", "  transition label ", "  beta  ", " Stack ",
                                    "Semantic subroutine"]
            for i in range(0, count):
                semantic_subroutine = self.table[i].semantic_subroutine
                semantic_str = ''
                if semantic_subroutine.get('error'):
                    semantic_str += "[≠] error"
                else:
                    if semantic_subroutine.get('exit'):
                        semantic_str += "[≠] exit"
                    if semantic_subroutine.get('beta'):
                        semantic_str += "[≠] beta = {beta} ".format(beta=semantic_subroutine.get('beta'))
                        if semantic_subroutine.get('stack'):
                            semantic_str += "stack ↓ {stack}".format(stack=semantic_subroutine.get('stack'))
                table.append_row([self.table[i].alfa, to_str(self.table[i].transition_label),
                                  to_str(self.table[i].beta), to_str(self.table[i].stack),
                                  semantic_str])

            return str(table)
        return ''


def to_str(list):
    len_list = len(list)
    str1 = ''
    if len_list > 0:
        for i in range(len_list):
            str1 += str(list[i]) + ' '

    return str1
