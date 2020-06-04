import subprocess
import pytest


def test_cli_symbols1():
    r = subprocess.check_output([
        'python', '-m', 'unicodeit.cli',
        '\\Sigma'
    ])
    print(r.decode())
    assert r.decode() == 'Σ\n'


def test_cli_symbols2():
    r = subprocess.check_output([
        'python', '-m', 'unicodeit.cli',
        'def\\Sigma_{01234}abc\\alpha_{567}ggg\\beta_{1234}lll "\\Sigma e_0 e^3"'
    ])
    print(r.decode())
    assert r.decode() == 'defΣ₀₁₂₃₄abcα₅₆₇gggβ₁₂₃₄lll "Σ e₀ e³"\n'


def test_cli_symbols3():
    r = subprocess.check_output([
        'python', '-m', 'unicodeit.cli',
        'def^{01234}abc\\alpha^{567abc} "\\:) \\:G"'
    ])
    print(r.decode())
    assert r.decode() == 'def⁰¹²³⁴abcα⁵⁶⁷ᵃᵇᶜ "☺ ㋡"\n'


@pytest.mark.skip('this was already broken')
def test_cli_symbols4():
    r = subprocess.check_output([
        'python', '-m', 'unicodeit.cli',
        'ggg\\beta^{1234=\\(5\\)}lll'
    ])
    print(r.decode())
    assert r.decode() == 'Σ\n'


def test_subscripts():
    r = subprocess.check_output([
        'python', '-m', 'unicodeit.cli',
        'a_{\\beta\\gamma\\phi\\rho\\chi}'
    ])
    print(r.decode())
    assert r.decode() == 'aᵦᵧᵩᵨᵪ\n'


def test_superscripts():
    r = subprocess.check_output([
        'python', '-m', 'unicodeit.cli',
        'm^{ABDEGHIJKLMNOPRTUWabcdefghiklmnoprstuvwxyz\\beta\\gamma\\delta\\phi\\chi<>}'
    ])
    print(r.decode())
    assert r.decode() == 'mᴬᴮᴰᴱᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᴿᵀᵁᵂᵃᵇᶜᵈᵉᶠᵍʰⁱᵏˡᵐⁿᵒᵖʳˢᵗᵘᵛʷˣʸᶻᵝᵞᵟᵠᵡ˂˃\n'
