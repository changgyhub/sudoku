# Sudoku
A scalable sudoku solver with templates for all constraint satisfaction problems.

## Author
[Chang Gao](http://www.linkedin.com/in/irsisyphus "linkedin")<br>
[Bruce Tan](http://halfer53.github.io/ "homepage")<br>
[Rimoun Ghaly](https://www.linkedin.com/in/rimoun-ghaly-41287b107/ "linkedin")<br>

## Usage
```Bash
python main.py <input> <output> <timeout> <tokens>
```

1. `<input>`: Raw input file of sudoku problems, see `/ExampleSudokuFiles` for samples. For sudoku data, we support different size of board, with digits or/and upperCase letters.

2. `<output>`: Name and location of output file.

3. `<timeout>`: Maximum time of backtracking (in seconds).

4. `<tokens>`: Backtracking methods to use, we support:
 * `BT`: Default backtracking.
 * `FC, ACP, NKD, NKT`: Consistency checking methods to use. `FC` for Forward Checking, `ACP` for Arc Consistency, `NKD` for Naked Double, and `NKT` for Naked Triple. If multiple methods are set, they will be considered in order.
 * `MRV, DH`: Variable selection heuristic to use. `MRV` for Minimum Remaining Values, and `DH` for Degree Heuristic. We only support one heuristic at the same time.
 * `LCV`: Value selection heuristic to use. `LCV` for Least Constraining Value.

## Generate a new Sudoku puzzle
```Bash
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
```Bash
python main.py
```
You may customize your test in main.test()

## Note
Do not copy contents of this repo for course assignments. You should take the responsibility for any form of plagiarism.
