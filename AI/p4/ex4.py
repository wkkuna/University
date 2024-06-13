import copy

from ex3 import get_agent_move
from jungle import Jungle, blue, opponent, red
from tqdm import tqdm


def manhattan_dist(pos0, pos1):
    (x0, y0), (x1, y1) = pos0, pos1
    return abs(x0 - x1) + abs(y0 - y1)


# Brute force to the den (prioritize the distance from opponents den)
def heuristic(game, player):
    enemy_den = game.dens[opponent(player)]
    res = sum(manhattan_dist(pos, enemy_den)
              for (_, pos) in game.pieces[player].items())
    return 100 - res


def agent_alt(game, player):
    best_move = None
    score = 0
    for move in game.possible_moves(player):
        new_game = copy.deepcopy(game)
        new_game.move(move)
        if heuristic(new_game, player) > score:
            score = heuristic(new_game, player)
            best_move = move
    return best_move


if __name__ == '__main__':
    MAX_MOVES = 20000
    num_of_games = 10
    wins = 0

    for _ in tqdm(range(int(num_of_games))):
        game = Jungle()
        player = red

        if num_of_games % 2:
            player = blue

        win = game.is_over()
        while win == -1:
            if player == blue:
                move = get_agent_move(game, MAX_MOVES, player)
                game.move(move)

            if player == red:
                game.move(agent_alt(game, player))

            win = game.is_over()
            player = opponent(player)

        wins += win == red

    print(f"Success ratio: {wins} / {num_of_games}\n")
