from random import choice, randint
from time import time


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
        if x != None:
            return ('1' * self.rows_spec[x] in "".join(str(e) for e in self.puzzle[x]))\
                and (sum(self.puzzle[x]) == self.rows_spec[x])

        if y != None:
            column = [self.puzzle[x][y] for x in range(self.height)]
            valid = ('1' * self.columns_spec[y] in "".join([str(x) for x in column]))\
                and (sum(column) == self.columns_spec[y])
            return valid

        for i in range(self.height):
            if not self.is_valid(x=i) or not self.is_valid(y=i):
                return False
        return True

    def reset(self):
        self.puzzle = [[0 for y in range(self.width)]
                       for x in range(self.height)]

    def solve(self):
        t0 = 0
        limit = self.height*self.width*5

        def pick_row():
            invalid_rows = []
            for i in range(self.width):
                if not self.is_valid(x=i):
                    invalid_rows.append(i)

            if len(invalid_rows) == 0:
                return None

            return choice(invalid_rows)

        def pick_column():
            invalid_columns = []
            for i in range(self.height):
                if not self.is_valid(y=i):
                    invalid_columns.append(i)

            if len(invalid_columns) == 0:
                return None

            return choice(invalid_columns)

        def opt_dist(idx, D, is_row):
            bits = []
            min_cost = self.width

            bits = self.puzzle[idx] if is_row else [
                self.puzzle[x][idx] for x in range(self.height)]
            ones = [i for i in range(len(bits)) if bits[i] == 1]

            if not len(ones):
                return D

            n = len(bits)
            for fst in ones:
                if fst+D > n:
                    break
                min_cost = min(D - sum(bits[fst:fst+D]) +
                               sum(bits[:fst]) + sum(bits[fst+D:]), min_cost)

            return min_cost

        def switch(i, j):
            self.puzzle[i][j] = 0 if self.puzzle[i][j] else 1

        def get_opt_element(idx, is_row=True):
            best_fit = -self.width
            opt_elem = None

            for i in range(self.height):
                row_idx = idx if is_row else i
                column_idx = i if is_row else idx

                op0 = opt_dist(row_idx, self.rows_spec[row_idx], True)\
                    + opt_dist(column_idx,
                               self.columns_spec[column_idx], False)

                switch(row_idx, column_idx)

                ops = opt_dist(row_idx, self.rows_spec[row_idx], True)\
                    + opt_dist(column_idx,
                               self.columns_spec[column_idx], False)

                if op0 - ops > best_fit:
                    best_fit = op0 - ops
                    opt_elem = (row_idx, column_idx)

                switch(row_idx, column_idx)
            return opt_elem

        while (not self.is_valid() and t0 < limit):
            pick = pick_row()
            elem = None

            if pick is None or t0 % 2:
                pick = pick_column()
                if pick is not None:
                    elem = get_opt_element(pick, is_row=False)
            else:
                elem = get_opt_element(pick)

            if elem is None:
                switch(randint(0, self.width-1), randint(0, self.height-1))
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
    with open("zad5_input.txt") as f, open("zad5_output.txt", 'w') as out:
        line = f.readline()
        h, w = line.split(' ')
        rows_spec = []
        columns_spec = []
        for i, line in enumerate(f.readlines()):
            num = int(line.strip())
            if i < int(h):
                rows_spec.append(num)
            else:
                columns_spec.append(num)
        p = Puzzle(rows_spec, columns_spec)
        output = solve_puzzle(p)
        print(output)
        out.writelines(output)
