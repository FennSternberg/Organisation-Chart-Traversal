# Organisation-Chart-Traversal

This repository implements a command-line program for for Superheroes Inc, an old-fashioned company which has very strict rules about only passing information up and down the
management chain. Given details of the organisational chart and the names of two people, it prints out the names of all the people in the chain between them.

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
- `Employee ID` and `Manager ID` are integers; `Manager ID` may be blank for root(s).
- Rows may appear in any order
- Non uniqueness of names is tolerated, but further user input will be requested if non-uniqueness leads to amiguity in the communication path.
