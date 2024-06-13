import math
import time

from ex1 import Reversi, random_move_non_cache
from tqdm import tqdm


class Node:
    def __init__(self, game, parent, player):
        self.game = game
        self.parent = parent
        self.player = player
        self.children = []
        self.expanded = False
        self.is_terminal = False
        self.wins = 0
        self.games = 0
        self.move = None


class MCTS:
    def __init__(self, game, player):
        self.root = Node(game, None, player)

    # Upper confidence bound
    def get_ucb(self, node):
        if node.games == 0:
            return float('inf')
        return node.wins / node.games + math.sqrt(2 * math.log(node.parent.games) / node.games)

    def select(self):
        selected = self.root

        while selected.expanded:
            if selected.is_terminal:
                return selected

            selected = sorted(selected.children, key=self.get_ucb, reverse=True)[0]

        return selected

    def expand(self, node):
        game = node.game
        node.expanded = True

        if game.terminal():
            node.is_terminal = True
            node.children = [node]
        else:
            moves = game.get_moves_non_cache()
            if moves is None:
                moves = [None]

            for move in moves:
                new_game = game.copy()
                new_game.move(move)
                new_node = Node(new_game, node, 1 - node.player)
                new_node.move = move

                node.children.append(new_node)

    def simulate(self, node):
        game = node.game.copy()
        player = node.player

        while not game.terminal():
            move = random_move_non_cache(game)
            game.move(move)
            player = 1 - player

        if (game.difference() > 0 and self.root.player == 1) or (game.difference() < 0 and self.root.player == 0):
            return 1
        return 0

    def backpropagate(self, node, result):
        node.games += 1
        node.wins += result

        if node.parent is not None:
            self.backpropagate(node.parent, result)

    def get_move(self, max_iterations):
        for _ in range(max_iterations):
            selected = self.select()
            self.expand(selected)

            for child in selected.children:
                result = 0
                for _ in range(1):
                    result += self.simulate(child)

                self.backpropagate(child, result / 1)

        best = 0
        best_move = None

        for child in self.root.children:
            if child.games > best:
                best = child.games
                best_move = child.move

        return best_move


if __name__ == "__main__":
    wins = 0
    rnd_player = 1
    mcst_player = 0
    mcts_max_iterations = 10
    num_of_games = 6

    for _ in tqdm(range(int(num_of_games / 2))):
        game = Reversi()
        player = 1
        mcst_moved = False
        mcst = MCTS(game, player)

        while True:
            if player == rnd_player:
                move = random_move_non_cache(game)
            else:
                if not mcst_moved:
                    mcst = MCTS(game, player)

                start_time = time.time()
                move = mcst.get_move(mcts_max_iterations)
                print(
                    (f"Win ratio: {round(mcst.root.wins / mcst.root.games, 3)} "
                     f"Won:{int(mcst.root.wins)}/{mcst.root.games} --- "
                     f"in {(time.time() - start_time)} s"))
                mcst_moved = True
            mcst.root = next((child for child in mcst.root.children if child.move == move), None)
            game.move(move)
            player = 1 - player

            if game.terminal():
                if game.winner() == mcst_player:
                    wins += 1
                # DRAW
                elif game.winner() == -1:
                    wins += 0.5
                break

    rnd_player = 0
    mcst_player = 1
    for _ in tqdm(range(int(num_of_games / 2))):
        game = Reversi()
        player = 1
        mcst_moved = False
        mcst = MCTS(game, player)

        while True:
            if player == rnd_player:
                move = random_move_non_cache(game)
            else:
                if not mcst_moved:
                    mcst = MCTS(game, player)

                start_time = time.time()
                move = mcst.get_move(mcts_max_iterations)
                print(
                    (f"Win ratio: {round(mcst.root.wins / mcst.root.games, 3)} "
                     f"Won:{int(mcst.root.wins)}/{mcst.root.games} --- "
                     f"in {(time.time() - start_time)} s"))
                mcst_moved = True
            mcst.root = next((child for child in mcst.root.children if child.move == move), None)
            game.move(move)
            player = 1 - player

            if game.terminal():
                if game.winner() == mcst_player:
                    wins += 1
                # DRAW
                elif game.winner() == -1:
                    wins += 0.5
                break

    print(f"Tournament MCST wins: {wins}/{num_of_games}")
