import sys

from . import unicodeit


if __name__ == "__main__":
    result = [unicodeit.replace(f) for f in sys.argv[1:]]

    def print_no_b(data):
        if not isinstance(data, str):
            data = data.decode()
        print(data)

    for r in result:
        print_no_b(r)
