class IntcodeMemory(list):
    DEFAULT_VALUE = 0

    """
    Subclass of list that defaults to a value of 0 and can extend to an
    infinite size. Negative values and slice access are forbidden.
    """
    def __init__(self, code=[]):
        # Initialse ourselves with code
        self += code

    def __fill(self, index):
        "fill memory with zeroes up to index"
        self += ([self.DEFAULT_VALUE] * (index - len(self) + 1))

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            raise Exception("slice access")

        if index < 0:
            raise Exception("negative memory access")

        self.__fill(index)
        list.__setitem__(self, index, value)

    def __getitem__(self, index):
        if isinstance(index, slice):
            raise Exception("slice access")

        if index < 0:
            raise Exception("negative memory access")

        if index >= len(self):
            return self.DEFAULT_VALUE
        else:
            return list.__getitem__(self, index)

    def __add__(self, other):
        if isinstance(other, list):
            r = self.copy()
            r += other
            return r
        else:
            return list.__add__(self, other)

    def copy(self):
        "Return a shallow copy of the list"
        r = IntcodeMemory()
        r += self
        return r


