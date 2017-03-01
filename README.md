# Sudoku
A scalable sudoku solver, can be generalized to a solver for all constraint satisfaction problems.

## Author
[Chang Gao](http://www.linkedin.com/in/irsisyphus "linkedin")<br>
[Bruce Tan](http://halfer53.github.io/ "homepage")<br>
[Rimoun Ghaly](https://www.linkedin.com/in/rimoun-ghaly-41287b107/ "linkedin")<br>

## Usage
```
python main.py <input> <output> <timeout> <tokens>
```

1. `<input>`: Raw input file of sudoku problems, see `/ExampleSudokuFiles` for samples. We support different size of board, and upperCase letters.

2. `<output>`: Name and location of output file.

3. `<timeout>`: Maximum time of backtracking (in seconds).

4. `<tokens>`: Backtracking methods to use, we support:
 * `BT`: Default backtracking.
 * `FC`, `ACP`, `NKD`, `NKT`: Consistency checking methods to use. `FC` for Forward Checking, `ACP` for Arc Consistency, `NKD` for Naked Double, and `NKT` for Naked Triple. Cannot be used at the same time.
 * `MRV`, `DH`: Variable selection heuristic to use. `MRV` for Minimum Remaining Values, and `DH` for Degree Heuristic. Cannot be used at the same time.
 * `LCV`: Value selection heuristic to use. `LCV` for Least Constraining Value.

## Generate a new Sudoku puzzle
 ```
python problem_generator.py <input> <output>
```

The input file will consist of 4 numbers

M N P Q
  - M is the number of cells that will be initialized
  - N is the size of the NXN grid
  - P is the number of rows in each block
  - Q is the number of columns in each block

EXAMPLE: ```25 9 3 3```

## Default Testing
For default test on all solver options, you can simply type
```
python main.py
```
