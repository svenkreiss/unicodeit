import sys

from .replace import replace


if __name__ == "__main__":
    result = [replace(f) for f in sys.argv[1:]]
    print(' '.join(result))
