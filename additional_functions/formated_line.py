
class Formated(object):

    @staticmethod
    def formated(line, width):
        len_line = len(line)
        if len_line <= width:
            new_line = ''
            difference_in_len = width - len_line
            left_indent = round(difference_in_len / 2)
            right_indent = difference_in_len - left_indent
            for i in range(left_indent):
                new_line += ' '
            new_line += line
            for i in range(right_indent):
                new_line += ' '
            print(len(new_line))
            return new_line
        else:
            return False