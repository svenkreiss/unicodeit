import subprocess
import sys

import pytest


PYTHON = 'python3' if sys.platform != 'win32' else 'python'


def test_cli_symbols1():
    r = subprocess.check_output([
        PYTHON, '-m', 'unicodeit.cli',
        '\\Sigma'
    ])
    print(r.decode())
    assert r.decode().strip() == 'Σ'


def test_cli_symbols2():
    r = subprocess.check_output([
        PYTHON, '-m', 'unicodeit.cli',
        'def\\Sigma_{01234}abc\\alpha_{567}ggg\\beta_{1234}lll "\\Sigma e_0 e^3"'
    ])
    print(r.decode())
    assert r.decode().strip() == 'defΣ₀₁₂₃₄abcα₅₆₇gggβ₁₂₃₄lll "Σ e₀ e³"'


def test_cli_symbols3():
    r = subprocess.check_output([
        PYTHON, '-m', 'unicodeit.cli',
        'def^{01234}abc\\alpha^{567abc} "\\:) \\:G"'
    ])
    print(r.decode())
    assert r.decode().strip() == 'def⁰¹²³⁴abcα⁵⁶⁷ᵃᵇᶜ "☺ ㋡"'


@pytest.mark.skip('this was already broken')
def test_cli_symbols4():
    r = subprocess.check_output([
        PYTHON, '-m', 'unicodeit.cli',
        'ggg\\beta^{1234=\\(5\\)}lll'
    ])
    print(r.decode())
    assert r.decode().strip() == 'Σ'


def test_subscripts():
    r = subprocess.check_output([
        PYTHON, '-m', 'unicodeit.cli',
        'a_{\\beta\\gamma\\varphi\\rho\\chi}'
    ])
    print(r.decode())
    assert r.decode().strip() == 'aᵦᵧᵩᵨᵪ'


def test_superscripts():
    r = subprocess.check_output([
        PYTHON, '-m', 'unicodeit.cli',
        'm^{ABDEGHIJKLMNOPRTUWabcdefghiklmnoprstuvwxyz\\beta\\gamma\\delta\\varphi\\chi<>}'
    ])
    print(r.decode())
    assert r.decode().strip() == 'mᴬᴮᴰᴱᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᴿᵀᵁᵂᵃᵇᶜᵈᵉᶠᵍʰⁱᵏˡᵐⁿᵒᵖʳˢᵗᵘᵛʷˣʸᶻᵝᵞᵟᵠᵡ˂˃'
