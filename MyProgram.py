import sys
from src.organization import Organization
from src.visualize import ascii_forest

def print_usage():
    msg = (
        "Usage:\n"
        "  python MyProgram.py <input.txt> \"Name A\" \"Name B\"\n"
        "  python MyProgram.py --visualize <input.txt>\n"
    )
    sys.stderr.write(msg)

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    
    if not argv or argv[0] in {"-h", "--help"}:
        print_usage()
        return 0
    
    if argv[0] == "--visualize":
        if len(argv) != 2:
            print_usage()
            return 2
        input_path = argv[1]
        input_path = argv[1]
        org = Organization(input_path)
        for line in ascii_forest(org):
            try:
                print(line)
            except UnicodeEncodeError:
                # Fallback if unable to render characters
                safe = (
                    line.replace("├", "+")
                    .replace("└", "+")
                    .replace("│", "|")
                    .replace("─", "-")
                )
                print(safe)
        return 0
    
    if len(argv) != 3:
        print_usage()
        return 2

    input_path, name_a, name_b = argv
    org = Organization(input_path)

    def choose_id(label:str, name:str, matches:list[int]) -> int:
        if len(matches) < 2:
            return matches[0]
        print(f"Multiple matches found for '{name}'. Please choose by employee ID:")
        
        for eid in matches:
            print(org.format_label(eid))
        
        valid = set(matches)
        while True:
            try:
                print(f"Enter the employee ID for the {label} person:")
                sel = input().strip()
                choice = int(sel)
            except ValueError:
                print("Please enter a valid numeric employee ID.")
                continue
            if choice in valid:
                return choice
            print("Invalid selection. Valid IDs:", ", ".join(str(x) for x in sorted(valid)))

    matches_a = org.find_employee_ids_by_name(name_a)
    matches_b = org.find_employee_ids_by_name(name_b)

    if not matches_a:
        sys.stderr.write(f"No employees found matching '{name_a}'.\n")
        return 1
    
    if not matches_b:
        sys.stderr.write(f"No employees found matching '{name_b}'.\n")
        return 1

    # select among multiple matches
    a_id = choose_id("first", name_a, matches_a)
    b_id = choose_id("second", name_b, matches_b)

    fmt = org.format_path_between(a_id, b_id)
    print(fmt)
    return 0

if __name__ == "__main__":
    sys.exit(main())