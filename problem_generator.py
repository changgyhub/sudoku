"""Problem Generator for Sudoku."""


# Rule 1: no row, column, or box can contain the same symbol more than once
# Randomly Select a cell. Try to assign a number. if the number violates
# the rule 1, do not assign it and erase that number from database.
import itertools
import random
from sys import argv


class UnassignableVariableException(Exception):

    def __init__(self, variable):
        self.variable = variable

    def __str__(self):
        return repr(self.variable)


def getRandomVariable(N, board):
    """
    Get an unassigned random position given the board.
    :param N: The edge length of the board
    :param board: The board
    :return: a random, unassigned position on the board
    """
    var = (random.randint(0, N - 1), random.randint(0, N - 1))
    while isAssigned(var, board):
        var = (random.randint(0, N - 1), random.randint(0, N - 1))
    return var


def assignValue(var, board, assignable, N, P, Q):
    """
    Attempt to assign a value in specified board position.

    :param var: The position on the board
    :param board:  The board
    :param assignable: The mapping of assignable values
    """
    conversion = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9,
                  10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F',
                  16: 'G', 17: 'H', 18: 'I', 19: 'J', 20: 'K', 21: 'L',
                  22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R',
                  28: 'S', 29: 'T', 30: 'U', 31: 'V', 32: 'W', 33: 'X',
                  34: 'Y', 35: 'Z'}
    # assign a possible value to a variable and update board and assignable
    random.shuffle(assignable[var])
    for val in assignable[var]:
        if isValidValue(var, conversion[val], board, N, P, Q):
            board[var] = conversion[val]
            assignable[var].remove(val)
            return
        assignable[var].remove(val)

    # No assignable value available
    raise UnassignableVariableException(var)


def isAssigned(var, board):
    return board[var] != 0


def isValidValue(var, val, board, N, P, Q):
    # check whether current value can be assigned to current variable
    return isValidColValue(var, val, board, N) \
        and isValidRowValue(var, val, board, N) \
        and isValidBlock(var, val, board, P, Q)


def isValidColValue(var, val, board, N):
    return val not in [board[(var[0], v)] for v in range(N) if v != var[1]]


def isValidRowValue(var, val, board, N):
    return val not in [board[(v, var[1])] for v in range(N) if v != var[0]]


def isValidBlock(var, val, board, P, Q):
    block_number = var[0] // P, var[1] // Q
    return val not in \
        [board[(i, j)]
         for i in range(P * block_number[0], P * block_number[0] + P)
         for j in range(Q * block_number[1], Q * block_number[1] + Q)
         if (i, j) != var]


def isBoardComplete(board, M, N):
    return M == len([(k1, k2) for (k1, k2) in itertools.product(
                                range(N), repeat=2) if board[(k1, k2)] != 0])


def printBoard(board, N):
    printed_board = ''
    for i in range(N):
        for j in range(N):
            printed_board += str(board[(i, j)])
            if j < N - 1:
                printed_board += " "
        printed_board += '\n'
    return printed_board


def createAssignable(N):
    """Create a mapping of assignable values given a variable."""
    assignable = {}
    # possible values to assign in each cell of the sudoku board
    for (k1, k2) in itertools.product(range(N), repeat=2):
        assignable[(k1, k2)] = list(range(1, N + 1))
    return assignable


def createBoard(N):
    """Create a board initialized with zero elements."""
    board = {}
    for (k1, k2) in itertools.product(range(N), repeat=2):
        board[(k1, k2)] = 0
    return board


def populateBoard(M, N, P, Q):
    board = None
    while not board:
        assignable = createAssignable(N)
        board = createBoard(N)

        try:
            while not isBoardComplete(board, M, N):
                var = getRandomVariable(N, board)
                assignValue(var, board, assignable, N, P, Q)

            return board
        except UnassignableVariableException as e:
            board = None


def readInput(inputFilename):
    with open(inputFilename, 'r') as f:
        line = f.readline()
        try:
            M, N, P, Q = map(int, line.rstrip().split(" "))

            # Validate input constraints
            if M > N ** 2:
                print("Invalid input constraint: M > N^2 where " +
                      "M={}, N={}".format(M, N))
                exit(-1)

            if P * Q != N:
                print("Invalid input constraint: P * Q == N where " +
                      "P={}, Q={}, N={}".format(P, Q, N))
                exit(-1)

            return M, N, P, Q
        except ValueError as e:
            print("Invalid input format: " +
                  "<{}>. Expected <M N P Q>.".format(line))
            exit(-1)


def writeOutput(outputFilename, N, P, Q, board):
    with open(outputFilename, 'w') as f:
        f.write("{0} {1} {2}\n".format(N, P, Q))
        f.write(printBoard(board, N))


def parseCommandLineArguments():
    if len(argv) != 3:
        print("Insufficient number of arguments. " +
              "Usage: python3 problem_generator.py input-file output-file")
        exit(-1)

    inputFilename = argv[1]
    outputFilename = argv[2]
    return inputFilename, outputFilename


def main():
    inputFilename, outputFilename = parseCommandLineArguments()
    M, N, P, Q = readInput(inputFilename)
    board = populateBoard(M, N, P, Q)
    writeOutput(outputFilename, N, P, Q, board)
    print("Successfully generated a Monster Sudoku problem in <{0}>".format(
        outputFilename))


if __name__ == '__main__':
    main()
