"""Constraint Network of CSP."""


class ConstraintNetwork:
    def __init__(self):
        """
        CSP representation of the problem.
        Contains the variables, constraints, and many helpful accessors.
        """
        self.constraints = []
        self.variables = []

    # --------- Modifiers Method ---------
    def addConstraint(self, c):
        if c not in self.constraints:
            self.constraints.append(c)

    def addVariable(self, v):
        if v not in self.variables:
            self.variables.append(v)

    # def pushAssignment(self, a):
    #     """
    #         Used for Local Search. Assigns a value to a variable based
    #         on the parameter a
    #         @param a Assignment to actualize
    #     """
    #     a.variable.assignValue(a.value)

    # --------- Accessors Method ---------
    def getNeighborsOfVariable(self, v):
        neighbors = set()
        for c in self.constraints:
            if c.contains(v):
                for x in c.vars:
                    neighbors.add(x)
        neighbors.remove(v)
        return list(neighbors)

    # def isConsistent(self):
    #     """
    #     Used for local search.
    #     Determines if the current assignment is consistent.
    #     """
    #     for c in self.constraints:
    #         return c.isConsistent()
    #     return True

    def getConstraintsContainingVariable(self, v):
        """If list of constraints that contains v."""
        outList = []
        for c in self.constraints:
            if c.contains(v):
                outList.append(c)
        return outList

    def getModifiedConstraints(self):
        """
        Return modified constraints.

        Specificallt, return the constraints containing variables whose
        domains were modified since the last call to this method.

        After getting the constraints, it will reset each variable to
        unmodified.

        Note* The first call to this method returns the constraints
        containing the initialized variables.

        @return ArrayList of modified constraints
        """
        mConstraints = []
        for c in self.constraints:
            if c.isModified():
                mConstraints.append(c)

        for v in self.variables:
            v.setModified(False)

        return mConstraints

    # --------- String Representation ---------
    def __str__(self):
        output = str(len(self.variables)) + " Variables: {"
        delim = ""

        for v in self.variables:
            output += delim + v.name
            delim = ","
        output += "}"

        output += "\n" + str(len(self.constraints)) + " Constraints:"
        delim = "\n"
        for c in self.constraints:
            output += delim + str(c)

        output += "\n"
        for v in self.variables:
            output += str(v) + "\n"

        return output
