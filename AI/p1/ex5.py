# As stated in task description
# We randomly select row/column in which we're
# going to make changes, then flip the bit that
# is going to minimize the `opt_dist` that is
# that is best for our current situation

# I alter between modifying column/row as I think
# it gets me the result quicker
from random import choice, randint


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
                c = '#' if self.puzzle[i][j] == 1 else '.'
                output += c
            output += '\n'
        return output

    def opt_dist(self, idx, D, is_row):
        bits = []
        min_cost = self.width
        bits = self.puzzle[idx] if is_row else [
            self.puzzle[x][idx] for x in range(self.height)]
        for i in range(len(bits) - D + 1):
            min_cost = min(D - sum(bits[i:i+D]) +
                           sum(bits[:i]) + sum(bits[i+D:]), min_cost)
        return min_cost

    def is_valid(self, x=None, y=None):
        if x is not None:
            return self.opt_dist(x, rows_spec[x], True) == 0

        if y is not None:
            return self.opt_dist(y, columns_spec[y], False) == 0

        for i in range(self.height):
            if not self.is_valid(x=i) or not self.is_valid(y=i):
                return False
        return True

    def reset(self):
        self.puzzle = [[0 for _ in range(self.width)]
                       for _ in range(self.height)]

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

        def flip(i, j):
            self.puzzle[i][j] = not self.puzzle[i][j]

        def get_opt_element(idx, is_row=True):
            best_fit = -self.width
            opt_elem = None

            for i in range(self.height):
                ridx = idx if is_row else i
                cidx = i if is_row else idx

                # Cost before altering the bit
                op0 = self.opt_dist(ridx, self.rows_spec[ridx], True)\
                    + self.opt_dist(cidx, self.columns_spec[cidx], False)

                flip(ridx, cidx)

                # Cost after altering the bit
                op1 = self.opt_dist(ridx, self.rows_spec[ridx], True)\
                    + self.opt_dist(cidx, self.columns_spec[cidx], False)

                if op0 - op1 > best_fit:
                    best_fit = op0 - op1
                    opt_elem = (ridx, cidx)

                flip(ridx, cidx)
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

            # Flip anything at random if we didn't find anything
            if elem is None:
                flip(randint(0, self.width-1), randint(0, self.height-1))
            else:
                flip(elem[0], elem[1])
            t0 += 1

        if not self.is_valid():
            return None

        return self.draw_puzzle()


def solve_puzzle(puzzle):
    out = puzzle.solve()
    while (out is None):
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
