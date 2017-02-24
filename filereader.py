"""File Reader for CSP."""


from math import floor

import constraint
import constraintnetwork
import gameboard
import variable

ODOMETERTOINT = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
                 "7": 7, "8": 8, "9": 9, "A": 10, "B": 11, "C": 12, "D": 13,
                 "E": 14, "F": 15, "G": 16, "H": 17, "I": 18, "J": 19, "K": 20,
                 "L": 21, "M": 22, "N": 23, "O": 24, "P": 25, "Q": 26, "R": 27,
                 "S": 28, "T": 29, "U": 30, "V": 31, "W": 32, "X": 33, "Y": 34,
                 "Z": 35}


def SudokuFileReader(filePath):
    """Read from input file and generate gameboard."""
    with open(filePath) as f:
        lines = f.readlines()

        if len(lines) == 0:
            raise ValueError("Input file \"" + filePath + "\" was empty")
        elif len(lines) < int(lines[0].split()[0]) + 1:
            raise ValueError("Incomplete or Emtpy board for file \""
                             + filePath + "\".Please be advised.")
        else:
            board = []
            for i in range(len(lines)):
                if i == 0:
                    checkGameBoardParameters(lines[i])
                    N = int(lines[i].split()[0])
                    p = int(lines[i].split()[1])
                    q = int(lines[i].split()[2])
                else:
                    tempLine = []
                    for n in lines[i].split():
                        # print(num)
                        # print(type(num)
                        tempLine.append(ODOMETERTOINT[n])
                    board.append(tempLine)

            return gameboard.GameBoard(N, p, q, board)

# --------- HELPER FUNTION ---------


def checkGameBoardParameters(params):
    if len(params.split()) != 3:
        raise ValueError("Params invalid in file.")


def GameBoardToConstraintNetwork(gb):
    board = gb.board
    variables = []
    value = 0
    for i in range(gb.N):
        for j in range(gb.N):
            value = board[i][j]
            domain = []
            if value == 0:
                d = 1
                while d <= gb.N:
                    domain.append(d)
                    d += 1
            else:
                domain.append(value)

            block = int(((floor(i / gb.p) * gb.p) + floor(j / gb.q)))
            variables.append(variable.Variable(domain, i, j, block))

    rows = dict()
    cols = dict()
    blocks = dict()

    for v in variables:
        row = v.row
        col = v.col
        block = v.block

        if not (row in rows.keys()):
            rows[row] = []
        if not (col in cols.keys()):
            cols[col] = []
        if not (block in blocks.keys()):
            blocks[block] = []

        rows[row].append(v)
        cols[col].append(v)
        blocks[block].append(v)

    cn = constraintnetwork.ConstraintNetwork()
    for v in variables:
        cn.addVariable(v)

    for e in rows:
        c = constraint.Constraint()
        for v in rows[e]:
            c.addVariable(v)
        cn.addConstraint(c)

    for e in cols:
        c = constraint.Constraint()
        for v in cols[e]:
            c.addVariable(v)
        cn.addConstraint(c)

    for e in blocks:
        c = constraint.Constraint()
        for v in blocks[e]:
            c.addVariable(v)
        cn.addConstraint(c)

    return cn


def ConstraintNetworkToGameBoard(cn, n, p, q):
        # gb = gameboard.GameBoard()
    board = [[0 for j in range(n)] for i in range(n)]
    row = 0
    col = 0
    for v in cn.variables:
        board[row][col] = v.getAssignment()
        col += 1
        if col == n:
            col = 0
            row += 1
    # gb.board = board
    # gb.N = n
    # gb.p = p
    # gb.q = q
    return gameboard.GameBoard(n, p, q, board)
