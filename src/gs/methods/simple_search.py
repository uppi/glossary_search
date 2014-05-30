# -*- coding: utf-8 -*-

import re
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
        value = value.replace("+", " ")
        value = value.replace(")", " ")
        value = value.replace("(", " ")
        value = value.replace("*", " ")
        value = value.replace(".", " ")
        value = value.replace("-", " ")
        value = value.replace(u"．", " ")
        words = value.split()
        if words:
            parts = [self.__make_one_word_regex_part(word, rich) for word in words]
            full = u' *'.join(parts)
            if len(words) > 1:
                any_word = u'|'.join((u"(?:" + part + u")" for part in parts))
                result_string = u'(?:' + full + u')|(?:' + any_word + u')'
                return re.compile(u'(?:' + full + u')|(?:' + any_word + u')', re.U)
            else:
                return re.compile(full, re.U)
        return None


def test():
    s = u'凱瑟琳．班'
    r = SimpleSearch().make_regex(s)
    r.search("凱瑟琳")

if __name__ == '__main__':
    test()