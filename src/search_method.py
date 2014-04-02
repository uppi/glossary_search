# -*- coding: utf-8 -*-

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
import re, korean

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
    ending_rxstring_fin = u"{0}$".format(ending_rxstring)
    ending_rxstring_rich = u"({0})?".format(ending_rxstring)
    ending_regexp = re.compile(ending_rxstring_fin)

    @staticmethod
    def remove_endings(text):
        return u" ".join([MorphSearch.remove_ending(word) for word in text.split()])

    @staticmethod
    def remove_ending(word):
        word = word.replace("+", ".")
        word = word.replace(")", ".")
        word = word.replace("(", ".")
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
        #print "Making"
        prepared = MorphSearch.prepare_text(unicode(value))
        #print "Prepared:", prepared
        if prepared:
            try:
                if not rich:
                    return re.compile(prepared, re.U)
                else:
                    print "Rich."
                    value = unicode(value)
                    words = [MorphSearch.remove_ending(word) + MorphSearch.ending_rxstring_rich for word in value.split()]
                    try:
                        return re.compile(u" +".join(words))
                    except Exception as e:
                        print str(e)
                        print value
                        return None
            except Exception as e:
                print str(e)
                return None
        return None

if __name__ == "__main__":
    text = u"홀든은 자신의 임무는 끝났다고 말하며 셰넌에게 돌아가라고 말했다. 말하는 섬 마을 기초훈련장 앞에 있는 셰넌에게 돌아가 보고하자.\n"
    print text
    print MorphSearch.prepare_text(text)
