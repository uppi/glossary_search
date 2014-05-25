# -*- coding: utf-8 -*-

class SearchMethod(object):
    def prepare_text(self, text):
        raise NotImplementedError("Pure virtual method call")

    def make_regex(self, value, rich=False):
        raise NotImplementedError("Pure virtual method call")

if __name__ == "__main__":
    text = u"자이언트 윈디마"
    print text
    #print "prepared:", d.prepare_text(text)
    #print "rich:", self.make_regex(text, True).pattern


    #자이언((?:가)|(?:와)|(?:의)|(?:어게)|(?:는)|(?:께서)|(?:한테서)|(?:석)|(?:계)|(?:을)|(?:씨)|(?:은)|(?:아)|(?:께)|(?:에)|(?:님)|(?:한테)|(?:로)|(?:과)|(?:으로)|(?:에게서)|(?:여)|(?:에서)|(?:를)|(?:이)|(?:야))? +윈디마((?:가)|(?:와)|(?:의)|(?:어게)|(?:는)|(?:께서)|(?:한테서)|(?:석)|(?:계)|(?:을)|(?:씨)|(?:은)|(?:아)|(?:께)|(?:에)|(?:님)|(?:한테)|(?:로)|(?:과)|(?:으로)|(?:에게서)|(?:여)|(?:에서)|(?:를)|(?:이)|(?:야))?

