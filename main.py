"""Main for Sudoku Solver."""

import os
import sys
import filereader
import btsolver
import signal
import time
from itertools import permutations
from heapq import heappush, heappop


def signal_handler(signum, frame):
    """Limit excution time of a function call."""
    raise Exception("Timed out!")


def printSolverStats(solverObj, totalStart, isTimeOut):

    def getHouseString(hindex):
        if hindex >= solverObj.blockhouseoffset:
            return "Block " + str(hindex - solverObj.blockhouseoffset + 1)
        elif hindex >= solverObj.colhouseoffset:
            return "Column "+str(hindex - solverObj.colhouseoffset + 1)
        else:
            return "Row " + str(hindex + 1)

    def checkCorrectness():
        n = solverObj.gameboard.N
        targetval = (n*(n+1))/2
        for hindex, house in enumerate(solverObj.houses):
            dic = {}
            sum = 0
            for cell in house:
                if cell.isAssigned():
                    val = cell.getAssignment()
                    sum += val
                    if dic.get(val) == 1:
                        return "Duplicate value " + str(val) +\
                               " at " + getHouseString(hindex)
                    else:
                        dic[val] = 1
                else:
                    return " Value is not assigned at " + cell
            if sum != targetval:
                return "Inconsistent Value at " + getHouseString(hindex)
        return "Correct Result"

    output = "TOTAL_START=" + str(time.asctime(time.localtime(totalStart)))

    if solverObj.preprocessing_startTime != 0:
        output += "\nPREPROCESSING_START=" + str(time.asctime(
                  time.localtime(solverObj.preprocessing_startTime)))
        output += "\nPREPROCESSING_DONE=" + str(time.asctime(
                  time.localtime(solverObj.preprocessing_endTime)))
    else:
        output += "\nPREPROCESSING_START=0"
        output += "\nPREPROCESSING_DONE=0"

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

    output += "\nSOLUTION=("
    for i in solverObj.gameboard.board:
        for j in i:
            output += str(j) + ","
    output = output[:-1]
    output += ")"

    output += "\nCOUNT_NODES=" + str(solverObj.numAssignments)
    output += "\nCOUNT_DEADENDS=" + str(solverObj.numBacktracks)
    output += "\n" + str(solverObj.gameboard)

    if not isTimeOut:
        output += "\n"+checkCorrectness()
    else:
        output += "\nCorrectness Unchecked Due to Exception."

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

    for method in tokens:
        if method == 'FC':
            print("FC/ACP/NKD/NKT token detected: Forward Checking (FC)")
            solver.setConsistencyChecks(
                btsolver.ConsistencyCheck['ForwardChecking'])
        elif method == 'ACP':
            print("FC/ACP/NKD/NKT token detected: Arc Consistency (ACP)")
            solver.setConsistencyChecks(
                btsolver.ConsistencyCheck['ArcConsistency'])
        elif method == 'NKD':
            print("FC/ACP/NKD/NKT token detected: Naked Double (NKD)")
            solver.setConsistencyChecks(
                btsolver.ConsistencyCheck['NKD'])
        elif method == 'NKT':
            print("FC/ACP/NKD/NKT token detected: Naked Triple (NKT)")
            solver.setConsistencyChecks(
                btsolver.ConsistencyCheck['NKT'])
        elif method == 'MRV':
            print("MRV/DH token detected: Minimum Remaining Values (MRV)")
            solver.setVariableSelectionHeuristic(
                btsolver.VariableSelectionHeuristic['MRV'])
        elif method == 'DH':
            print("MRV/DH token detected: Degree Heuristic (DH)")
            solver.setVariableSelectionHeuristic(
                btsolver.VariableSelectionHeuristic['DH'])
        elif method == 'LCV':
            print("LCV token detected: Least Constraining Value (LCV)")
            solver.setValueSelectionHeuristic(
                btsolver.ValueSelectionHeuristic['LCV'])

    isTimeOut = False
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(int(sys.argv[3]))
    try:
        solver.solve()
        signal.alarm(0)  # cancel alarm
    except Exception:
        isTimeOut = True
        solver.endTime = time.time()
        print("Timed out by " + sys.argv[3] + " seconds !!!")

    print(printSolverStats(solver, TOTAL_START, isTimeOut))

    with open(sys.argv[2], "w") as outfile:
        outfile.write(printSolverStats(solver, TOTAL_START, isTimeOut))


def test():
    """
    Test Function for Solver.

    Recommanded configuration:
    -------------------------------
    numTest | difficulty | timeout
    -------------------------------
       20   |    'E'     |  30/60
        5   |    'M'     |  60/120
        1   |    'H'     | 300/600
    -------------------------------
    """
    numTest = 1       # number of tests for each configuration
    difficulty = 'H'  # E - easy, M - medium, H - high
    timeout = 600     # set timeout to exit, will display 'infs'

    consisList = ['ForwardChecking', 'ArcConsistency', 'NKD', 'NKT']
    outfile = open('log/P' + difficulty + '.txt', 'w+')
    headline = 'id numBacktracks numAssignments avgtime'
    print('\n'+headline)
    outfile.write(headline+'\n')
    ph5_comb = [21, 27, 93, 75, 81, 87, 69, 159, 387, 63, 147, 141, 381, 351, 339, 363, 345, 333, 15, 153, 22, 327, 375, 279, 321, 369, 129]
    for root, dirs, files in os.walk("ExampleSudokuFiles/"):
        # for name in [x for x in files if x.startswith('P' + difficulty)]:
            name = "PH5.txt"
            combid = 0
            logline = name
            outfile.write(logline+'\n')
            print('\n' + logline)
            print('Unordered Result:')
            data = filereader.SudokuFileReader("ExampleSudokuFiles/" + name)
            timeHeap = []
            for consisNum in range(16):
                consisChk = []
                consisBits = "{0:04b}".format(consisNum)
                for bit, consisBit in enumerate(consisBits):
                    if consisBit == '1':
                        consisChk.append(consisList[bit])
                if not consisChk:
                    consisChk = ['None']
                for consisChkPermute in permutations(consisChk):
                    for VarH in ['None', 'MRV', 'DH']:
                        for ValH in ['None', 'LCV']:
                            combid += 1
                            if combid in ph5_comb:
                                avgtime = 0
                                for i in range(numTest):
                                    solver = btsolver.BTSolver(data)
                                    for consis in consisChkPermute:
                                        solver.setConsistencyChecks(
                                             btsolver.ConsistencyCheck[consis])
                                    solver.setVariableSelectionHeuristic(
                                        btsolver.VariableSelectionHeuristic[VarH])
                                    solver.setValueSelectionHeuristic(
                                        btsolver.ValueSelectionHeuristic[ValH])
                                    signal.signal(signal.SIGALRM, signal_handler)
                                    signal.alarm(timeout)
                                    try:
                                        avgtime += float(solver.solve())
                                        signal.alarm(0)  # cancel alarm
                                    except Exception:
                                        avgtime = float('inf')
                                        break
                                    if i == numTest - 1:
                                        avgtime /= numTest
                                status = str(combid) + ' ' +\
                                    str(solver.numBacktracks) + ' ' +\
                                    str(solver.numAssignments) + ' ' +\
                                    str(avgtime)
                                print(status)
                                heappush(timeHeap, (avgtime, status))           
            print('Ordered Result:')
            while timeHeap:
                avgtime, status = heappop(timeHeap)
                outfile.write(status+'\n')
                print(status)
    outfile.close()


if __name__ == '__main__':
    main()
