#import numpy as np
from queue import Queue

class Puzzle:
    def __init__(self, rows_spec, columns_spec):
        self.rows_spec = rows_spec
        self.columns_spec = columns_spec
        self.width = len(columns_spec)
        self.height = len(rows_spec)
        self.possible_rows = [self.generate(self.width, row_spec) for row_spec in self.rows_spec]
        self.possible_columns = [self.generate(self.height, column_spec) for column_spec in self.columns_spec]
        
    def draw_puzzle(self):
        output = ""
        for i in range(self.height):
            for j in range(self.width):
                output += '#' if self.possible_rows[i][0][j] == 1 else '.'
            output += '\n'
        return output
    
    def fill_overlap(self, dim, specs):
        seq = [0]*dim
        for i, spec in enumerate(specs):
            sum_left = sum(specs[:i]) + i
            sum_right = sum(specs[i+1:]) + len(specs) - i - 1
            x0 = sum_left
            x1 = dim - sum_right
            diff = x1 - x0 - spec
            for j in range(x0 + diff, x1 - diff):
                seq[j] = 1
        return seq

    # generate possible rows or columns
    def generate(self, length, specs):
        if not length:
            return [[]]
        if not specs:
            return [[0] * length]

        block = [1] * specs[0]
        if specs[1:]:
            block += [0]
        remaining_length = length - len(block)
        
        # for current block append all possible tails
        current_possibilities = [block + tail for tail in self.generate(remaining_length, specs[1:])]
        necessary_length = sum(specs) + len(specs) - 1

        # is it possible to append zero's at front
        return current_possibilities + [[0] + tail for tail in self.generate(length - 1, specs)]\
               if necessary_length < length else current_possibilities
 
    def solve(self):
        steps = Queue()
        for y in range(self.height):
            for x in range(self.width):
                steps.put((x, y))

        # change bits until all are deduced
        while not steps.empty():
            x, y = steps.get()
            if not self.reduce_posibilities(x, y):
                steps.put((x, y))

    # if bit's value is the same throught row/column the corresponding column/row 
    # without said value should not be considered 
    def reduce_posibilities(self, x, y):
        bit = self.possible_rows[y][0][x]
        if all(row[x] == bit for row in self.possible_rows[y]):
            self.possible_columns[x] = [column for column in self.possible_columns[x] if column[y] == bit]
            return True
            
        bit = self.possible_columns[x][0][y]
        if all(column[y] == bit for column in self.possible_columns[x]):
            self.possible_rows[y] = [row for row in self.possible_rows[y] if row[x] == bit]
            return True
        return False

if __name__ == "__main__":
    with open("zad_input.txt") as f, open("zad_output.txt", 'w') as out:
        line = f.readline()
        h, w = map(int, line.split(' '))
        rows_spec = [[int(x) for x in f.readline().split()] for _ in range(h)]
        columns_spec = [[int(x) for x in f.readline().split()] for _ in range(w)]

        p = Puzzle(rows_spec, columns_spec)
        p.solve()
        output = p.draw_puzzle()
        print(output)
        out.writelines(output)