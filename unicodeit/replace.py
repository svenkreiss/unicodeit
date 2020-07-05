# Copyright (c) 2010 Sven Kreiss, Kyle Cranmer
import re

from .data import REPLACEMENTS, COMBININGMARKS, SUBSUPERSCRIPTS


def replace(f: str):
    # escape combining marks with a space after the backslash
    for c in COMBININGMARKS:
        offset = 0
        for s in re.finditer(c[0], f):
            f = f[:s.start()+1+offset] + " " + f[s.start()+1+offset:]
            offset += 1

    for r in REPLACEMENTS:
        f = f.replace(r[0], r[1])

    # expand groups of subscripts: \_{01234}
    offset = 0
    #for s in re.finditer(r"\\_\{[^\}]+\}", f):
    for s in re.finditer(
            r"_\{[0-9\+-=\(\)<>\-aeoxjhklmnpstiruv"
            r"\u03B2\u03B3\u03C1\u03C6\u03C7]+\}", f):
        newstring, n = re.subn(
            r"([0-9\+-=\(\)<>\-aeoxjhklmnpstiruv"
            r"\u03B2\u03B3\u03C1\u03C6\u03C7])",
            r"_\1", s.group(0)[2:-1])
        f = f[:s.start()+offset] + newstring + f[s.end()+offset:]
        offset += n*2 - (n + 3)


    # expand groups of superscripts: \^{01234}
    offset = 0
    #for s in re.finditer(r"\\\^\{[^\}]+\}", f):
    for s in re.finditer(
            r"\^\{[0-9\+-=\(\)<>ABDEGHIJKLMNOPRTUW"
            r"abcdefghijklmnoprstuvwxyz"
            r"\u03B2\u03B3\u03B4\u03C6\u03C7\u222B]+\}", f):
        newstring, n = re.subn(
            r"([0-9\+-=\(\)<>ABDEGHIJKLMNOPRTUW"
            r"abcdefghijklmnoprstuvwxyz"
            r"\u03B2\u03B3\u03B4\u03C6\u03C7\u222B])",
            r"^\1", s.group(0)[2:-1])
        f = f[:s.start()+offset] + newstring + f[s.end()+offset:]
        offset += n*2 - (n + 3)

    # now replace subsuperscripts
    for r in SUBSUPERSCRIPTS:
        f = f.replace(r[0], r[1])

    # combining marks (unicode char modifies previous char)
    for c in COMBININGMARKS:
        offset = 0
        for s in re.finditer(r"\\ "+c[0][2:]+r"\{[^\}]+\}", f):
            newstring, n = re.subn(r"(.)", r"\1"+c[1], s.group(0)[len(c[0])+1:-1])
            f = f[:s.start()+offset] + newstring + f[s.end()+offset:]
            offset += n - (n + len(c[0])+1)

    return f.encode('utf-8')