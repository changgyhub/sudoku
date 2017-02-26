# sudoku
A scalable sudoku solver, can be generalized to a solver for all constraint satisfaction problems.

## Author
[Chang Gao](http://hk.linkedin.com/in/irsisyphus "linkedin")<br>
Bruce Tan<br>
Rimoun Ghaly

## Usage
`python3 main.py <input> <output> <timeout> <tokens>`

1. `<input>`: Raw input file of sudoku problems, see `/ExampleSudokuFiles` for samples. We support different size of board, and upperCase letters.

2. `<output>`: Name and location of output file.

3. `<timeout>`: Maximum time of backtracking (in seconds).

4. `<tokens>`: Backtracking methods to use, we support:
 * `BT`: Default backtracking.
 * `FC`, `ACP`, `NKT`: Consistency Checking Methods to use. `FC` for Forward Checking, `ACP` for Arc Consistency, and `NKT` for Naked Triple. Cannot be used at the same time.
 * `MRV`, `DH`: Variable Selection Heuristic to use. `MRV` for Minimum Remaining Values, and `DH` for Degree Heuristic. Cannot be used at the same time.
 * `LCV`: Value Selection Heuristic to use. `LCV` for Least Constraining Value.
