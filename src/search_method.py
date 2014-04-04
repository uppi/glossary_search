# -*- coding: utf-8 -*-

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
import traceback, re
import korean

class DefaultSearch(object):
    @staticmethod
    def prepare_text(text):
        return text

    @staticmethod
    def make_one_word_regex_part(word, rich=False):
        result = "(?:(?:^)|[ .+-])" + re.escape(word)
        if len(word) != 1:
            result += "?"
        if rich:
            return "(" + result + "[^ ]?" + ")"
        else:
            return result + "[^ ]?"

    @staticmethod
    def make_regex(value, rich=False):
        value = unicode(value)
        words = value.split()
        if words:
            return re.compile(u' *'.join(DefaultSearch.make_one_word_regex_part(word, rich) for word in words), re.U) 
        return None

class MorphSearch(object):
    ending_rxstring = u"|".join([u"(?:{0})".format(x) for x in korean.noun_endings])
    ending_rxstring_fin = u"(?:{0})$".format(ending_rxstring)
    ending_rxstring_rich = u"({0})?".format(ending_rxstring)
    ending_regexp = re.compile(ending_rxstring_fin)

    @staticmethod
    def remove_endings(text):
        return u" ".join([MorphSearch.remove_ending(word) for word in text.split()])

    @staticmethod
    def remove_ending(word):
        word = word.replace("+", " ")
        word = word.replace(")", " ")
        word = word.replace("(", " ")
        word = word.replace("*", " ")
        word = word.replace(".", " ")
        mo = MorphSearch.ending_regexp.search(word)
        if not mo:
            return word
        else:
            return word[:-(len(mo.group(0)))]

    @staticmethod
    def prepare_text(text):
        return MorphSearch.remove_endings(text)

    @staticmethod
    def make_regex(value, rich=False):
        prepared = MorphSearch.prepare_text(unicode(value))
        if prepared:
            try:
                if not rich:
                    return re.compile(prepared, re.U)
                else:
                    value = unicode(value)
                    words = [MorphSearch.remove_ending(word) + MorphSearch.ending_rxstring_rich for word in value.split()]
                    pattern = u" +".join(words)
                    try:
                        return re.compile(pattern)
                    except Exception as e:
                        traceback.print_exc()
                        return None
            except Exception as e:
                traceback.print_exc()
                return None
        return None

if __name__ == "__main__":
    text = u"자이언트 윈디마"
    print text
    print "prepared:", MorphSearch.prepare_text(text)
    print "rich:", MorphSearch.make_regex(text, True).pattern


    #자이언((?:가)|(?:와)|(?:의)|(?:어게)|(?:는)|(?:께서)|(?:한테서)|(?:석)|(?:계)|(?:을)|(?:씨)|(?:은)|(?:아)|(?:께)|(?:에)|(?:님)|(?:한테)|(?:로)|(?:과)|(?:으로)|(?:에게서)|(?:여)|(?:에서)|(?:를)|(?:이)|(?:야))? +윈디마((?:가)|(?:와)|(?:의)|(?:어게)|(?:는)|(?:께서)|(?:한테서)|(?:석)|(?:계)|(?:을)|(?:씨)|(?:은)|(?:아)|(?:께)|(?:에)|(?:님)|(?:한테)|(?:로)|(?:과)|(?:으로)|(?:에게서)|(?:여)|(?:에서)|(?:를)|(?:이)|(?:야))?

