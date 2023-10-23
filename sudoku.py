import numpy as np

class Contradiction(Exception):
    """Thrown when assigning a value results in another cell having no possible values"""

class sudoku:
    shape = (9,9)
    fmt = """*-----------------*
|{} {} {}|{} {} {}|{} {} {}|
|{} {} {}|{} {} {}|{} {} {}|
|{} {} {}|{} {} {}|{} {} {}|
|-----------------|
|{} {} {}|{} {} {}|{} {} {}|
|{} {} {}|{} {} {}|{} {} {}|
|{} {} {}|{} {} {}|{} {} {}|
|-----------------|
|{} {} {}|{} {} {}|{} {} {}|
|{} {} {}|{} {} {}|{} {} {}|
|{} {} {}|{} {} {}|{} {} {}|
*-----------------*"""
    def __init__(self, values = None) -> None:
        # represent values 1..9 as a bitfield. Fill grid with full potential 0b111111111
        self.grid = np.full(self.shape, (1 << 9) - 1, dtype=np.uint16)
        if values:
            self.load(values)

    def load(self, values):
        for idx, value in np.ndenumerate(np.array(values).reshape(self.shape)):
            if value:
                self[idx] = value

    def guess(self):
        checkpoint = self.grid.copy()
        # find first ambiguous index
        for idx, bits in np.ndenumerate(self.grid):
            if bits.bit_count() == 1:
                continue
            # loop through all potential values at idx
            value = 1
            while bits:
                if not 1 & bits:
                    value, bits = value + 1, bits >> 1
                    continue
                try:
                    self[idx] = value
                    self.guess()
                    break
                except Contradiction:
                    self.grid[:,:] = checkpoint[:,:]
                    value, bits = value + 1, bits >> 1
            else:
                # we've tried all possible values at idx and all lead to contradictions.
                # a previous guess was wrong. we need to backtrack
                raise Contradiction

    def __getitem__(self, position):
        # convert bitfield into integer, return 0 if the value isn't yet determined.
        b = int(self.grid[position])
        return b.bit_length() if b.bit_count() == 1 else 0

    def __setitem__(self, position, value):
        # convert integer into bitfield
        bit = 1 << (value - 1)

        # all places where propagation may happen
        # this considers only direct row, column, and block constraints
        mask = np.zeros(self.shape, dtype=np.uint16)
        mask[position[0],:] = 1
        mask[:,position[1]] = 1
        x0, y0 = position[0] - (position[0] % 3), position[1] - (position[1] % 3)
        mask[x0:x0+3,y0:y0+3] = 1
        mask[position] = 0

        # where propagation actually will happen
        prop = (self.grid & (mask*bit))

        # make changes
        self.grid[position] = bit
        self.grid ^= prop

        # if any bitfield is 0, that cell can't contain any values
        if np.any(self.grid == 0):
            raise Contradiction

        # propagate to indexes that changed and are now final values
        for idx in zip(*prop.nonzero()):
            if self[idx]:
                self[idx] = self[idx]

    def __str__(self):
        return self.fmt.format(*(
            int(b).bit_length() if b.bit_count() == 1 else ' ' for b in self.grid.flatten()
            ))

    def diff(self, solution):
        match = [self[idx] == a
            for (idx, _), a in zip(np.ndenumerate(self.grid), solution)
                 ]
        return False if all(match) else self.fmt.format(*(['X', ' '][v] for v in match))

blank =[0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0]
# https://sandiway.arizona.edu/sudoku/examples.html
# Arizona Daily Wildcat: Tuesday, Jan 17th 2006
# guessing not necessary
easy1 =[0,0,0,2,6,0,7,0,1,
        6,8,0,0,7,0,0,9,0,
        1,9,0,0,0,4,5,0,0,
        8,2,0,1,0,0,0,4,0,
        0,0,4,6,0,2,9,0,0,
        0,5,0,0,0,3,0,2,8,
        0,0,9,3,0,0,0,7,4,
        0,4,0,0,5,0,0,3,6,
        7,0,3,0,1,8,0,0,0]
sol1 = [4,3,5,2,6,9,7,8,1,
        6,8,2,5,7,1,4,9,3,
        1,9,7,8,3,4,5,6,2,
        8,2,6,1,9,5,3,4,7,
        3,7,4,6,8,2,9,1,5,
        9,5,1,7,4,3,6,2,8,
        5,1,9,3,2,6,8,7,4,
        2,4,8,9,5,7,1,3,6,
        7,6,3,4,1,8,2,5,9]

# Vegard Hanssen puzzle 2155141
# guessing also not technically necessary, but the simple propagation implemented here is insufficient
hard2 =[0,0,0,6,0,0,4,0,0,
        7,0,0,0,0,3,6,0,0,
        0,0,0,0,9,1,0,8,0,
        0,0,0,0,0,0,0,0,0,
        0,5,0,1,8,0,0,0,3,
        0,0,0,3,0,6,0,4,5,
        0,4,0,2,0,0,0,6,0,
        9,0,3,0,0,0,0,0,0,
        0,2,0,0,0,0,1,0,0]
sol2 = [5,8,1,6,7,2,4,3,9,
        7,9,2,8,4,3,6,5,1,
        3,6,4,5,9,1,7,8,2,
        4,3,8,9,5,7,2,1,6,
        2,5,6,1,8,4,9,7,3,
        1,7,9,3,2,6,8,4,5,
        8,4,5,2,1,9,3,6,7,
        9,1,3,7,6,8,5,2,4,
        6,2,7,4,3,5,1,9,8]

g = sudoku(easy1)
print(g)
print(g.diff(sol1) or 'ok')
g = sudoku(hard2)
g.guess()
print(g)
print(g.diff(sol2) or 'ok')
