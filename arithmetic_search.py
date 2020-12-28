from collections import deque
from operator import add, mul, sub

import numpy as np


GRID = np.array([
    [None, sub, 9, mul],
    [add, 4, sub, 18],
    [4, mul, 11, mul],
    [mul, 8, sub, 1],
])
START_VALUE = 22
VAULT_TARGET = 30


def adj(pos):
    i, j = pos
    if i > 0:
        yield i - 1, j
    if i < len(GRID) - 1:
        yield i + 1, j
    if j > 0:
        yield i, j - 1
    if j < len(GRID[0]) - 1:
        yield i, j + 1


def main():
    q = deque()
    q.append(((0, 0), START_VALUE, (str(START_VALUE),)))
    while q:
        pos, val, path = q.popleft()
        if pos == (0, 0) and len(path) != 1:
            continue
        if pos == (3, 3):
            if val == VAULT_TARGET:
                print(" ".join(path))
                break
            continue
        for op_pos in adj(pos):
            op = GRID[op_pos]
            for arg_pos in adj(op_pos):
                arg = GRID[arg_pos]
                if arg is not None:
                    q.append((arg_pos, op(val, arg), path + (op.__name__, str(arg))))


if __name__ == "__main__":
    main()
