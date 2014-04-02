# -*- coding: utf-8 -*-

noun_endings = [x for x in set(["이", "가", "은", "는", "께서", "의", "을", "를", "어게", "한테", "에", "께", "에게서", "한테서", "로", "으로", "야", "아", "여", "님", "께서", "씨", "에게서", "에서", "에", "와", "과", "와", "과"])]
print len(noun_endings)


# cut the endings while preprocessing, also cut them in the searching text.
# for highlighting make rich regexps with (|||)