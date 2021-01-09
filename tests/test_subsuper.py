import unicodeit


def test_superscript_12():
    assert unicodeit.replace('a^{12}') == 'a¹²'


def test_superscript_minus1():
    assert unicodeit.replace('cm^{-1}') == 'cm⁻¹'


def test_subscript_12():
    assert unicodeit.replace('a_{12}') == 'a₁₂'


def test_subscript_minus1():
    assert unicodeit.replace('cm_{-1}') == 'cm₋₁'
