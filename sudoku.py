import numpy as np
from dataclasses import dataclass, field
# https://sandiway.arizona.edu/sudoku/index.html#heuristics

@dataclass
class cell:
    grid: 'np.array' = None
    x: int = 0
    y: int = 0
    potentials: set = field(default_factory=lambda:set(range(1,10)))
    def __hash__(self):
        return 9 * self.y + self.x
    # nditer / flatiter
    @property
    def blk(self):
        x = self.x//3 * 3
        y = self.y//3 * 3
        return self.grid[x:x+2,y:y+2].flatten()
    @property
    def row(self):
        return self.grid[self.x,:]
    @property
    def col(self):
        return self.grid[:,self.y]
    @property
    def val(self):
        return self.potentials

    #@val.setter
    def assign(self, val):
        self.potentials = set((val,))
        self.update_neighbors()

    def reduce(self, nval):
        if len(self.potentials) == 1:
            return
        self.potentials -= nval
        # it's a contradiction to have no options
        if not self.val:
            raise SyntaxError

        if len(self.potentials) == 1:
            self.update_neighbors()

    def update_neighbors(self):
        n = set((*self.blk, *self.row, *self.col))
        for c in n:
            if c != self:
                c.reduce(self.val)

    def __str__(self):
        if len(self.potentials) > 1:
            return ' '
        return str(next(iter(self.potentials)))

class grid:
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
        shape = (9,9)
        self.grid = np.array([cell() for _ in range(81)]).reshape(shape)
        for idx in np.ndindex(shape):
            e = self.grid[idx]
            e.x, e.y, e.grid = *idx, self.grid
        if values:
            self.load(values)
    def load(self, values):
        for (x,y), e in np.ndenumerate(np.array(values).reshape((9,9))):
            if e:
                self.grid[x,y].assign(e)

    def __str__(self):
        return self.fmt.format(*self.grid.flatten())

    def check(self, solution):
        return self.fmt.format(*(
            ' ' if s == a else 'X'
            for s, a in zip((next(iter(c.val)) for c in self.grid.flatten()), solution)
            ))

    @property
    def cpot(self):
        return self.fmt.format(*(len(c.val) for c in self.grid.flatten()))

# https://sandiway.arizona.edu/sudoku/examples.html
#      |     |     |     |
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

g = grid(easy1)
print(g)
#print(g.cpot)
print(g.fmt.format(*sol1))
print(g.check(sol1))
