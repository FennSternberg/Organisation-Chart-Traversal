import sys
from src.organisation import Organization

if __name__ == "__main__":
    argv = sys.argv[1:]
    if argv is None:
        argv = sys.argv[1:]

    input_path, name_a, name_b = argv
    org = Organization(input_path)