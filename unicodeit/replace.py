# Copyright (c) 2010 Sven Kreiss, Kyle Cranmer
import re

from .data import REPLACEMENTS, COMBININGMARKS, SUBSUPERSCRIPTS


def replace(f: str):
    # Catch cases like \not\subset and \not\in and convert them to
    # use the combining character slash as in \slash{\subset}
    f = re.sub(r'\\not(\\[A-z]+)', r'\\slash{\1}', f)
    # escape combining marks with a space after the backslash
    for c in COMBININGMARKS:
        f = f.replace(c[0] + '{', '\\ ' + c[0][1:] + '{')

    # replace
    for r in REPLACEMENTS:
        f = f.replace(r[0], r[1])

        # check whether it was escaped for combining marks but has empty braces
        if r[0].endswith('{}'):
            f = f.replace('\\ ' + r[0][1:], r[1])

    # expand groups of subscripts: \_{01234}
    offset = 0
    for s in re.finditer(
            r"_\{[0-9\+-=\(\)<>\-aeoxjhklmnpstiruv"
            r"\u03B2\u03B3\u03C1\u03C6\u03C7\u2212]+\}", f):
        newstring, n = re.subn(
            r"([0-9\+-=\(\)<>\-aeoxjhklmnpstiruv"
            r"\u03B2\u03B3\u03C1\u03C6\u03C7\u2212])",
            r"_\1", s.group(0)[2:-1])
        f = f[:s.start() + offset] + newstring + f[s.end() + offset:]
        offset += n * 2 - (n + 3)

    # expand groups of superscripts: \^{01234}
    offset = 0
    for s in re.finditer(
            r"\^\{[0-9\+-=\(\)<>ABDEGHIJKLMNOPRTUW"
            r"abcdefghijklmnoprstuvwxyz"
            r"\u03B2\u03B3\u03B4\u03C6\u03C7\u222B\u2212]+\}", f):
        newstring, n = re.subn(
            r"([0-9\+-=\(\)<>ABDEGHIJKLMNOPRTUW"
            r"abcdefghijklmnoprstuvwxyz"
            r"\u03B2\u03B3\u03B4\u03C6\u03C7\u222B\u2212])",
            r"^\1", s.group(0)[2:-1])
        f = f[:s.start() + offset] + newstring + f[s.end() + offset:]
        offset += n * 2 - (n + 3)

    # now replace subsuperscripts
    for r in SUBSUPERSCRIPTS:
        f = f.replace(r[0], r[1])

    # process combining marks first
    for c in COMBININGMARKS:
        escaped_latex = f'\\ {c[0][1:]}{{'
        while escaped_latex in f:
            i = f.index(escaped_latex)
            if len(f) <= i + len(escaped_latex):
                # incomplete: unescape and continue
                f = f[:i] + c[0] + '{'
                continue

            combined_char = f[i + len(escaped_latex)]

            remainder = ''
            if len(f) >= i + len(escaped_latex) + 2:
                remainder = f[i + len(escaped_latex) + 2:]

            f = f[:i] + combined_char + c[1] + remainder

    return f
