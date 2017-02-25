"""Variable for CSP."""


import trail
import domain

STATIC_NAMING_COUNTER = 1


class Variable:

    def __init__(self, possible_Values, row, col, block):
        # self.namingCounter = 1
        global STATIC_NAMING_COUNTER
        self.name = "v" + str(STATIC_NAMING_COUNTER)
        # self.namingCounter += 1
        STATIC_NAMING_COUNTER += 1
        self.domain = domain.Domain(possible_Values)
        self.row = row
        self.col = col
        self.block = block
        if self.size() == 1:
            self.modified = True
            self.unchangeable = True
        else:
            self.modified = False
            self.unchangeable = False
        self.oldSize = self.size()
        self.trailOfVariable = trail.masterTrailVariable

    # --------- Copy Constructors Method ---------
    def copy(self, v):
        self.domain = v.domain
        self.row = v.row
        self.col = v.col
        self.block = v.block
        self.modified = v.modified
        self.name = v.name

    # --------- Accessors Method ---------
    def isChangeable(self):
        return not self.unchangeable

    def isAssigned(self):
        return self.size() == 1

    def isModified(self):
        return self.modified

    def setModified(self, mod):
        self.modified = mod
        self.domain.modified = mod

    def getAssignment(self):
        """Return the value currently assigned to the IntVariable, 0 if no."""
        if not self.isAssigned():
            return 0
        else:
            return self.domain.values[0]

    def Values(self):
        return self.domain.values

    def size(self):
        return self.domain.size()

    # --------- Modifiers Method ---------
    # def assignValue(self, val):
    #     """
    #         Used for local Search
    #         @param val new assignment
    #     """
    #     self.setDomain(domain.Domain(val))

    def updateDomain(self, d):
        """Add the changed domain to the Trail (Used for Backtracking)."""
        self.methodModifiesDomain()
        if self.domain != d:
            self.domain = d
            self.modified = True

    def setDomain(self, d):
        """Change to a new domain without changing the Trail."""
        if self.domain != d:
            self.domain = d
            self.modified = True

    def removeValueFromDomain(self, val):
        """Remove a single value from the domain of V."""
        self.methodModifiesDomain()
        self.domain.remove(val)
        self.modified = self.domain.isModified()

    # --------- Helper Method ---------
    def methodModifiesDomain(self):
        newSize = self.size()
        if self.oldSize > newSize:
            self.oldSize = newSize
        self.trailOfVariable.push(self)

    # --------- String Representation ---------
    def __str__(self):
        # "print node stats"
        output = ""
        output += " Name: " + self.name
        output += " Row " + str(self.row) + " Col " + str(self.col) + \
                  " BLock " + str(self.block)
        output += " domain: {"
        for i in self.domain.values:
            output += str(i) + ","
        output = output.rstrip()
        output = output[:-1]
        output += "}"
        return output
