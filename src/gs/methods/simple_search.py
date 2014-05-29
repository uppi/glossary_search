import traceback, re
from .search_method import SearchMethod

class SimpleSearch(SearchMethod):
    def prepare_text(self, text):
        return text

    @staticmethod
    def __make_one_word_regex_part(word, rich=False):
        result = re.escape(word)
        if rich:
            return "(" + result + ")"
        else:
            return result

    def make_regex(self, value, rich=False):
        value = unicode(value)
        words = value.split()
        if words:
            return re.compile(u' *'.join(self.__make_one_word_regex_part(word, rich) for word in words), re.U) 
        return None