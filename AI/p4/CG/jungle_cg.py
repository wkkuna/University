import copy
import random

inf = 100000
ninf = -100000

WIDTH, HEIGHT = 7, 9
red, blue = range(2)
φ = None
# 0    1    2     3      4       5      6      7
rat, cat, dog, wolf, leopard, tiger, lion, elephant = range(8)
MAX_COUNTER = 30


def get_player(color: str): return red if color == 'red' else blue


def opponent(player): return blue if player == red else red


class Jungle:
    def __init__(self):
        self.board = [[(blue, 6), φ, φ, φ, φ, φ, (blue, 5)],
                      [φ, (blue, 2), φ, φ, φ, (blue, 1), φ],
                      [(blue, 0), φ, (blue, 4), φ, (blue, 3), φ, (blue, 7)],
                      [φ, φ, φ, φ, φ, φ, φ],
                      [φ, φ, φ, φ, φ, φ, φ],
                      [φ, φ, φ, φ, φ, φ, φ],
                      [(red, 7), φ, (red, 3), φ, (red, 4), φ, (red, 0)],
                      [φ, (red, 1), φ, φ, φ, (red, 2), φ],
                      [(red, 5), φ, φ, φ, φ, φ, (red, 6)]]

        self.traps = {(2, 0), (4, 0), (3, 1), (3, 7), (2, 8), (4, 8)}
        self.dens = [(3, 8), (3, 0)]
        self.ponds = {(1, 3), (2, 3), (4, 3), (5, 3), (1, 4),
                      (2, 4), (4, 4), (5, 4), (1, 5), (2, 5), (4, 5), (5, 5)}
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.pieces = {red: {}, blue: {}}
        self.counter = 0

        # Keep track of the pieces
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.board[y][x]:
                    player, animal = self.board[y][x]
                    self.pieces[player][animal] = (x, y)

    def is_rat_blocking(self, start_pos, end_pos, player):
        (x0, y0), (x1, y1) = start_pos, end_pos
        dx = abs(x0 - x1)
        dy = abs(y0 - y1)

        if rat not in self.pieces[opponent(player)]:
            return False

        rx, ry = self.pieces[opponent(player)][rat]

        if dx and y0 == ry and abs(x0 - rx) <= 2 and abs(x1 - rx) <= 2:
            return True

        if dy and x0 == rx:
            return True

        return False

    def can_beat(self, animal0, pos0, animal1, pos1):
        if pos0 in self.ponds and pos1 in self.ponds:
            return False
        if pos0 in self.ponds:
            return False
        if pos1 in self.traps:
            return True
        if animal0 == rat and animal1 == elephant:
            return True
        if animal0 == elephant and animal1 == rat:
            return False
        if animal0 >= animal1:
            return True
        return False

    def possible_moves(self, player):
        moves = []
        for animal0, pos in self.pieces[player].items():
            x, y = pos
            for dx, dy in self.directions:
                x0, y0 = x + dx, y + dy
                new_pos = (x0, y0)

                if x0 in range(0, WIDTH) and y0 in range(0, HEIGHT):
                    if self.dens[player] == new_pos:
                        continue
                    if new_pos in self.ponds:
                        if animal0 not in (rat, lion, tiger):
                            continue

                        if animal0 in (lion, tiger):
                            dx *= 3
                            dy *= 4
                            new_pos = (x + dx, y + dy)
                            if self.is_rat_blocking(pos, new_pos, player):
                                continue

                    if self.board[y0][x0]:
                        player1, animal1 = self.board[y0][x0]
                        if player1 == player:
                            continue
                        if not self.can_beat(animal0, pos, animal1, new_pos):
                            continue
                    moves.append((pos, new_pos))
        return moves

    def piece_comparison(self):
        for i in range(7, -1, -1):
            res = 0
            res -= 1 if i in self.pieces[red] else 0
            res += 1 if i in self.pieces[blue] else 0
            if res:
                return res
        return 0

    def is_terminal(self):
        # Any of the players is out of their pieces
        if not len(self.pieces[1]):
            return 0
        if not len(self.pieces[0]):
            return 1

        x0, y0 = self.dens[0]
        x1, y1 = self.dens[1]
        if self.board[y0][x0]:
            return blue
        if self.board[y1][x1]:
            return red

        if MAX_COUNTER <= self.counter:
            diff = self.piece_comparison()
            return diff if diff in [red, blue] else red
        # not terminal
        return -1

    def move(self, move):
        if not move:
            return φ
        (x, y), (nx, ny) = move

        p1, a1 = self.board[y][x]
        if self.board[ny][nx]:
            p2, a2 = self.board[ny][nx]
            del self.pieces[p2][a2]
            self.counter = 0
        else:
            self.counter += 1

        self.pieces[p1][a1] = (nx, ny)
        self.board[y][x] = φ
        self.board[ny][nx] = (p1, a1)
        return f"{x} {y} {nx} {ny}"

    def get_random_move(self, player):
        moves = self.possible_moves(player)
        if not len(moves):
            return None
        return random.choice(moves)


def manhattan_dist(pos0, pos1):
    (x0, y0), (x1, y1) = pos0, pos1
    return abs(x0 - x1) + abs(y0 - y1)


def heuristic(game, player):
    enemy_den = game.dens[opponent(player)]
    res = sum(manhattan_dist(pos, enemy_den)
              for (_, pos) in game.pieces[player].items())
    return 150 - res


def alpha_beta(game, player, depth):
    alpha = ninf
    beta = inf

    _, best_move = alpha_beta_search(
        game, player, depth, alpha, beta, player)
    return best_move

def alpha_beta_search(game, player, depth, alpha, beta, starting_player):
    win = game.is_terminal()
    if win != -1 or depth == 0:
        return (heuristic(game, starting_player), None)

    best_move = None
    moves = game.possible_moves(player)
    if moves == None:
        moves = [None]

    if player == blue:
        best_result = ninf
        for move in moves:
            new_game = copy.deepcopy(game)
            new_game.move(move)

            result, m = alpha_beta_search(
                new_game, opponent(player), depth - 1, alpha, beta, starting_player)
            if result > best_result:
                best_result = result
                best_move = move
            alpha = max(alpha, best_result)

            if alpha >= beta:
                break

        return (best_result, best_move)
    else:
        best_result = inf
        for move in moves:
            new_game = copy.deepcopy(game)
            new_game.move(move)

            result, _ = alpha_beta_search(
                new_game, opponent(player), depth - 1, alpha, beta, starting_player)

            if result < best_result:
                best_move = move
                best_result = result
            beta = min(beta, best_result)

            if alpha >= beta:
                break

        return (best_result, best_move)


color = input()  # color of your player ("red" or "blue")
player = get_player(color)
game = Jungle()

# game loop
while True:
    x_1, y_1, x_2, y_2 = [int(i) for i in input().split()]
    if [x_1, y_1, x_2, y_2] != [-1, -1, -1, -1]:
        game.move(((x_1, y_1), (x_2, y_2)))
    move_count = int(input())  # number of legal moves
    legal_moves = []
    for i in range(move_count):
        x1, y1, x2, y2 = map(int, input().split(' '))
        legal_moves.append(((x1, y1), (x2, y2)))

    best = alpha_beta(game, player, 4)
    # score = 0
    # for move in legal_moves:
    #     new_game = copy.deepcopy(game)
    #     new_game.move(move)
    #     if heuristic(new_game, player) > score:
    #         score = heuristic(new_game, player)
    #         best = move

    move = best if best else random.choice(legal_moves)
    game.move(move)
    (x1, y1), (x2, y2) = move  # unwrap
    print(f"{x1} {y1} {x2} {y2}")
