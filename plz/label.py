
class Label(object):
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    @staticmethod
    def find_label(label_table, name):
        count_label = len(label_table)
        for i in range(count_label):
            if label_table[i].name == name:
                return label_table[i]
        return None
