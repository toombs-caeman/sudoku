a very rough sudoku solver in python

This solver represents the board as an array 9-bit bitfields, representing the *potential values* that could be contained in each cell.

Row, column, and block constraints are propagated whenever cells are collapsed to a single value by reducing the potential field of adjacent cells, which may trigger further propagation.

When constraint propagation ends, the solver can guess the remaining cells, backtracking whenever a guess results in a contradiction.
Guessing is technically unnecessary as puzzles are supposed to have a single solution, however more complicated inference would be necessary. Guessing is succinct and sufficiently fast.

# Future Ideas
* re-write in various languages and test relative performance
* write fully logical implementation (no guessing/backtracking), perf test
    *
* [generate puzzles with unique solutions](https://stackoverflow.com/questions/6924216/how-to-generate-sudoku-boards-with-unique-solutions)
* interactive TUI
    * [example game](https://www.linuxlinks.com/nudoku/)
    * [termcolor](https://pypi.org/project/termcolor/)
* other puzzle solvers
    * allow varied grid size/shape
    * [kakuro](https://en.wikipedia.org/wiki/Kakuro)
# reference
* https://sandiway.arizona.edu/sudoku/index.html#heuristics
