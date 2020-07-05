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
