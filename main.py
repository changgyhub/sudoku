"""Main for Sudoku Solver."""

import os
import sys
import signal
import filereader
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

    if len(sys.argv) < 4:
        print("Program did not received enough correct argument.")
        print("Start Preset Testing.")
        test()
        return

    # GB = gameboard.GameBoard(
    #      12,3,4,[[0 for j in range(12)] for i in range(12)])
    # print(GB)

    TOTAL_START = time.time()
    sudokudata = filereader.SudokuFileReader(sys.argv[1])
    print(sudokudata)
    # cn = filereader.GameBoardToConstraintNetwork(sudokudata)
    # print(cn)
    solver = btsolver.BTSolver(sudokudata)
    tokens = sys.argv[4:]
    solver.setTokens(tokens)

    if len(sys.argv) == 4 or sys.argv[4] == 'BT':
        print("Default option tokens detected: Backtracking Search (BT)")

    if 'FC' in tokens:
        print("FC/ACP/NKD/NKT token detected: Forward Checking (FC)")
        solver.setConsistencyChecks(
            btsolver.ConsistencyCheck['ForwardChecking'])
    elif 'ACP' in tokens:
        print("FC/ACP/NKD/NKT token detected: Arc Consistency (ACP)")
        solver.setConsistencyChecks(
            btsolver.ConsistencyCheck['ArcConsistency'])
    elif 'NKD' in tokens:
        print("FC/ACP/NKD/NKT token detected: Naked Double (NKD)")
        solver.setConsistencyChecks(
            btsolver.ConsistencyCheck['NKD'])
    elif 'NKT' in tokens:
        print("FC/ACP/NKD/NKT token detected: Naked Triple (NKT)")
        solver.setConsistencyChecks(
            btsolver.ConsistencyCheck['NKT'])

    if 'MRV' in tokens:
        print("MRV/DH token detected: Minimum Remaining Values (MRV)")
        solver.setVariableSelectionHeuristic(
            btsolver.VariableSelectionHeuristic['MRV'])
    elif 'DH' in tokens:
        print("MRV/DH token detected: Degree Heuristic (DH)")
        solver.setVariableSelectionHeuristic(
            btsolver.VariableSelectionHeuristic['DH'])

    if 'LCV' in tokens:
        print("LCV token detected: Least Constraining Value (LCV)")
        solver.setValueSelectionHeuristic(
            btsolver.ValueSelectionHeuristic['LCV'])

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

    # return solver.endTime - solver.startTime


def test():
    for root, dirs, files in os.walk("ExampleSudokuFiles/"):
        for name in files:
            if name == 'PE1.txt':
            # if name.endswith('.txt'):
                sudokudata = filereader.SudokuFileReader(
                                            "ExampleSudokuFiles/" + name)
                for ConsisChk in [None, 'ForwardChecking',
                                  'ArcConsistency', 'NKD', 'NKT']:
                    for VarH in [None, 'MRV', 'DH']:
                        for ValH in [None, 'LCV']:
                            solver = btsolver.BTSolver(sudokudata)
                            if ConsisChk is not None:
                                solver.setConsistencyChecks(
                                    btsolver.ConsistencyCheck[ConsisChk])
                            if VarH is not None:
                                solver.setVariableSelectionHeuristic(
                                     btsolver.VariableSelectionHeuristic[VarH])
                            if ValH is not None:
                                solver.setValueSelectionHeuristic(
                                    btsolver.ValueSelectionHeuristic[ValH])
                            print(name, ConsisChk, VarH, ValH,
                                  solver.solve(), 's')


if __name__ == '__main__':
    main()
