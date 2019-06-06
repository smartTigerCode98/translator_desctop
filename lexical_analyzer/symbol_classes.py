
import re

class SymbolClasses(object):
   @staticmethod
   def white_separator(symbol):
       if symbol == ' ' or symbol == '\v' or symbol == '\t':
           return True
       return False

   @staticmethod
   def letter(symbol):
       if re.match(r'[a-z]', symbol):
           return True
       return False

   @staticmethod
   def number(symbol):
       if re.match(r'[0-9]', symbol):
           return True
       return False

   @staticmethod
   def plus(symbol):
       if re.match(r'[+-]', symbol):
           return True
       return False

   @staticmethod
   def dot(symbol):
       if symbol == '.':
           return True
       return False

   @staticmethod
   def single_character_splitters(symbol):
       if re.match(r'[,/*:;{}()]', symbol) or symbol == '\n':
           return True
       return False

   @staticmethod
   def less(symbol):
       if symbol == '<':
           return True
       return False

   @staticmethod
   def more(symbol):
       if symbol == '>':
           return True
       return False

   @staticmethod
   def equally(symbol):
       if symbol == '=':
           return True
       return False

   @staticmethod
   def exclamation(symbol):
       if symbol == '!':
           return True
       return False

   @staticmethod
   def dollar(symbol):
       if symbol == '$':
           return True
       return False


