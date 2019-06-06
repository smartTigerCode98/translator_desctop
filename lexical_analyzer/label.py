from beautifultable import BeautifulTable


class Label(object):

    def __init__(self, code = None, name = None):
        self.code = code
        self.name = name

    @staticmethod
    def add_label(collection_records_label, code, name):
        collection_records_label.append(Label(code, name))

    @staticmethod
    def find_label(label, collection_records_label):
        count = len(collection_records_label)
        for i in range(0, count):
            if collection_records_label[i].name == label:
                return collection_records_label[i].code
        return None

    @staticmethod
    def find_not_defined_label(label, collection_records_label):
        count = len(collection_records_label)
        for i in range(0, count):
            if collection_records_label[i].name == label:
                return i
        return None

    @staticmethod
    def show_label(collection_records_label):
        count = len(collection_records_label)
        print(' ')
        print("--------------------------------")
        print("|          Label table         |")
        print("--------------------------------")
        print("|  code  |         name        |")
        print("--------------------------------")
        for i in range(0, count):
            print("|   %-4i |       %-8s      |" % (collection_records_label[i].code, collection_records_label[i].name))
            print("-------------------------------")

    @staticmethod
    def table_lexes_to_string(collection_records_label) -> str:
        count = len(collection_records_label)
        if count > 0:
            table = BeautifulTable()
            table._max_table_width = 400
            table.column_headers = ["                Label code                 ",
                                    "                Label name               "]
            for i in range(0, count):
                table.append_row([collection_records_label[i].code,
                                  collection_records_label[i].name])

            return str(table)
        return ''

