
#
# test case:
# python unicodeit.py \\Sigma def\\Sigma_{01234}abc\\alpha_{567}ggg\\beta_{1234}lll "\\Sigma e_0 e^3" def^{01234}abc\\alpha^{567abc}ggg\\beta^{1234=\(5\)}lll "\\:) \\:G"
# python unicodeit.py a_{\\beta\\gamma\\phi\\rho\\chi} b_{aeox} c_{hklmnpst} d_j
# python unicodeit.py "m^{ABDEGHIJKLMNOPRTUWabcdefghiklmnoprstuvwxyz\beta\gamma\delta\phi\chi<>}"
#

import re
from xml.etree import ElementTree as ET

nodes = ET.parse('ent.xml').getroot()

replacements = {}

def addSymbols(replacements):
    #isoent
    for n in nodes:
        if(n.tag == 'char'):
            unicode = ''
            latex = ''
            
            unicodeElement = n.find('unicode')
            if unicodeElement is not None:
                if unicodeElement.attrib.has_key('value'):
                    unicode = unicodeElement.attrib['value']
            
            latexElement = n.find('latex/seq') 
            if latexElement is not None:
                latex = latexElement.text
                    
            latexElement = n.find('latex/mathseq') 
            if latexElement is not None:
                latex = latexElement.text
                
            # remove elements of the form "\^{A}" and "\_{A}"
            if len(latex) == 5 and latex[2] == "{" and latex[4] == "}":
                continue
    
            #  and latex.find('{') == -1 and latex.find('}') == -1
            if unicode and latex and latex[0] == '\\' and latex.find('\\',1) == -1 and latex != "\\backslash":
                replacements[latex] = unicode
                
    # alias
    replacements["\\to"] = "2192"

    # other symbols    
    replacements["\\degree"] = "00B0"
    replacements["\\star"] = "002A"
    replacements["\\sqrt"] = "221A"
    replacements["\\sqrt[3]"] = "221B"
    replacements["\\sqrt[4]"] = "221C"
    replacements["\\neq"] = "2260"
    replacements["\\ne"] = "2260"
                

#def addSubSuper(replacements):
#    # sub- and superscript replacements from http://en.wikipedia.org/wiki/Unicode_subscripts_and_superscripts
#    # ascii part from http://www.w3schools.com/tags/ref_entities.asp
#
#    # subscripts
#    for i in range(10): replacements["\\_"+str(i)] = "208"+str(i)
#    replacements["\\_+"] = "208A"
#    replacements["\\_-"] = "208B"
#    replacements["\\_="] = "208C"
#    replacements["\\_("] = "208D"
#    replacements["\\_)"] = "208E"
#    # superscripts
#    replacements["\\^0"] = "2070"
#    replacements["\\^1"] = "00B9"#"20B9"
#    replacements["\\^2"] = "00B2"#"20B2"
#    replacements["\\^3"] = "00B3"#"20B3"
#    replacements["\\^4"] = "2074"
#    replacements["\\^5"] = "2075"
#    replacements["\\^6"] = "2076"
#    replacements["\\^7"] = "2077"
#    replacements["\\^8"] = "2078"
#    replacements["\\^9"] = "2079"
#    replacements["\\^+"] = "207A"
#    replacements["\\^-"] = "207B"
#    replacements["\\^="] = "207C"
#    replacements["\\^("] = "207D"
#    replacements["\\^)"] = "207E"
#    replacements["\\^n"] = "207F"
#    replacements["\\^i"] = "2071"
#    replacements["\\^*"] = "002A"
    
def addSubSuperNoSlash(replacements):
    # sub- and superscript replacements from http://en.wikipedia.org/wiki/Unicode_subscripts_and_superscripts
    # ascii part from http://www.w3schools.com/tags/ref_entities.asp

    # subscripts
    for i in range(10): replacements["_"+str(i)] = "208"+str(i)
    replacements["_+"] = "208A"
    replacements["_-"] = "208B"
    replacements["_="] = "208C"
    replacements["_("] = "208D"
    replacements["_)"] = "208E"
    replacements["_<"] = "02F1"
    replacements["_>"] = "02F2"
    replacements["_a"] = "2090"
    replacements["_e"] = "2091"
    replacements["_o"] = "2092"
    replacements["_x"] = "2093"
    replacements["_j"] = "2C7C"
    replacements["_h"] = "2095"
    replacements["_k"] = "2096"
    replacements["_l"] = "2097"
    replacements["_m"] = "2098"
    replacements["_n"] = "2099"
    replacements["_p"] = "209A"
    replacements["_s"] = "209B"
    replacements["_t"] = "209C"
    replacements["_i"] = "1D62"
    replacements["_r"] = "1D63"
    replacements["_u"] = "1D64"
    replacements["_v"] = "1D65"
    replacements["_\u03B2"] = "1D66" #beta
    replacements["_\u03B3"] = "1D67" #gamma
    replacements["_\u03C1"] = "1D68" #rho
    replacements["_\u03C6"] = "1D69" #phi
    replacements["_\u03C7"] = "1D6A" #chi
    
    # superscripts
    replacements["^0"] = "2070"
    replacements["^1"] = "00B9"#"20B9"
    replacements["^2"] = "00B2"#"20B2"
    replacements["^3"] = "00B3"#"20B3"
    replacements["^4"] = "2074"
    replacements["^5"] = "2075"
    replacements["^6"] = "2076"
    replacements["^7"] = "2077"
    replacements["^8"] = "2078"
    replacements["^9"] = "2079"
    replacements["^+"] = "207A"
    replacements["^-"] = "207B"
    replacements["^="] = "207C"
    replacements["^("] = "207D"
    replacements["^)"] = "207E"
    replacements["^*"] = "002A"
    replacements["^<"] = "02C2"
    replacements["^>"] = "02C3"
    
    # from http://en.wikipedia.org/wiki/Phonetic_symbols_in_Unicode
    # and there are a couple of more signs, that are not added yet
    replacements["^A"] = "1D2C"
    replacements["^B"] = "1D2E"
    replacements["^D"] = "1D30"
    replacements["^E"] = "1D31"
    replacements["^G"] = "1D33"
    replacements["^H"] = "1D34"
    replacements["^I"] = "1D35"
    replacements["^J"] = "1D36"
    replacements["^K"] = "1D37"
    replacements["^L"] = "1D38"
    replacements["^M"] = "1D39"
    replacements["^N"] = "1D3A"
    replacements["^O"] = "1D3C"
    replacements["^P"] = "1D3E"
    replacements["^R"] = "1D3F"
    replacements["^T"] = "1D40"
    replacements["^U"] = "1D41"
    replacements["^V"] = "1111"
    replacements["^W"] = "1D42"

    # from: http://en.wikipedia.org/wiki/Subscript_and_superscript
    replacements["^a"] = "1D43"
    replacements["^b"] = "1D47"
    replacements["^c"] = "1D9C"
    replacements["^d"] = "1D48"
    replacements["^e"] = "1D49"
    replacements["^f"] = "1DA0"
    replacements["^g"] = "1D4D"
    replacements["^h"] = "02B0"
    replacements["^i"] = "2071"
    replacements["^j"] = "02B2"
    replacements["^k"] = "1D4F"
    replacements["^l"] = "02E1"
    replacements["^m"] = "1D50"
    replacements["^n"] = "207F"
    replacements["^o"] = "1D52"
    replacements["^p"] = "1D56"
    replacements["^r"] = "02B3"
    replacements["^s"] = "02E2"
    replacements["^t"] = "1D57"
    replacements["^u"] = "1D58"
    replacements["^v"] = "1D5B"
    replacements["^w"] = "02B7"
    replacements["^x"] = "02E3"
    replacements["^y"] = "02B8"
    replacements["^z"] = "1DBB"
    
    replacements["^\u03B2"] = "1D5D" #beta
    replacements["^\u03B3"] = "1D5E" #gamma
    replacements["^\u03B4"] = "1D5F" #delta
    replacements["^\u03C6"] = "1D60" #phi
    replacements["^\u03C7"] = "1D61" #chi
    replacements["^\u222B"] = "1DB4" #int


    
def addEmoticons(replacements):
    replacements["\\smile"] = "263A"
    replacements["\\:)"] = "263A"
    replacements["\\sad"] = "2639"
    replacements["\\:("] = "2639"
    replacements["\\happy"] = "32E1"
    replacements["\\:G"] = "32E1"
    
def addMathLetterlike(replacements):
    replacements["\\h"] = "210E"
    replacements["\\i"] = "2139"
    replacements["\\estimated"] = "212E"
    replacements["\\mathbb{R}"] = "211D"
    replacements["\\mathbb{C}"] = "2102"
    replacements["\\mathbb{N}"] = "2115"
    replacements["\\mathbb{P}"] = "2119"
    replacements["\\mathbb{Q}"] = "211A"
    replacements["\\mathbb{Z}"] = "2124"
    replacements["\\mathbb{D}"] = "2145"
    replacements["\\mathbb{d}"] = "2146"
    replacements["\\mathbb{e}"] = "2147"
    replacements["\\mathbb{i}"] = "2148"
    replacements["\\mathbb{j}"] = "2149"
    replacements["\\mathbb{H}"] = "210D"
    replacements["\\mathbb{R}"] = "211D"
    replacements["\\mathbb{gamma}"] = "213D"
    replacements["\\mathbb{Gamma}"] = "213E"
    replacements["\\mathbb{Pi}"] = "213F"
    replacements["\\mathcal{L}"] = "2112"
    replacements["\\mathcal{M}"] = "2133"
    replacements["\\mathcal{H}"] = "210B"
    replacements["\\mathcal{B}"] = "212C"
    replacements["\\mathcal{I}"] = "2111"
    replacements["\\mathcal{R}"] = "211B"
    replacements["\\mathcal{e}"] = "212F"
    replacements["\\mathcal{E}"] = "2130"
    replacements["\\mathcal{g}"] = "210A"

def addCombiningMarks(replacements):
    # combining diacritical marks
    replacements["\\vec"] = "20D7"

    replacements["\\grave"] = "0300"
    replacements["\\acute"] = "0301"
    replacements["\\hat"] = "0302"
    replacements["\\tilde"] = "0303"
    replacements["\\overline"] = "0305"
    replacements["\\bar"] = "0305"
    replacements["\\breve"] = "0306"
    replacements["\\dot"] = "0307"
    replacements["\\ddot"] = "0308"
    replacements["\\underline"] = "0332"
    replacements["\\doubleunderline"] = "0333"
    replacements["\\strikethrough"] = "0335"
    replacements["\\slash"] = "0338"
    

addSymbols(replacements)
#addSubSuperNoSlash(replacements) # handled separately, do not add here
addEmoticons(replacements)
addMathLetterlike(replacements)
#addCombiningMarks(replacements) # handled separately, do not add here

#print replacements

replacements = replacements.items()

def sortRule(i):
    return -len(i[0])
replacements = sorted(replacements, key=sortRule)

def escapeAll(i):
    escape = ['\\', '.', '^', '$', '*', '+', '?', '{', '}', '[', ']', '|', '(', ')', '\''] # backslash must be first
    l = i
    
    for e in escape:
        l = l.replace(e, '\\'+e)
    #undo escaped unicode \u
    l = re.sub(r'\\\\u([0-9A-Fa-f]{4})', r'\\u\1', l)
    
    return l

# write python converter script
template = open("template.py", "r")
out = open("unicodeit.py", "w")
for t in template:
    if t[:12] == "replacements":
        out.write("replacements = [\n")
        for l,u in replacements:
            l = escapeAll(l)
            out.write("    (ur'"+l+"', u'\\u"+u+"'),\n")
        out.write("]\n")
    elif t[:14] == "combiningmarks":
        combiningmarks = {}
        addCombiningMarks(combiningmarks)
        out.write("combiningmarks = [\n")
        for l,u in combiningmarks.items():
            l = escapeAll(l)
            out.write("    (ur'"+l+"', u'\\u"+u+"'),\n")
        out.write("]\n")
    elif t[:15] == "subsuperscripts":
        subsuperscripts = {}
        addSubSuperNoSlash(subsuperscripts)
        out.write("subsuperscripts = [\n")
        for l,u in subsuperscripts.items():
            l = escapeAll(l)
            out.write("    (ur'"+l+"', u'\\u"+u+"'),\n")
        out.write("]\n")
    else:
        out.write(t)

# write js converter script
template = open("template.js", "r")
out = open("unicodeit.js", "w")
for t in template:
    if t[:16] == "var replacements":
        out.write("var replacements = [\n")
        for l,u in replacements:
            l = escapeAll(l)
            out.write("    ['"+l+"', '\\u"+u+"'],\n")
        out.write("];\n")
    elif t[:18] == "var combiningmarks":
        combiningmarks = {}
        addCombiningMarks(combiningmarks)
        out.write("var combiningmarks = [\n")
        for l,u in combiningmarks.items():
            l = escapeAll(l)
            out.write("    ['"+l+"', '\\u"+u+"'],\n")
        out.write("];\n")
    elif t[:19] == "var subsuperscripts":
        subsuperscripts = {}
        addSubSuperNoSlash(subsuperscripts)
        out.write("var subsuperscripts = [\n")
        for l,u in subsuperscripts.items():
            l = escapeAll(l)
            out.write("    ['"+l+"', '\\u"+u+"'],\n")
        out.write("];\n")
    else:
        out.write(t)

print "No of replacements: %d" % (len(replacements)+len(combiningmarks)+len(subsuperscripts))



# list all replacements
def nicePrint(i):
    return i[0]
def printFromFunction(f):    
    r = {}
    f(r)
    r = r.items()
    r = sorted(r, key=nicePrint)
    for l,u in r:
        if l == "_\u03B2": l = "_{\\beta}"
        if l == "_\u03B3": l = "_{\\gamma}"
        if l == "_\u03C1": l = "_{\\rho}"
        if l == "_\u03C6": l = "_{\\phi}"
        if l == "_\u03C7": l = "_{\\chi}"
        print "%20s  \t %s" % (l, unichr(int(u, 16)).encode("utf-8"))
def jsonFromFunctions(functions):    
    r = {}
    for f in functions:
        f(r)
    r = r.items()
    #r = sorted(r, key=nicePrint)
    for l,u in r:
        if l == "_\u03B2": l = "_{\\beta}"
        if l == "_\u03B3": l = "_{\\gamma}"
        if l == "_\u03C1": l = "_{\\rho}"
        if l == "_\u03C6": l = "_{\\phi}"
        if l == "_\u03C7": l = "_{\\chi}"
        
        #print '"%s %s",' % (l, unichr(int(u, 16)).encode("utf-8")),
        if len(re.split('"',l)) > 1: continue
        if len(re.split("'",l)) > 1: continue
        if l[0]=="\\"  and  len(l) <= 2: continue
        print '"%s",' % (escapeAll(l)),
    
print "Sub- and Superscripts"
print "=============================="
printFromFunction(addSubSuperNoSlash)
print ""
print "Letterlike Symbols"
print "=============================="
printFromFunction(addMathLetterlike)
print ""
print "Emoticons"
print "=============================="
printFromFunction(addEmoticons)
print ""
print "Combining Marks"
print "=============================="
printFromFunction(addCombiningMarks)
print ""
print "Symbols"
print "=============================="
printFromFunction(addSymbols)


print ""
print "JSON"
print "=============================="
jsonFromFunctions([addSymbols,addSubSuperNoSlash,addMathLetterlike,addEmoticons,addCombiningMarks])

