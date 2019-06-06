

from beautifultable import BeautifulTable

class Lexem(object):
    def __init__(self, serial_number = None, line_number = None, lexem = None, code_lexem = None, code_idn = None, code_con = None, code_label = None):
        self.serial_number = serial_number
        self.line_number = line_number
        self.lexem = lexem
        self.code_lexem = code_lexem
        self.code_idn = code_idn
        self.code_con = code_con
        self.code_label = code_label

    @staticmethod
    def add_lex(collection_records_lexem, line, lex, code, code_idn = None, code_con = None, code_label = None):
        collection_records_lexem.append(Lexem(len(collection_records_lexem) + 1,
                                                    line,
                                                    lex,
                                                    code,
                                                    code_idn,
                                                    code_con,
                                                    code_label))

    @staticmethod
    def get_number_line_for_lexem(collection_records_lexem, lexem):
        count_lexem = len(collection_records_lexem)
        for i in range(count_lexem):
            if collection_records_lexem[i].lexem == lexem:
                return collection_records_lexem[i].line_number
        return False

    @staticmethod
    def find_type_idn(collection_records_lex):
        index_last_lex = len(collection_records_lex) - 1
        while index_last_lex >= 0:
            if collection_records_lex[index_last_lex].lexem == 'tiger' or collection_records_lex[
                index_last_lex].lexem == 'int' or collection_records_lex[index_last_lex].lexem == 'float':
                return collection_records_lex[index_last_lex].lexem
            elif collection_records_lex[index_last_lex].lexem == ',':
                if collection_records_lex[index_last_lex - 1].code_lexem == 100:
                    index_last_lex -= 2
                    continue
                else:
                    return None
            else:
                return None

    @staticmethod
    def set_code_for_label(label, code_label, collection_records_lexem):
        count = len(collection_records_lexem)
        for i in range(count):
            if collection_records_lexem[i].lexem == label:
                collection_records_lexem[i].code_label = code_label


    @staticmethod
    def show_lexes(collection_records_lexem):
        count = len(collection_records_lexem)
        print(' ')
        print("---------------------------------------------------------------------------------------------------")
        print("|                                          Table tokens                                           |")
        print("---------------------------------------------------------------------------------------------------")
        print("|  serial_number  | line_number |      lexem     | code_lexem | code_idn | code_con |  code_label |")
        print("---------------------------------------------------------------------------------------------------")
        for i in range(0, count):
            print(
                "|       %-4i      |      %-3i    |     %-6s     |     %-3s    |    %-4s  |   %-4s   |     %-4s    |" % (
                collection_records_lexem[i].serial_number,
                collection_records_lexem[i].line_number,
                collection_records_lexem[i].lexem,
                collection_records_lexem[i].code_lexem,
                collection_records_lexem[i].code_idn,
                collection_records_lexem[i].code_con,
                collection_records_lexem[i].code_label))
            print("---------------------------------------------------------------------------------------------------")

    @staticmethod
    def __make_line() -> str:
        line = ''
        for i in range(213):
            line += '-'
        line += '\n'
        return line


    @staticmethod
    def table_lexes_to_string(collection_records_lexem) -> str:
        count = len(collection_records_lexem)
        if count > 0:
            table = BeautifulTable()
            table._max_table_width = 400
            table.column_headers = ["   №   ", "line number", "lexem", "code lexem", "code identifier", "code сonstant", "code label"]
            for i in range(0, count):
                table.append_row([collection_records_lexem[i].serial_number,
                                  collection_records_lexem[i].line_number,
                                  collection_records_lexem[i].lexem,
                                  collection_records_lexem[i].code_lexem,
                                  collection_records_lexem[i].code_idn,
                                  collection_records_lexem[i].code_con,
                                  collection_records_lexem[i].code_label])

            return str(table)
        return ''


