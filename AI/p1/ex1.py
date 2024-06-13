import argparse
from collections import deque
from enum import IntEnum
from itertools import product

# All the chess pieces positions that we've considered
state = {}

# Dictionary containing references to the previous positions of chess pieces on the chessboard
# This is used to then reconstruct the moves that lead to the mat
move_seq = {}

# List of yet-to-consider possible moves used to generate new states
to_visit = []

_valid_board_fields = [[x, y] for (x, y) in product(range(8), range(8))]

# Used to generate new kings positions
dxy_range = [-1, 0, 1]
directions = list(product(dxy_range, dxy_range))
directions.remove((0, 0))


class Player(IntEnum):
    WHITE = 0
    BLACK = 1


def print_chessboard(bk, wk, wr):
    out = "   A B C D E F G H\n"
    for i in reversed(range(8)):
        out += f'{i+1} '
        for j in range(8):
            if [i, j] == wk:
                out += 'WK'
            elif [i, j] == wr:
                out += 'WR'
            elif [i, j] == bk:
                out += 'BK'
            elif (i + j) % 2:
                out += '⬜'
            else:
                out += '⬛'
        out += '\n'
    if args.debug:
        print(out)


# Hash chess positions (so that we can use a queue)
def hsh(bk, wk, wr):
    return str((bk, wk, wr))


# Is entering field p1(2) certain death from p2(1)
def is_capture_field(p1, p2):
    return abs(p1[0] - p2[0]) <= 1 and abs(p1[1] - p2[1]) <= 1


def valid_new_bk(bk, wk, wr, state):
    # If it's taken it's taken
    if bk == wk or bk == wr:
        return False

    # Cannot go outside the chessboard
    if bk not in _valid_board_fields:
        return False

    # We don't enter check field
    if is_capture_field(wk, bk) or bk[0] == wr[0] or bk[1] == wr[1]:
        return False

    # No point running in circles
    if hsh(bk, wk, wr) in state:
        return False

    return True


def valid_new_wk(bk, wk, wr, state):
    # This field is already taken
    if wk == bk or wk == wr:
        return False

    # Cannot go outside the chessboard
    if wk not in _valid_board_fields:
        return False

    # We don't want to give up the game
    if is_capture_field(wk, bk):
        return False

    # We've already considered it
    if hsh(bk, wk, wr) in state:
        return False

    return True


def valid_new_wr(bk, wk, wr, state):
    # This field is taken
    if wr == bk or wr == wk:
        return False

    # No going overboard
    if wr not in _valid_board_fields:
        return False

    # We don't feel like giving up the rook
    if is_capture_field(wr, bk):
        return False

    # Already considered
    if hsh(bk, wk, wr) in state:
        return False

    return True


def is_mat(bk, wk, wr):
    # Corner cases
    corner_cases = {
        (0, 0): [((1, 2), wr[1]), ((2, 1), wr[0])],
        (7, 0): [((6, 2), wr[1]), ((5, 1), wr[0])],
        (0, 7): [((1, 5), wr[1]), ((2, 6), wr[0])],
        (7, 7): [((6, 5), wr[1]), ((5, 6), wr[0])]
    }

    if tuple(bk) in corner_cases:
        for pos, rook_col in corner_cases[tuple(bk)]:
            if wk == pos and wr[1] == rook_col:
                return True

    # Wall cases
    if bk[0] in [0, 7] and abs(bk[0] - wk[0]) == 2 and bk[1] == wk[1] and bk[0] == wr[0]:
        return True

    if bk[1] in [0, 7] and abs(bk[1] - wk[1]) == 2 and bk[0] == wk[0] and bk[1] == wr[1]:
        return True

    return False


# Create all the necessary references for the new state
def add_new_state(new_bk, new_wk, new_wr, bk, wk, wr, turn):
    global state, move_seq, to_visit

    # Mark so that we don't proceed to consider this state once again
    state.add(hsh(new_bk, new_wk, new_wr))

    # Create the previous state entry for our new state
    move_seq[hsh(new_bk, new_wk, new_wr)] = hsh(bk, wk, wr)

    # Consider how we can go further
    to_visit.append([new_bk, new_wk, new_wr, turn])


def generate_states(turn, bk, wk, wr):
    global state, move_seq, to_visit
    move_seq = {}
    to_visit = deque([[bk, wk, wr, turn]])
    state = {hsh(bk, wk, wr)}
    start_pos = (bk, wk, wr)

    while not (turn == Player.BLACK and is_mat(bk, wk, wr)):
        bk, wk, wr, turn = to_visit.popleft()

        if turn == Player.WHITE:
            # generate all new possible position for white pieces
            for dx, dy in directions:
                new_wk = [wk[0] + dx, wk[1] + dy]
                if valid_new_wk(bk, new_wk, wr, state):
                    add_new_state(bk, new_wk, wr, bk, wk, wr, Player.BLACK)

            # There's no point considering positions other than the corner ones since
            # the mat can only occur when black king is in the corner or at the walls
            for new_wr in [[wr[0], 0], [wr[0], 7], [0, wr[1]], [7, wr[1]]]:
                if valid_new_wr(bk, wk, new_wr, state):
                    add_new_state(bk, wk, new_wr, bk, wk, wr, Player.BLACK)

        else:
            for dx, dy in directions:
                new_bk = [bk[0] + dx, bk[1] + dy]
                if valid_new_bk(new_bk, wk, wr, state):
                    add_new_state(new_bk, wk, wr, bk, wk, wr, Player.WHITE)
    # Finish
    return restore_moves((bk, wk, wr), start_pos, move_seq)


def restore_moves(end_pos, start_pos, moves):
    curr_pos = str(end_pos)
    start_pos = str(start_pos)
    stack = []

    while curr_pos != start_pos:
        stack.append(curr_pos)
        curr_pos = moves[curr_pos]
    stack.append(curr_pos)

    for p in list(reversed(stack)):
        print_chessboard(*eval(p))
    return len(stack) - 1


def encode(position):
    return [ord(position[0]) - ord('a'), int(position[1]) - 1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Minimum moves to mat whites')
    parser.add_argument('--debug', action=argparse.BooleanOptionalAction,
                        help='Debug option for visualization')
    args = parser.parse_args()

    with open("zad1_input.txt") as f, open("zad1_output.txt", "w") as out:
        for line in f.readlines():
            line = line.strip().split(' ')
            turn = Player.WHITE if line[0] == 'white' else Player.BLACK
            wk, wr, bk = list(map(encode, line[1:]))
            out.write(str(generate_states(turn, bk, wk, wr)))
