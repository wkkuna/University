#!/usr/bin/env python3
import random

directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
MAX_ITER = 300
WIDTH, HEIGHT = 7, 9
red, blue = range(2)
φ = None
# 0    1    2     3      4       5      6      7
rat, cat, dog, wolf, leopard, tiger, lion, elephant = range(8)


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

        self.counter = 0
        self.traps = {(2, 0), (4, 0), (3, 1), (3, 7), (2, 8), (4, 8)}
        self.dens = [(3, 8), (3, 0)]
        self.ponds = {(1, 3), (2, 3), (4, 3), (5, 3), (1, 4),
                      (2, 4), (4, 4), (5, 4), (1, 5), (2, 5), (4, 5), (5, 5)}
        self.pieces = {red: {}, blue: {}}

        # Keep track of the pieces
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.board[y][x]:
                    player, animal = self.board[y][x]
                    self.pieces[player][animal] = (x, y)

    # Check if opponent's rat is blocking the entrance to the pond
    def can_enter_pond(self, pos, new_pos, player):
        (x0, y0), (x1, y1) = pos, new_pos
        dx = abs(x0 - x1)
        dy = abs(y0 - y1)

        if rat not in self.pieces[opponent(player)]:
            return True

        rx, ry = self.pieces[opponent(player)][rat]

        if dx and y0 == ry and abs(x0 - rx) <= 2 and abs(x1 - rx) <= 2:
            return False

        if dy and x0 == rx:
            return False

        return True

    def is_stronger(self, curr_animal, other_animal,  pos,  new_pos):
        if pos in self.ponds and new_pos in self.ponds:
            return False
        if pos in self.ponds:
            return False
        if new_pos in self.traps:
            return True
        if curr_animal == rat and other_animal == elephant:
            return True
        if curr_animal == elephant and other_animal == rat:
            return False
        return curr_animal >= other_animal

    def possible_moves(self, player):
        moves = []
        for curr_animal, curr_pos in self.pieces[player].items():
            x, y = curr_pos
            for dx, dy in directions:
                x0, y0 = x + dx, y + dy
                new_pos = (x0, y0)

                if x0 in range(0, WIDTH) and y0 in range(0, HEIGHT):
                    # No point in going to our own den
                    if new_pos == self.dens[player]:
                        continue

                    if new_pos in self.ponds:
                        # Only rat can enter the pond
                        # Only lion and tiger can jump through the pond
                        if curr_animal not in (rat, lion, tiger):
                            continue

                        if curr_animal in [lion, tiger]:
                            # Calculate the new position after jumping
                            # through the pond
                            dx, dy = 3 * dx, 4 * dy
                            new_pos = (x + dx, y + dy)
                            # Cannot enter the pond if the rat's inside it
                            if not self.can_enter_pond(curr_pos, new_pos, player):
                                continue

                    if self.board[y0][x0]:
                        other_player, other_animal = self.board[y0][x0]
                        # If it's our piece on the new position, we cannot move there
                        if other_player == player:
                            continue
                        # If there's opponent's animal and is stronger than us there's no point
                        # moving there
                        if not self.is_stronger(curr_animal, other_animal, curr_pos, new_pos):
                            continue
                    # Otherwise, legal move
                    moves.append((curr_pos, new_pos))
        return moves

    def compare_pieces(self):
        for i in range(7, -1, -1):
            res = 0
            res -= 1 if i in self.pieces[red] else 0
            res += 1 if i in self.pieces[blue] else 0
            if res:
                return res
        return 0

    def is_over(self):
        # Any of the players is out of their pieces
        if not len(self.pieces[blue]):
            return red
        if not len(self.pieces[red]):
            return blue

        x0, y0 = self.dens[red]
        x1, y1 = self.dens[blue]
        # The den has been reached by opposing player
        if self.board[y0][x0]:
            return blue
        if self.board[y1][x1]:
            return red

        # Limit of iterations reached
        if MAX_ITER <= self.counter:
            # Give the win to the player with the strongest piece remaining
            diff = self.compare_pieces()
            return diff if diff in [red, blue] else red
        # Not terminal
        return -1

    def move(self, move):
        self.counter += 1
        # NOOP
        if not move:
            return φ

        (x, y), (nx, ny) = move

        p0, a0 = self.board[y][x]
        if self.board[ny][nx]:
            p1, a1 = self.board[ny][nx]
            del self.pieces[p1][a1]

        self.pieces[p0][a0] = (nx, ny)
        self.board[y][x] = φ
        self.board[ny][nx] = (p0, a0)
        return f"{x} {y} {nx} {ny}"

    def get_random_move(self, player):
        moves = self.possible_moves(player)
        return φ if not len(moves) else random.choice(moves)
