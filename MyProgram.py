import sys
from src.organization import Organization
from src.visualize import ascii_forest
if __name__ == "__main__":
    argv = sys.argv[1:]
    if argv is None:
        argv = sys.argv[1:]
    
    if argv[0] == "--visualize":
        input_path = argv[1]
        org = Organization(input_path)
        for line in ascii_forest(org):
            print(line)
        
        sys.exit(0)

    input_path, name_a, name_b = argv
    org = Organization(input_path)