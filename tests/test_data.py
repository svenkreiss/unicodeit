import unicodeit


def test_order_replacements():
    expr_length = float('inf')
    for l, _ in unicodeit.data.REPLACEMENTS:
        assert len(l) <= expr_length
        expr_length = len(l)


def test_order_subsuperscripts():
    expr_length = float('inf')
    for l, _ in unicodeit.data.SUBSUPERSCRIPTS:
        assert len(l) <= expr_length
        expr_length = len(l)


def test_order_combiningmarks():
    expr_length = float('inf')
    for l, _ in unicodeit.data.COMBININGMARKS:
        assert len(l) <= expr_length
        expr_length = len(l)


def test_combining_not_in_replacement():
    replacement_latex = {l.replace('{}', ''): u for l, u in unicodeit.data.REPLACEMENTS}
    for l, u in unicodeit.data.COMBININGMARKS:
        l = l.replace('{}', '')
        if l not in replacement_latex:
            continue

        # if the same command is in "replacements",
        # it must not be the combining mark
        assert replacement_latex[l] != u


def test_incomplete_combiningmark():
    assert unicodeit.replace('\\breve{') == '\\breve{'
