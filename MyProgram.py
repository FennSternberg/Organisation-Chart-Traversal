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
        sys.exit(0)

    input_path, name_a, name_b = argv
    org = Organization(input_path)
    matches_a = org.find_employee_ids_by_name(name_a)
    matches_b = org.find_employee_ids_by_name(name_b)

    # later implment user interaction to select among multiple matches
    a_id = matches_a[0]
    b_id = matches_b[0]

    fmt = org.format_path_between(a_id, b_id)
    print(fmt)