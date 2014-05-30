# -*- coding: utf-8 -*-

class SearchMethod(object):
    def prepare_text(self, text):
        raise NotImplementedError("Pure virtual method call")

    def make_regex(self, value, rich=False):
        raise NotImplementedError("Pure virtual method call")
