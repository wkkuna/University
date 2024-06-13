from random import choice

from tqdm import tqdm
from util import Pos, timeit

possible_moves = {}


class Reversi:
    def __init__(self):
        self.turn, self.other = 0, 1
        self.W, self.H = 8, 8
        self.dirs = [Pos(x, y) for x in range(-1, 2)
                     for y in range(-1, 2) if (x, y) != (0, 0)]
        self.history = []
        self.history_ends = []
        self.board = [[None for _ in range(self.H)] for _ in range(self.W)]
        self.board[4][4] = 1
        self.board[3][3] = 1
        self.board[4][3] = 0
        self.board[3][4] = 0
        self.tiles = set(Pos(x, y) for x in range(self.W)
                         for y in range(self.W) if self.board[y][x] is None)

    def __getitem__(self, pos):
        if 0 <= pos[0] < self.W and 0 <= pos[1] < self.H:
            return self.board[pos[1]][pos[0]]
        return None

    def __setitem__(self, pos, val):
        self.board[pos[1]][pos[0]] = val

    def copy(self):
        cp = Reversi()
        cp.turn, cp.other = self.turn, self.other
        cp.history = self.history.copy()
        cp.history_ends = self.history_ends
        cp.board = [row.copy() for row in self.board]
        cp.tiles = self.tiles.copy()
        return cp

    def captures(self, pos, d):
        pos = pos.copy() + d
        flipped = False
        while self[pos] == self.other:
            pos += d
            flipped = True
        return flipped and self[pos] == self.turn

    def switch_turn(self):
        self.turn, self.other = self.other, self.turn

    def get_moves(self):
        global possible_moves
        h = self.hash()+self.turn
        if h in possible_moves:
            return possible_moves[h]
        moves = []
        for pos in self.tiles:
            if any(self.captures(pos, d) for d in self.dirs):
                moves.append(pos)
        if len(possible_moves) < 10000000:
            possible_moves[h] = moves
        if not moves:
            return [None]

        return moves

    def get_moves_non_cache(self):
        moves = []

        for pos in self.tiles:
            if (any(self.captures(pos, direction) for direction in self.dirs)):
                moves.append(pos)
        if not moves:
            return None
        return moves

    def get_opp_moves(self):
        global possible_moves
        h = self.hash()+self.other
        if h in possible_moves:
            return possible_moves[h]
        moves = []
        self.switch_turn()
        for pos in self.tiles:
            if any(self.captures(pos, d) for d in self.dirs):
                moves.append(pos)
        self.switch_turn()
        if len(possible_moves) < 10000000:
            possible_moves[h] = moves
        return moves

    def get_stable(self, player):
        stable = set()
        directions = [Pos(1, 0), Pos(0, 1), Pos(-1, 0), Pos(0, -1)]

        for row in [0, 7]:
            for col in [0, 7]:
                if self[row, col] == player:
                    stable.add(Pos(row, col))
                    for direction in directions:
                        pos = Pos(row, col) + direction
                        while self[pos] == player:
                            stable.add(pos)
                            pos += direction

        return stable

    def sim(self, history):
        for move in history:
            self.move(move)

    def move(self, pos):
        if pos is None:
            self.switch_turn()
            self.history.append(None)
            self.history_ends.append(None)
            return
        self.tiles.remove(pos)
        to_flip = []
        ends = []
        for d in self.dirs:
            npos = pos + d
            counter = 0
            while self[npos] == self.other:
                to_flip.append(npos)
                npos = npos+d
                counter += 1
            if self[npos] != self.turn and counter > 0:
                to_flip = to_flip[:-counter]
                npos = pos+d
            ends.append(npos)
        self.history.append(pos)
        self.history_ends.append(ends)
        for p in to_flip:
            self[p] = self.turn
        self[pos] = self.turn
        self.switch_turn()

    def undo(self):
        pos = self.history.pop()
        ends = self.history_ends.pop()
        self.switch_turn()
        if pos is None:
            return
        self.tiles.add(pos)
        self[pos] = None
        for d, end in zip(self.dirs, ends):
            npos = pos + d
            while npos != end:
                self[npos] = self.other
                npos += d

    def terminal(self):
        if not len(self.tiles):
            return True

        if len(self.history) < 8:
            return False

        if sum(1 for move in self.history if move is not None) >= 60:
            return True

        return not self.history[-1] and not self.history[-2]

    def difference(self):
        return sum(1 if self[x, y] == 1 else -1 if self[x, y] == 0 else 0 for x in range(self.H) for y in range(self.W))

    def winner(self):
        diff = self.difference()
        return diff // abs(diff) if diff != 0 else -1

    def draw(self):
        for y in range(self.H):
            for x in range(self.W):
                print('.' if self.board[y][x] is None else self.board[y][x], end='')
            print()
        print()

    def hash(self):
        return hash(''.join('.' if self.board[y][x] is None else str(self.board[y][x])
                            for x in range(self.W) for y in range(self.H)))


def random_move(board):
    r = board.get_moves()
    return None if not r else choice(r)


def random_move_non_cache(board):
    r = board.get_moves_non_cache()
    return None if not r else choice(r)


def heuristic(board: Reversi):
    values = [[20, -3, 11, 8, 8, 11, -3, 20],
              [-3, -7, -4, 1, 1, -4, -7, -3],
              [11, -4, 2, 2, 2, 2, -4, 11],
              [8, 1, 2, -3, -3, 2, 1, 8],
              [8, 1, 2, -3, -3, 2, 1, 8],
              [11, -4, 2, 2, 2, 2, -4, 11],
              [-3, -7, -4, 1, 1, -4, -7, -3],
              [20, -3, 11, 8, 8, 11, -3, 20]]

    positioning_weight = 0.1
    mobility_weight = 0.2
    domination_weight = 1
    stability_weight = 100

    positioning, mobility, domination, stability = 0, 0, 0, 0

    # Prioritize the corners
    if len(board.history) < 20:
        for y in range(8):
            for x in range(8):
                if board[x, y] == 1:
                    positioning += values[y][x]
                elif board[x, y] == 0:
                    positioning -= values[y][x]

    # Number of available moves vs number of available opponent moves
    if len(board.history) < 55:
        mobility = (len(board.get_moves()) -
                    len(board.get_opp_moves()))*(2*board.turn-1)

    # Difference in points
    if len(board.history) > 54:
        domination = board.difference()

    # Non-flippable coins
    if len(board.history) < 54:
        stability = len(board.get_stable(1)) - len(board.get_stable(0))

    return positioning*positioning_weight + mobility*mobility_weight +\
        domination*domination_weight + stability*stability_weight


def alphabeta(board, depth, turn, other, alpha=float('-inf'), beta=float('inf'), original=False):
    if board.terminal():
        diff = board.difference()
        return -10000000 if diff > 0 else 10000000 if diff < 0 else 0

    if depth == 0:
        return heuristic(board)

    best = float('-inf') if turn == 1 else float('inf')
    best_move = None

    for mv in board.get_moves():
        board.move(mv)
        value = alphabeta(board, depth - 1, other, turn, alpha, beta)
        board.undo()

        if (turn == 1 and value > best) or (turn != 1 and value < best):
            best = value
            best_move = mv

        if turn == 1:
            alpha = max(alpha, best)
            if alpha >= beta:
                break
        else:
            beta = min(beta, best)
            if alpha >= beta:
                break

    if original:
        return best, best_move
    return best


@timeit
def alphabeta_move(board, depth=2):
    moves = board.get_moves()
    if not len(moves):
        return None
    return alphabeta(board, depth, turn=board.turn, other=board.other, original=True)[1]


if __name__ == '__main__':
    timeit('START')

    max_wins, min_wins = 0, 0
    diffs = []
    players = (random_move, alphabeta_move)
    for _ in tqdm(range(1000)):
        game = Reversi()
        for turn in range(70):
            mv = players[turn % 2](game)
            game.move(mv)
            if game.terminal():
                break
            # game.draw()
        if game.difference() > 0:
            max_wins += 1
        else:
            min_wins += 1
        diffs.append(game.difference())
    print(max_wins, min_wins)

    timeit('SHOW')
