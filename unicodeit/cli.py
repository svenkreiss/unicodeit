import sys

from .replace import replace


if __name__ == "__main__":
    result = [replace(f) for f in sys.argv[1:]]

    def print_no_b(data):
        if not isinstance(data, str):
            data = data.decode()
        print(data)

    for r in result:
        print_no_b(r)
