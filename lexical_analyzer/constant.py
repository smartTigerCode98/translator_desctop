from beautifultable import BeautifulTable

class Constant(object):
    def __init__(self, code = None, name = None, type = None):
        self.code = code
        self.name = name
        self.type = type


    @staticmethod
    def add_con(collection_records_con, code, name, type):
        collection_records_con.append(Constant(code, name, type))


    @staticmethod
    def type_con(con):
        if con.find('.') != -1:
            return 'float'
        return 'int'

    @staticmethod
    def show_con(collection_records_con):
        count = len(collection_records_con)
        print(' ')
        print("---------------------------------------------")
        print("|             Constant table                |")
        print("---------------------------------------------")
        print("|  code  |         name        |    type    |")
        print("---------------------------------------------")
        for i in range(0, count):
            print("|   %-4i |         %-8s    |    %-5s   |" % (collection_records_con[i].code,
                                                                collection_records_con[i].name,
                                                                collection_records_con[i].type))
            print("---------------------------------------------")

    @staticmethod
    def table_lexes_to_string(collection_records_con) -> str:
        print('tyt')
        count = len(collection_records_con)
        print(count)
        if count > 0:
            table = BeautifulTable()
            table._max_table_width = 400
            table.column_headers = ["       Constant code        ", "       Constant name      ",
                                    "        Constant type        "]
            for i in range(0, count):
                table.append_row([collection_records_con[i].code,
                                  collection_records_con[i].name,
                                  collection_records_con[i].type])

            return str(table)
        return ' '