# -*- coding: utf-8 -*-

noun_endings = [x for x in set([u"석", u"계", u"이", u"가", u"은", u"는", u"께서", u"의", u"을", u"를", u"어게", u"한테", u"에", u"께", u"에게서", u"한테서", u"로", u"으로", u"야", u"아", u"여", u"님", u"께서", u"씨", u"에게서", u"에서", u"에", u"와", u"과", u"와", u"과"])]


# cut the endings while preprocessing, also cut them in the searching text.
# for highlighting make rich regexps with (|||)