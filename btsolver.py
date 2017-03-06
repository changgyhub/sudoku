"""Backtracking Solver for CSP."""


import time
import queue
import functools

import constraint
import constraintnetwork
import domain
import filereader
import gameboard
import trail
import variable
import collections
import itertools

# dictionary mapping heuristic to number
'''
for example, to set the variable selection heuristic to MRV, you would say,
self.setVariableSelectionHeuristic(VariableSelectionHeuristic
['MinimumRemainingValue']) this is needed when you have more than one heuristic
to break ties or use one over the other in precedence. you can also manually
set the heuristics in the main.py file when reading the parameters as the
primary heuristics to use and then break ties within the functions you
implementIt follows similarly to the other heuristics and chekcs
'''
VariableSelectionHeuristic = {'None': 0, 'MRV': 1, 'DH': 2}
# ValueSelectionHeuristic = {'None': 0, 'LeastConstrainingValue': 1}
ValueSelectionHeuristic = {'None': 0, 'LCV': 1}
ConsistencyCheck = {'None': 0, 'ForwardChecking': 1,
                    'ArcConsistency': 2, 'NKD': 3, 'NKT':4}


class BTSolver:
    """Backtracking solver."""

    # ---------Constructors Method ---------
    def __init__(self, gb):
        self.network = filereader.GameBoardToConstraintNetwork(gb)
        self.trail = trail.masterTrailVariable
        self.hassolution = False
        self.gameboard = gb

        self.numAssignments = 0
        self.numBacktracks = 0
        self.preprocessing_startTime = 0
        self.preprocessing_endTime = 0
        self.startTime = None
        self.endTime = None

        # refers to which variable selection heuristic in use(0 means default,
        # 1 means MRV, 2 means DEGREE)
        self.varHeuristics = 0
        # refers to which value selection heuristic in use(0 means default, 1
        # means LCV)
        self.valHeuristics = 0
        # refers to which consistency check will be run(0 for backtracking, 1
        # for forward checking, 2 for arc consistency)
        self.cChecks = []
        # self.runCheckOnce = False
        self.tokens = []  # tokens(heuristics to use)

        # build list of houses
        # e.g. for N=9, house length = 27, houses[0:8]are the row houses,
        # 9:17 are the column houses, and 18:26 are the block houses
        self.houses = [[] for x in range(self.gameboard.N*3)]
        self.colhouseoffset = self.gameboard.N
        self.blockhouseoffset = self.gameboard.N*2
        for i in self.network.variables:
            self.houses[i.row].append(i)
            self.houses[i.col+self.colhouseoffset].append(i)
            self.houses[i.block+self.blockhouseoffset].append(i)

    # --------- Modifiers Method ---------

    def setTokens(self, tokens):
        """Set the set of heuristics to be taken into consideration."""
        self.tokens = tokens

    def setVariableSelectionHeuristic(self, vsh):
        """Modify the variable selection heuristic."""
        self.varHeuristics = vsh

    def setValueSelectionHeuristic(self, vsh):
        """Modify the value selection heuristic."""
        self.valHeuristics = vsh

    def setConsistencyChecks(self, cc):
        """Modify the consistency check."""
        self.cChecks.append(cc)

    # --------- Accessors Method ---------
    def getSolution(self):
        return self.gameboard

    # @return time required for the solver to attain in seconds
    def getTimeTaken(self):
        return self.endTime - self.startTime

    # --------- Helper Method ---------
    def checkConsistency(self):
        """which consistency check to run but it is up to you when implementing
        the heuristics to break ties using the other heuristics passed in。"""
        allchecked = self.assignmentsCheck()
        for method in self.cChecks:
            if not allchecked:
                break
            if method == 1:
                allchecked = allchecked and self.forwardChecking()
            elif method == 2:
                allchecked = allchecked and self.arcConsistency()
            elif method == 3:
                allchecked = allchecked and self.nakedDouble()
            elif method == 4:
                allchecked = allchecked and self.nakedTriple()
        return allchecked

    def assignmentsCheck(self):
        """
            default consistency check. Ensures no two variables are assigned to
            the same value.
            @return true if consistent, false otherwise.
        """
        for v in self.network.variables:
            if v.isAssigned():
                for vOther in self.network.getNeighborsOfVariable(v):
                    if v.getAssignment() == vOther.getAssignment():
                        return False
        return True

    def nakedCandidate(self,r):

        # if there is an assigned cell
        # eliminate all possible candidates in the same row, column and block
        def searchAllPotentialCandidates():
            for i in self.network.variables:
                if i.isAssigned():
                    neighbours = list(self.houses[i.row])
                    neighbours.extend(self.houses[i.col + self.colhouseoffset])
                    neighbours.extend(self.houses[i.block + \
                                      self.blockhouseoffset])
                    for other in neighbours:
                        if i != other and not other.isAssigned():
                            if i.getAssignment() in other.domain.values:
                                # other.domain.values.remove(i.getAssignment())
                                other.removeValueFromDomain(i.getAssignment())


        # check if the current house is consistent
        def isConsistent(houses):
            dic = {}
            for cell in house:
                if cell.isAssigned():
                    val = cell.getAssignment()
                    if dic.get(val) == 1:
                        return False
                    else:
                        dic[val] = 1
            return True

        # eliminate the candidates in other cells in the same house
        # return false if inconsistent assignment is found
        def eliminateOtherCellsInTheSameHouse(house,zones,candidates):
            for cell in house:
                if cell not in zones:
                    for can in candidates:
                        if can in cell.domain.values:
                            # if cell.isAssigned():
                            #     return False
                            cell.removeValueFromDomain(can)
                            # print("eliminate ", cell)



        # each candidate occur more than two times but less than or equal to
        # three times in the combined list, of which three cells are included
        # e.g. (2,9)  (2,9)  (2,6,9)  are not nakedtriple

        def occureMoreThanTwoTimes(candidates,lumplist,r):
            for candit in candidates:
                if lumplist.count(candit) < 2 or lumplist.count(candit) > r:
                    return False
            return True


        # return all the legal permutations given constraint r
        # N.B. the order does not matter
        # the maximum number of permutations is n!/(n-r)!*r!,
        # where n is the size of M*N grid, and r is the constraint
        # Note that illegal permutations are eliminated by checkPermutations()
        def permutations(iterable, r):
            pool = tuple(iterable)
            n = len(pool)
            it = itertools.combinations(range(n), r)
            for indices in it:
                if len(set(indices)) == r:
                    toContinue,candidates = checkPermutations(pool,indices,r)
                    if toContinue:
                        # for i in indices:
                        #     print(pool[i])
                        yield tuple(pool[i] for i in indices), candidates

        # return if the current permutation (indices) is not a naked candidate
        def checkPermutations(pool,indices,r):
            lumplist = []
            candidates = set()
            for i in indices:
                cell = pool[i]
                if cell.isAssigned() or len(cell.domain.values) > r:
                    return False, None
                lumplist.extend(cell.domain.values)
                candidates.update(cell.domain.values)
            if len(candidates) != r:
                return False, None
            if not occureMoreThanTwoTimes(candidates,lumplist,r):
                return False, None
            return True, candidates

        # start searching naked candidates
        searchAllPotentialCandidates();

        for hindex, house in enumerate(self.houses):
            for combination,candidates in permutations(house,r):
                eliminateOtherCellsInTheSameHouse(house,
                    combination, candidates)
            if not isConsistent(house):
                    return False

        return True

    def nakedDouble(self):
        return self.nakedCandidate(2)

    def nakedTriple(self):
        return self.nakedCandidate(3)

    def forwardChecking(self):
        """Forward checking."""
        for v in self.network.variables:
            if v.isAssigned():
                for vOther in self.network.getNeighborsOfVariable(v):
                    if v.getAssignment() == vOther.getAssignment():
                        return False
                    vOther.removeValueFromDomain(v.getAssignment())
                    if vOther.domain.size() == 0:
                        return False
        return True

    def arcConsistency(self):
        """Maintaining Arc Consistency."""
        worklist = queue.Queue()
        for v in self.network.variables:
            if v.isAssigned():
                for vOther in self.network.getNeighborsOfVariable(v):
                    worklist.put((v, vOther))
                    worklist.put((vOther, v))

        def arcReduce(x, y):
            """Reduce arc used in arcConsistency algorithm."""
            change = False
            for vx in x.Values():
                allow = False
                for vy in y.Values():
                    if vx != vy:
                        allow = True
                        break
                if not allow:
                    x.removeValueFromDomain(vx)
                    change = True
            return change

        while not worklist.empty():
            x, y = worklist.get()
            if arcReduce(x, y):
                if x.domain.size() == 0:
                    return False
                else:
                    for z in self.network.getNeighborsOfVariable(x):
                        if z != y:
                            worklist.put((x, z))
                            worklist.put((z, x))
        return True

    def selectNextVariable(self):
        """
            Selects the next variable to check.
            @return next variable to check. null if there are no more variables
                    to check.
        """
        if self.varHeuristics == 0:
            return self.getfirstUnassignedVariable()
        elif self.varHeuristics == 1:
            return self.getMRV()
        elif self.varHeuristics == 2:
            return self.getDegree()
        else:
            return self.getfirstUnassignedVariable()

    def getfirstUnassignedVariable(self):
        """
            default next variable selection heuristic. Selects the first
            unassigned variable.
            @return first unassigned variable. null if no variables are
                    unassigned.
        """
        for v in self.network.variables:
            if not v.isAssigned():
                return v
        return None

    def getMRV(self):
        """MRV heuristic."""
        var = None
        mrv = float('inf')
        for v in self.network.variables:
            if not v.isAssigned():
                if v.domain.size() < mrv:
                    var = v
                    mrv = v.domain.size()
        return var

    def getDegree(self):
        """Degree heuristic."""
        var = None
        mnv = float('-inf')
        for v in self.network.variables:
            if not v.isAssigned():
                neigh = self.network.getNeighborsOfVariable(v)
                numMnv = sum([1 for i in neigh if not i.isAssigned()])
                if numMnv > mnv:
                    var = v
                    mdv = numMnv
        return var

    def getNextValues(self, v):
        """
            Value Selection Heuristics. Orders the values in the domain of the
            variable passed as a parameter and returns them as a list.
            @return List of values in the domain of a variable in a specified
                    order.
        """
        if self.valHeuristics == 0:
            return self.getValuesInOrder(v)
        elif self.valHeuristics == 1:
            return self.getValuesLCVOrder(v)
        else:
            return self.getValuesInOrder(v)

    def getValuesInOrder(self, v):
        """
            Default value ordering.
            @param v Variable whose values need to be ordered
            @return values ordered by lowest to highest.
        """
        values = v.domain.values
        return sorted(values)

    def getValuesLCVOrder(self, v):
        """LCV heuristic."""
        values = v.domain.values

        def compareLCV(v1,v2):
            """compare LCV of two variables"""
            numConstraintV1 = 0
            numConstraintV2 = 0
            for neigh in self.network.getNeighborsOfVariable(v):
                if neigh.domain.contains(v1):
                    numConstraintV1 += 1
                if neigh.domain.contains(v2):
                    numConstraintV2 += 1
            return numConstraintV1 - numConstraintV2

        return sorted(values, key = functools.cmp_to_key(compareLCV))

    def success(self):
        """ Called when solver finds a solution """
        self.hassolution = True
        self.gameboard = \
            filereader.ConstraintNetworkToGameBoard(self.network,
                                                    self.gameboard.N,
                                                    self.gameboard.p,
                                                    self.gameboard.q)

    # --------- Solver Method ---------
    def solve(self):
        """ Method to start the solver """
        self.startTime = time.time()
        try:
            self.solveLevel(0)
        except VariableSelectionException:
            print("Error with variable selection heuristic.")
        self.endTime = time.time()
        # trail.masterTrailVariable.trailStack = []
        self.trail.trailStack = []
        return self.endTime - self.startTime

    def solveLevel(self, level):
        """
            Solver Level
            @param level How deep the solver is in its recursion.
            @throws VariableSelectionException
                contains some comments that can be uncommented for more
                in depth analysis
        """
        # print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")
        # print("BEFORE ANY SOLVE LEVEL START")
        # print(self.network)
        # print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")

        if self.hassolution:
            return

        # Select unassigned variable
        v = self.selectNextVariable()
        # print("V SELECTED --> " + str(v))

        # check if the assigment is complete
        if v is None:
            # print("!!! GETTING IN V == NONE !!!")
            for var in self.network.variables:
                if not var.isAssigned():
                    raise ValueError(
                        '''Something happened with the
                        variable selection heuristic''')
            self.success()
            return

        # loop through the values of the variable being checked LCV
        # print("getNextValues(v): " + str(self.getNextValues(v)))
        for i in self.getNextValues(v):
            # print("next value to test --> " + str(i))
            self.trail.placeTrailMarker()

            # check a value
            v.updateDomain(domain.Domain(i))
            self.numAssignments += 1

            # move to the next assignment
            if self.checkConsistency():
                self.solveLevel(level + 1)

            # if this assignment failed at any stage, backtrack
            if not self.hassolution:
                # print("=======================================")
                # print("AFTER PROCESSED:")
                # print(self.network)
                # print("================ ")
                # print("self.trail before revert change: ")
                for i in self.trail.trailStack:
                    pass
                    # print("variable --> " + str(i[0]))
                    # print("domain backup --> " + str(i[1]))
                # print("================= ")

                self.trail.undo()
                self.numBacktracks += 1
                # print("REVERT CHANGES:")
                # print(self.network)
                # print("================ ")
                # print("self.trail after revert change: ")
                for i in self.trail.trailStack:
                    pass
                    # print("variable --> " + str(i[0]))
                    # print("domain backup --> " + str(i[1]))
                # print("================= ")

            else:
                return
