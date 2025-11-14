# Organisation-Chart-Traversal

This repository implements a command-line program for for Superheroes Inc, an old-fashioned company which has very strict rules about only passing information up and down the
management chain. Given details of the organisational chart and the names of two people, it prints out the names of all the people in the chain between them.

## Requirements

- Python 3.13.9 or later
- No non-standard libraries required
  
## Usage

- Find a path between two names:

  `python MyProgram.py <input.txt> "Name A" "Name B"`

  Example:

  `python MyProgram.py tests/test_inputs/superheroes.txt "Batman" "Super Ted"`

  Output:

  `Batman (16) -> Black Widow (6) -> Gonzo the Great (2) -> Dangermouse (1) <- Invisible Woman (3) <- Super Ted (15)`

- Visualize the hierarchy as an ASCII tree:

  `python MyProgram.py --visualize <input.txt>`

  Example:

  `python MyProgram.py --visualize python MyProgram.py tests/test_inputs/superheroes.txt`

  Output:

```text
Dangermouse (1)
├── Gonzo the Great (2)
│   └── Black Widow (6)
│       ├── Batman (16)
│       └── Catwoman (17)
└── Invisible Woman (3)
    ├── Hit Girl (12)
    └── Super Ted (15)
```
## Input Format

The program expects a pipe-separated table:

```text
| Employee ID | Name            | Manager ID |
| 1           | Dangermouse     |            |
| 2           | Gonzo the Great | 1          |
| 3           | Invisible Woman | 1          |
| 6           | Black Widow     | 2          |
| 12          | Hit Girl        | 3          |
| 15          | Super Ted       | 3          |
| 16          | Batman          | 6          |
| 17          | Catwoman        | 6          |
```

- The header row is required.
- `Employee ID` and `Manager ID` are integers
- `Manager ID` may be blank for root(s)
- Any columns not labelled with `Employee ID`, `Manager ID` or `Name` will be ignored
- Rows may appear in any order
- Columns may appear in any order
- Non-table lines will be ignored
- Lines without an employee Id will be ignored
- Duplicate `Employee ID`s are not allowed, and an error will be raised if they exist in the input file
- Cyclic management chains will raise an error

## Behavior and Rules

- Name comparisons ignore case, leading/trailing spaces, and runs of multiple spaces.
- If either name matches more than one employee (duplicate names), the program interactively prompts you to choose the intended employee by entering their `employee ID`. It displays all matching `ID - Name` options from the input file before prompting.
- The path formatting shows direction relative to the first name:
  - `->` moves upward (employee to manager)
  - `<-` moves downward (manager to subordinate)

## Running Tests

This project uses the standard library `unittest` module.

`python -m unittest discover -s tests -p "test_*.py" -v`

## File Layout

- `MyProgram.py` — CLI entry point.
- `src/organization.py` — Input file parsing, and path finding/formatting.
- `src/visualize.py` — ASCII tree printer for the organization chart.
- `tests/` — Unit tests
- `tests/test_inputs` - Test input files
