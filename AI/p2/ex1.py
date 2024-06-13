from collections import deque

from numpy import ndarray, zeros


def generate_seqs(n: int, pattern: list[int]) -> list[list[int]]:
    '''
    Generate all possible sequences of 1s and 0s of length `n`
    restricted by the pattern `pattern`, where each element on
    the list `pattern` specifies required length of 1s.
    Each sequence of 1s must be separated by at least one 0.
    '''

    if not n:
        return [[]]

    if not len(pattern):
        return [[0] * n]

    block_len = pattern[0]
    block = [1] * block_len
    new_n = n - block_len

    if len(pattern[1:]) > 0:
        block += [0]
        new_n -= 1

    # Continue the process for the rest of the pattern
    cur_seqs = [block + p for p in generate_seqs(new_n, pattern[1:])]
    required_len = sum(pattern) + len(pattern) - 1

    if required_len < n:  # adjust size by filling beginning with zeros
        return cur_seqs + [[0] + p for p in generate_seqs(n - 1, pattern)]
    else:
        return cur_seqs


def solve(rspecs: list[list[int]], cspecs: list[list[int]]) -> ndarray:
    '''
    The main idea is to generate all the possible
    rows / columns for given specification to then
    find common elements amongst them all and eliminate
    those potential solution that contradict them

    I.E. if all rows share the same value for element (x, y)
    then those columns that contradict the (x, y) cannot
    be the solution.

    We may need to go back to some of the elements therefore
    we put them on a queue to later consider them
    '''
    height, width = len(rspecs), len(cspecs)
    rspace = [generate_seqs(width, row) for row in rspecs]
    cspace = [generate_seqs(height, column) for column in cspecs]

    puzzle = zeros((height, width))  # matrix with zeros
    # Coordinates for the undetermined elements of the puzzle
    undetermined: deque[tuple[int, int]] = deque()

    def adjust_columns(y, x):
        cspace[x] = list(filter(lambda c: c[y] == puzzle[y][x], cspace[x]))

    def adjust_rows(y, x):
        rspace[y] = list(filter(lambda r: r[x] == puzzle[y][x], rspace[y]))

    def subsolve(y, x, current_rows):
        '''
        Mark the certain elements in the puzzle.

        If an element occurs in all generated
        sequences it's certain.
        '''
        rfixed = current_rows[0][x]

        # Fixed point within all the possible rows
        if all(row[x] == rfixed for row in current_rows):
            # the element is common for all possible rows,
            # therefore, it must be in the solution
            puzzle[y][x] = rfixed
            # filter out the contradictory columns
            adjust_columns(y, x)

        # Find common point for all columns
        else:
            cfixed = cspace[x][0][y]

            if all(column[y] == cfixed for column in cspace[x]):
                puzzle[y][x] = cfixed
                adjust_rows(y, x)
            else:

                undetermined.append((y, x))  # we delay this cell

    for y in range(height):
        current_rows = rspace[y]

        for x in range(width):
            subsolve(y, x, current_rows)

    while len(undetermined) > 0:
        y, x = undetermined.popleft()
        current_rows = rspace[y]
        subsolve(y, x, current_rows)

    return puzzle


def draw_puzzle(puzzle) -> str:
    out: str = ''
    for row in puzzle:
        for elem in row:
            out += '#' if elem else '.'
        out += '\n'
    return out


if __name__ == "__main__":
    with open('zad_input.txt') as f:
        content: list[str] = []
        row_specs: list[list[int]] = []
        col_specs: list[list[int]] = []

        h, w = f.readline().split(' ')
        h, w = int(h), int(w)

        for i, line in enumerate(f.readlines()):
            num = list(map(int, line.split(' ')))
            if i < h:
                row_specs.append(num)
            else:
                col_specs.append(num)

    puzzle = solve(row_specs, col_specs)
    print(draw_puzzle(puzzle))
    with open("zad_output.txt", "w") as out:
        out.write(draw_puzzle(puzzle))
