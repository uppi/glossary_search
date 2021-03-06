import traceback, re
from .search_method import SearchMethod
class MorphSearch(SearchMethod):
    def __init__(self, endings):
        self.ending_rxstring = u"|".join([u"(?:{0})".format(x) for x in endings])
        self.ending_rxstring_fin = u"(?:{0})$".format(self.ending_rxstring)
        self.ending_rxstring_rich = u"({0})?".format(self.ending_rxstring)
        self.ending_regexp = re.compile(self.ending_rxstring_fin)

    def __stem_text(self, text):
        return u" ".join([self.__stem_word(word) for word in text.split()])

    def __stem_word(self, word):
        word = word.replace("+", " ")
        word = word.replace(")", " ")
        word = word.replace("(", " ")
        word = word.replace("*", " ")
        word = word.replace(".", " ")
        match = self.ending_regexp.search(word)
        if not match:
            return word
        else:
            return word[:-(len(match.group(0)))]

    def prepare_text(self, text):
        return self.__stem_text(text)

    def make_regex(self, value, rich=False):
        prepared = self.prepare_text(unicode(value))
        if prepared:
            try:
                if not rich:
                    return re.compile(prepared, re.U)
                else:
                    value = unicode(value)
                    words = [self.__stem_word(word) + self.ending_rxstring_rich for word in value.split()]
                    pattern = u" +".join(words)
                    return re.compile(pattern)
            except re.error:
                traceback.print_exc()
                return None
        return None
