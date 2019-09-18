# Copyright (c) 2010 Sven Kreiss, Kyle Cranmer
from __future__ import unicode_literals
__author__ = "Sven Kreiss <sk@svenkreiss.com>, Kyle Cranmer <kyle.cranmer@nyu.edu>"
__version__ = "0.6.2"
import sys, re
import six

replacements = []
combiningmarks = []
subsuperscripts = []


def replace(inp):
    result = []
    for f in inp:
        f = f.decode("utf-8")
        
        #f = re.sub(r"([^\\])([_|\^])", r"\1\\\2", f) # do not require backslash in front of ^ or _
        #f = re.sub(r"^([_|\^])", r"\\\1", f)
        
        # escape combining marks with a space after the backslash
        for c in combiningmarks:
            offset = 0
            for s in re.finditer(c[0], f):
                f = f[:s.start()+1+offset] + " " + f[s.start()+1+offset:]
                offset += 1
            
        for r in replacements:
            f = re.sub(r[0], r[1], f)

        # expand groups of subscripts: \_{01234}    
        offset = 0
        #for s in re.finditer(r"\\_\{[^\}]+\}", f):
        for s in re.finditer(r"_\{[0-9\+-=\(\)<>\-aeoxjhklmnpstiruv\u03B2\u03B3\u03C1\u03C6\u03C7]+\}", f):
            newstring,n = re.subn(r"([0-9\+-=\(\)<>\-aeoxjhklmnpstiruv\u03B2\u03B3\u03C1\u03C6\u03C7])", r"_\1", s.group(0)[2:-1])
            f = f[:s.start()+offset] + newstring + f[s.end()+offset:]
            offset += n*2 - (n + 3)
            
            
        # expand groups of superscripts: \^{01234}    
        offset = 0
        #for s in re.finditer(r"\\\^\{[^\}]+\}", f):
        for s in re.finditer(r"\^\{[0-9\+-=\(\)<>ABDEGHIJKLMNOPRTUWabcdefghijklmnoprstuvwxyz\u03B2\u03B3\u03B4\u03C6\u03C7\u222B]+\}", f):
            newstring,n = re.subn(r"([0-9\+-=\(\)<>ABDEGHIJKLMNOPRTUWabcdefghijklmnoprstuvwxyz\u03B2\u03B3\u03B4\u03C6\u03C7\u222B])", r"^\1", s.group(0)[2:-1])
            f = f[:s.start()+offset] + newstring + f[s.end()+offset:]
            offset += n*2 - (n + 3)
        
        # now replace subsuperscripts
        for r in subsuperscripts:
            f = re.sub(r[0], r[1], f)

        # combining marks (unicode char modifies previous char)
        for c in combiningmarks:
            offset = 0
            for s in re.finditer(r"\\ "+c[0][2:]+r"\{[^\}]+\}", f):
                newstring,n = re.subn(r"(.)", r"\1"+c[1], s.group(0)[len(c[0])+1:-1])
                f = f[:s.start()+offset] + newstring + f[s.end()+offset:]
                offset += n - (n + len(c[0])+1)

        result.append( six.text_type(f).encode("utf-8") )
                
    return result


if __name__ == "__main__":
    result = replace(sys.argv[1:])
    def print_no_b(data):
        if not isinstance(data, str):
            data = data.decode()
        print(data)
    for r in result: print_no_b(r)
