"""Domain of CSP."""


class Domain:

    def __init__(self, value_or_values):
        """Represent the domain of a variable."""
        self.values = []
        if type(value_or_values) is int:
            self.values.append(value_or_values)
        else:  # type list
            self.values = value_or_values

        self.modified = False

    # --------- Constructors/Modified Method ---------
    def copy(self, values):
        self.values = values

    def add(self, num):
        self.values.append(num)

    def remove(self, num):
        if num in self.values:
            self.modified = True
            self.values.remove(num)
            return True
        else:
            return False

    # --------- Accessors Method ---------
    def contains(self, v):
        """Check if a value exists within the domain."""
        return v in self.values

    def size(self):
        return len(self.values)

    def isEmpty(self):
        """Return true if no values are contained in the domain."""
        return not self.values

    def isModified(self):
        """Return whether or not the domain has been modified."""
        return self.modified

    # --------- String Representation ---------
    def __str__(self):
        """String Representation method to print Domain values inside {}."""
        output = "{"
        for i in range(len(self.values) - 1):
            output += str(self.values[i]) + ", "
        try:
            output += str(self.values[-1])
        except IndexError:
            pass

        output += "}"
        return output
        # return str(self.values)
