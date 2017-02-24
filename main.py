"""Main for Sudoku Solver."""

import sys
import signal
import gameboard
import filereader
import constraint
import constraintnetwork
import btsolver
import time


def signal_handler(signum, frame):
    """Limit excution time of a function call."""
    raise Exception("Timed out!")


def printSolverStats(solverObj, totalStart, isTimeOut):
    output = "TOTAL_START=" + str(time.asctime(time.localtime(totalStart)))

    if solverObj.preprocessing_startTime != 0:
        output += "\nPREPROCESSING_START=" + str(time.asctime(
                  time.localtime(solverObj.preprocessing_startTime)))
        output += "\nPREPROCESSING_DONE=" + str(time.asctime(
                  time.localtime(solverObj.preprocessing_endTime)))
    else:
        output += "\nPREPROCESSING_START=0"
        output += "\nPREPROCESSING_DONE=0"

    # print(str(solverObj.endTime) +'              '+ str(solverObj.startTime))
    # solverObj.startTime = solverObj.endTime - 1
    output += "\nSEARCH_START=" + \
        str(time.asctime(time.localtime(solverObj.startTime)))
    output += "\nSEARCH_DONE=" + \
        str(time.asctime(time.localtime(solverObj.endTime)))
    output += "\nSOLUTION_TIME=%.7f" % (
        (solverObj.preprocessing_endTime - solverObj.preprocessing_startTime)
        + (solverObj.endTime - solverObj.startTime))
    if isTimeOut:
        output += "\nSTATUS=timeout"
    elif solverObj.hassolution:
        output += "\nSTATUS=success"
    else:
        output += "\nSTATUS=error"

    # print(self.gameboard.board)
    output += "\nSOLUTION=("
    for i in solverObj.gameboard.board:
        for j in i:
            output += str(j) + ","
    output = output[:-1]
    output += ")"

    output += "\nCOUNT_NODES=" + str(solverObj.numAssignments)
    output += "\nCOUNT_DEADENDS=" + str(solverObj.numBacktracks)
    output += "\n" + str(solverObj.gameboard)

    return output


def main():
    # Check command-line arguments.
    print('Python version:', sys.version)

    # GB = gameboard.GameBoard(
    #      12,3,4,[[0 for j in range(12)] for i in range(12)])
    # print(GB)

    TOTAL_START = time.time()
    sudokudata = filereader.SudokuFileReader(sys.argv[1])
    print(sudokudata)
    # cn = filereader.GameBoardToConstraintNetwork(sudokudata)
    # print(cn)
    solver = btsolver.BTSolver(sudokudata)

    # three examples of how you would change the various aspects of solver
    # solver.setConsistencyChecks(btsolver.ConsistencyCheck['None'])
    # solver.setValueSelectionHeuristic(btsolver.ValueSelectionHeuristic['None'])
    # solver.setVariableSelectionHeuristic(btsolver.VariableSelectionHeuristic['None'])
    tokens = sys.argv[4:]
    solver.setTokens(tokens)

    '''once you have implemented more heuristics,
       you can add the appropriate lines to this conditional clause'''
    if len(sys.argv) < 4:
        raise ValueError("Program did not received enough correct argument.")
    elif len(sys.argv) == 4 or sys.argv[4] == 'BT':
        print("Default option tokens detected: Backtracking Search (BT)")
    elif sys.argv[4] == 'FC':
        print("FC tokens detected:  Forward Checking (FC)")
        solver.setConsistencyChecks(
            btsolver.ConsistencyCheck['ForwardChecking'])
    else:
        print("Default option tokens detected: something else ...")

    if 'FC' in tokens:
        solver.setConsistencyChecks(
            btsolver.ConsistencyCheck['ForwardChecking'])
    elif 'ACP' in tokens:
        solver.setConsistencyChecks(
            btsolver.ConsistencyCheck['ArcConsistency'])

    if 'MRV' in tokens:
        solver.setVariableSelectionHeuristic(
            btsolver.VariableSelectionHeuristic['MRV'])
    elif 'DH' in tokens:
        solver.setVariableSelectionHeuristic(
            btsolver.VariableSelectionHeuristic['DH'])

    if 'LCV' in tokens:
        solver.setValueSelectionHeuristic(
            btsolver.ValueSelectionHeuristic['LCV'])

    if 'NKT' in tokens:
        solver.setConsistencyChecks(btsolver.ConsistencyCheck['NKT'])

    isTimeOut = False
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(int(sys.argv[3]))
    try:
        solver.solve()
    except IndexError:
        isTimeOut = True
        solver.endTime = time.time()
        print("Timed out by " + sys.argv[3] + " seconds !!!")

    print(printSolverStats(solver, TOTAL_START, isTimeOut))

    with open(sys.argv[2], "w") as outfile:
        outfile.write(printSolverStats(solver, TOTAL_START, isTimeOut))


if __name__ == '__main__':
    main()
