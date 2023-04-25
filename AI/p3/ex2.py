from numpy import array, dstack, all, zeros, ones, any, where
from copy import deepcopy
from ex1 import generate_seqs, draw_puzzle

def to_file(nonogram):
    with open("zad_output.txt", "w") as out:
        output = draw_puzzle(nonogram)
        out.write(output)
    return output

def reduce_posibilities(idx, space, nonogram, is_row):
    solvable = True
    changed = False
    block = nonogram[idx, :] if is_row else nonogram[:, idx]

    updated_space = []
    # eliminate all blocks (rows or columns) that are not
    # consistent with current nonogram
    for pos in space[idx]:
        # generated row/column contains all ones from nonogram
        # and all zeros from nonogram
        if all(pos[block == 1] == 1) and all(pos[block == 0] == 0):
            updated_space.append(pos)

    if not len(updated_space):
        solvable = False

    space[idx] = updated_space.copy()
    certain_zeros = zeros(len(block), dtype="int64")
    certain_ones = ones(len(block), dtype="int64")

    # deduce certain values from possible rows/columns updates
    for possible_block in space[idx]:
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

def deduce(nonogram, rspace, cspace):
    height, width = nonogram.shape
    changed = True
    while changed:
        changed = False
        solvable = True
        for i in range(height):
            c, p = reduce_posibilities(i, rspace, nonogram, True)
            changed |= c
            solvable &= p
        for i in range(width):
            c, p = reduce_posibilities(i, cspace, nonogram, False)
            changed |= c
            solvable &= p
    return solvable


def in_progress(nonogram):
    return any(nonogram == -1)


def copy_and_set(nonogram, rspace, cspace, value, coord):
    def update_block(idx, block, space):
        updated_space = []
        for pos in space[idx]:
            if all(pos[block == 1] == 1) and all(pos[block == 0] == 0):
                updated_space.append(pos)
        return updated_space

    nonogram_copy = deepcopy(nonogram)
    cspace_copy = cspace.copy()
    rspace_copy = rspace.copy()
    nonogram_copy[tuple(coord)] = value

    x, y = coord
    rspace_copy[x] = update_block(x, nonogram_copy[x, :], rspace_copy)
    cspace_copy[y] = update_block(y, nonogram_copy[:, y], cspace_copy)
    return nonogram_copy, rspace_copy, cspace_copy


def solve(nonogram, rspace, cspace):
    while in_progress(nonogram):
        solvable = deduce(nonogram, rspace, cspace)
        if not solvable:
            return False
        # the first pixel that hasn't been touched yet
        unknown = dstack(where(nonogram == -1))[0]
        # the end
        if not len(unknown):
            to_file(nonogram)
            return True
        coord = unknown[0]
        if solve(*copy_and_set(nonogram, rspace, cspace, 1, coord)):
            return True
        nonogram[tuple(coord)] = 0


if __name__ == "__main__":
    with open("zad_input.txt") as f:
        line = f.readline()
        h, w = map(int, line.split(' '))
        rspecs = [[int(x) for x in f.readline().split()] for _ in range(h)]
        cspecs = [[int(x) for x in f.readline().split()] for _ in range(w)]

        nonogram = zeros((h, w), dtype="int64") - 1
        rspace = [array(generate_seqs(w, row)) for row in rspecs]
        cspace = [array(generate_seqs(h, column)) for column in cspecs]
        
        solve(nonogram, rspace, cspace)
