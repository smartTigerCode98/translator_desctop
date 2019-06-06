from beautifultable import BeautifulTable

class Identifier(object):

    def __init__(self, code=None, name=None, type=None, value=None):
        self.code = code
        self.name = name
        self.type = type
        self.value = value

    @staticmethod
    def get_value(collection_records_idn, name_value):
        count_val = len(collection_records_idn)
        for i in range(0, count_val):
            if collection_records_idn[i].name == name_value:
                return collection_records_idn[i].value
        return None

    @staticmethod
    def set_value(collection_records_idn, name_value, value):
        count_val = len(collection_records_idn)
        for i in range(0, count_val):
            if collection_records_idn[i].name == name_value:
                collection_records_idn[i].value = value
                break

    @staticmethod
    def add_idn(collection_records_idn, code, name, type):
        collection_records_idn.append(Identifier(code, name, type))


    @staticmethod
    def find_idn(idn, collection_records_idn):
        count = len(collection_records_idn)
        for i in range(0, count):
            if collection_records_idn[i].name == idn:
                return collection_records_idn[i].code
        return None


    @staticmethod
    def show_idn(collection_records_idn):
        count = len(collection_records_idn)
        print(' ')
        print("---------------------------------------------")
        print("|            Table of identifier            |")
        print("---------------------------------------------")
        print("|  code  |         name        |    type    |")
        print("---------------------------------------------")
        for i in range(0, count):
            print("|   %-4i |         %-8s    |    %-5s   |" % (collection_records_idn[i].code,
                                                                collection_records_idn[i].name,
                                                                collection_records_idn[i].type))
            print("---------------------------------------------")

    @staticmethod
    def table_lexes_to_string(collection_records_idn) -> str:
        count = len(collection_records_idn)
        if count > 0:
            table = BeautifulTable()
            table._max_table_width = 400
            table.column_headers = ["           ID code            ", "          ID name         ",
                                    "          ID value          "]
            for i in range(0, count):
                table.append_row([collection_records_idn[i].code,
                                  collection_records_idn[i].name,
                                  collection_records_idn[i].value])

            return str(table)
        return ''