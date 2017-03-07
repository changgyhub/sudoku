"""Constraint of CSP."""


class Constraint:

    def __init__(self):
        """
        Constraint represents a NotEquals constraint on a set of variables.
        Used to ensure none of the variables contained in the constraint
        have the same assignment.
        """
        self.vars = []

    # --------- Copy Constructors Method ---------
    def copy(self, vars):
        self.vars = vars

    # --------- Modifiers Method ---------
    def addVariable(self, v):
        self.vars.append(v)

    # --------- Accessors Method ---------
    def size(self):
        return len(self.vars)

    def contains(self, v):
        """If v is in the constraint or not."""
        return v in self.vars

    def isModified(self):
        """If the a variable in the constraint has been modified."""
        for var in self.vars:
            if var.isModified():
                return True
        return False

    # def getConflicts(self):
    #     "Used for local search"
    #     pass

    # --------- Modifiers Method ---------
    def propagateConstraint(self):
        """
        Propagate the notequal constraint.
        Attempt to propagate the notequal constraint through the variables
        in the constraint. If it fails to do so, the propagation stops
        midway and does not reset the changes to the domains of the
        variables made so far.
        """
        # compares assignments and determines if the assigment breaks the
        # constraints
        for var in self.vars:
            if not var.isAssigned():
                continue
            varAssignment = var.getAssignment()
            for otherVar in self.vars:
                if var == otherVar:
                    continue
                if otherVar.size() == 1 and \
                   otherVar.getAssignment() == varAssignment:
                    return False
                otherVar.removeValueFromDomain(varAssignment)
        return True

    # def isConsistent(self):
    #     """
    #         Used for local search. Same as propagate constraint.
    #         @return true if constraint is consistent, false otherwise.
    #     """
    #     return self.propagateConstraint()

    # --------- String Representation ---------
    def __str__(self):
        output = "{"
        delim = ""
        for v in self.vars:
            output += delim + v.name
            delim = ","
        output += "}"
        return output
