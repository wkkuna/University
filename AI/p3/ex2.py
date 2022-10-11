from numpy import array, dstack, all, zeros, ones, any, where
from copy import deepcopy


def generate(nonogram, rows_spec, columns_spec):
    def single_sequence(length, specs):
        if not length:
            return [[]]
        if not specs:
            return [[0] * length]

        block = [1] * specs[0]
        if specs[1:]:
            block += [0]
        remaining_length = length - len(block)

        # for current block append all possible tails
        current_possibilities = [
            block + tail for tail in single_sequence(remaining_length, specs[1:])]
        necessary_length = sum(specs) + len(specs) - 1

        # is it possible to append zero's at front
        return current_possibilities + [[0] + tail for tail in single_sequence(length - 1, specs)]\
            if necessary_length < length else current_possibilities
    h, w = nonogram.shape
    possible_rows = [array(single_sequence(w, rs)) for rs in rows_spec]
    possible_columns = [array(single_sequence(h, cs)) for cs in columns_spec]
    return possible_rows, possible_columns


def reduce_posibilities(idx, possibilities, nonogram, is_row):
    solvable = True
    changed = False
    block = None
    if is_row:
        block = nonogram[idx, :]
    else:
        block = nonogram[:, idx]

    updated_possibilities = []
    # eliminate all blocks (rows or columns) that are not
    # consistent with current nonogram
    for pos in possibilities[idx]:
        # generated row/column contains all ones from nonogram
        # and all zeros from nonogram
        if all(pos[block == 1] == 1) and all(pos[block == 0] == 0):
            updated_possibilities.append(pos)

    if not len(updated_possibilities):
        solvable = False

    possibilities[idx] = updated_possibilities.copy()
    certain_zeros = zeros(len(block), dtype="int64")
    certain_ones = ones(len(block), dtype="int64")

    # deduce certain values from possible rows/columns updates
    for possible_block in possibilities[idx]:
        certain_zeros |= possible_block
        certain_ones &= possible_block

    for i in range(len(block)):
        if certain_zeros[i] == 0 and block[i] == -1:
            changed = True
            block[i] = 0
        if certain_ones[i] == 1 and block[i] == -1:
            changed = True
            block[i] = 1

    if is_row:
        nonogram[idx, :] = block
    else:
        nonogram[:, idx] = block
    return changed, solvable


def to_file(nonogram):
    with open("zad_output.txt", "w") as out:
        output = ""
        for i in range(nonogram.shape[0]):
            for j in range(nonogram.shape[1]):
                output += '#' if nonogram[i][j] == 1 else '.'
            output += '\n'
        out.writelines(output)
        return output


def deduce(nonogram, possible_rows, possible_columns):
    height, width = nonogram.shape
    changed = True
    while changed:
        changed = False
        solvable = True
        for i in range(height):
            c, p = reduce_posibilities(i, possible_rows, nonogram, True)
            changed |= c
            solvable &= p
        for i in range(width):
            c, p = reduce_posibilities(i, possible_columns, nonogram, False)
            changed |= c
            solvable &= p
    return solvable


def in_progress(nonogram):
    return any(nonogram == -1)


def copy_and_set(nonogram, possible_rows, possible_columns, value, coord):
    def update_block(idx, block, posibilities):
        updated_possibilities = []
        for pos in posibilities[idx]:
            if all(pos[block == 1] == 1) and all(pos[block == 0] == 0):
                updated_possibilities.append(pos)
        return updated_possibilities

    nonogram_copy = deepcopy(nonogram)
    column_copy = possible_columns.copy()
    row_copy = possible_rows.copy()
    nonogram_copy[tuple(coord)] = value

    x, y = coord
    row = nonogram_copy[x, :]
    row_copy[x] = update_block(x, row, row_copy)
    column = nonogram_copy[:, y]
    column_copy[y] = update_block(y, column, column_copy)
    return nonogram_copy, row_copy, column_copy


def solve(nonogram, possible_rows, possible_columns):
    while in_progress(nonogram):
        solvable = deduce(nonogram, possible_rows, possible_columns)
        if not solvable:
            return False
        unknown = dstack(where(nonogram == -1))[0]
        if not len(unknown):
            to_file(nonogram)
            return True
        coord = unknown[0]
        nonogram_copy, row_copy, column_copy = copy_and_set(
            nonogram, possible_rows, possible_columns, 1, coord)
        if solve(nonogram_copy, row_copy, column_copy):
            return True
        nonogram[tuple(coord)] = 0


if __name__ == "__main__":
    with open("zad_input.txt") as f:
        line = f.readline()
        h, w = map(int, line.split(' '))
        rows_spec = [[int(x) for x in f.readline().split()] for _ in range(h)]
        columns_spec = [[int(x) for x in f.readline().split()]
                        for _ in range(w)]

        nonogram = zeros((h, w), dtype="int64") - 1
        possible_rows, possible_columns = generate(
            nonogram, rows_spec, columns_spec)
        solve(nonogram, possible_rows, possible_columns)
