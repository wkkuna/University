from random import choice, randint, seed
from time import time
import numpy as np

cache = {}

class Puzzle:
    def __init__(self, rows_spec, columns_spec):
        self.rows_spec = rows_spec
        self.columns_spec = columns_spec
        self.width = len(columns_spec)
        self.height = len(rows_spec)
        self.reset()

    def draw_puzzle(self):
        output = ""
        for i in range(self.height):
            for j in range(self.width):
                if self.puzzle[i][j] == 1:
                    output += '#'
                else:
                    output += '.'
            output += '\n'
        return output

    def is_valid(self, x=None, y=None):
        def is_valid_seq(bits, spec):
            offset = 0
            bits_str = "".join(str(e) for e in bits)
            for s in spec:
                idx = bits_str.find('1' * s, offset)
                if idx == -1:
                    return False
                offset = idx + s + 1
            return sum(bits) == sum(spec)

        if x != None:
            return is_valid_seq(self.puzzle[x], self.rows_spec[x])

        if y != None:
            return is_valid_seq([self.puzzle[x][y] for x in range(self.height)], self.columns_spec[y])

        for i in range(self.height):
            if not self.is_valid(x=i):
                return False
        for j in range(self.width):
            if not self.is_valid(y=j):
                return False
        return True

    def fill_certain(self):
        invalid_rows = [x for x in range(self.height) if not self.is_valid(x=x)]
        invalid_columns = [y for y in range(self.width) if not self.is_valid(y=y)]

        def fill(idx, is_row=True):
            def fill_range(idx, start, stop, value, is_row=True):
                if stop < start:
                    return

                for i in range(start, stop):
                    row = idx if is_row else i
                    col = i if is_row else idx

                    self.puzzle[row][col] = value

            specs = self.rows_spec[idx] if is_row else self.columns_spec[idx]
            dim = self.width if is_row else self.height
            
            for i, spec in enumerate(specs):
                sum_left = sum(specs[:i]) + i
                sum_right = sum(specs[i+1:]) + len(specs) - i - 1

                x0 = sum_left
                x1 = dim - sum_right
                diff = x1 - x0 - spec
                fill_range(idx, x0 + diff, x1 - diff, 1, is_row=is_row)

        for x in invalid_rows:
            fill(x)

        for y in invalid_columns:
            fill(y, is_row=False)

    def reset(self):
        self.puzzle = [[0 for y in range(self.width)]
                       for x in range(self.height)]

    def solve(self):
        t0 = 0
        limit = 30000

        def pick_row():
            invalid_rows = [x for x in range(self.height) if not self.is_valid(x=x)]
            if len(invalid_rows) == 0:
                return None
            return choice(invalid_rows)

        def pick_column():
            invalid_columns = [y for y in range(self.width) if not self.is_valid(y=y)]
            if len(invalid_columns) == 0:
                return None
            return choice(invalid_columns)

        def opt_dist(idx, spec, is_row):
            seq = self.puzzle[idx] if is_row else [self.puzzle[x][idx] for x in range(self.height)]

            def opt_dist_sequence(bits, spec):
                global cache
                run = tuple(bits), tuple(spec)
                if run in cache:
                    return cache[run]

                if not spec:
                    return sum(bits)

                n = len(bits)
                s = spec[0]
                
                subseq = sum(bits[:s])
                after = n > s and bits[s]
                min_cost = (s - subseq) + after + opt_dist_sequence(bits[s+1:], spec[1:])
                
                before = 0
                last = n - sum(spec) - len(spec) + 1
                for i in range(last):
                    subseq += bits[i + s] - bits[i]
                    before += bits[i]
                    after = n > i + s + 1 and bits[i + s + 1]
                    min_cost = min(s - subseq + before + after + opt_dist_sequence(bits[i+s+2:], spec[1:]), min_cost)

                cache[run] = min_cost
                return min_cost
            
            return opt_dist_sequence(seq, spec)

        def switch(i, j):
            self.puzzle[i][j] ^= 1

        def get_opt_element(idx, is_row=True):
            dim = self.width if is_row else self.height
            best_fit = -dim
            opt_elem = None

            for i in range(dim):                
                row_idx = idx if is_row else i
                column_idx = i if is_row else idx

                op0 = opt_dist(row_idx, self.rows_spec[row_idx], True)\
                    + opt_dist(column_idx, self.columns_spec[column_idx], False)
                
                switch(row_idx, column_idx)
                
                ops = opt_dist(row_idx, self.rows_spec[row_idx], True)\
                    + opt_dist(column_idx, self.columns_spec[column_idx], False)

                if ops == np.Inf:
                    continue 

                if op0 - ops > best_fit:
                    best_fit = op0 - ops
                    opt_elem = (row_idx, column_idx)
                
                switch(row_idx, column_idx)
            return opt_elem
        
        self.fill_certain()

        while (not self.is_valid() and t0 < limit):
            self.fill_certain()
            pick = pick_row()
            elem = None
            
            if pick is None or t0 % 2:
                pick = pick_column()
                if pick is not None:
                    elem = get_opt_element(pick, is_row=False)
            else:
                elem = get_opt_element(pick)

            if t0%5 == 0:
                switch(randint(0, self.height-1), randint(0, self.width-1))

            if elem is None:
                switch(randint(0, self.height-1), randint(0, self.width-1))
            else:
                switch(elem[0], elem[1])
            t0 += 1

        if not self.is_valid():
            return None

        return self.draw_puzzle()


def solve_puzzle(puzzle):
    out = puzzle.solve()
    while(out is None):
        puzzle.reset()
        out = puzzle.solve()
    return out


if __name__ == "__main__":
    with open("zad_input.txt") as f, open("zad_output.txt", 'w') as out:
        line = f.readline()
        h, w = line.split(' ')
        h = int(h)
        rows_spec = []
        columns_spec = []
        for i, line in enumerate(f.readlines()):
            num = list(map(int, line.split(' ')))
            tmp = []
            if i < h:
                rows_spec.append(num)
            else:
                columns_spec.append(num)

        p = Puzzle(rows_spec, columns_spec)
        output = solve_puzzle(p)
        print(output)
        out.writelines(output)