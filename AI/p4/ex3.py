#!/usr/bin/env python3
import copy

from jungle import Jungle, blue, opponent, red


def get_agent_move(game, n, agent):
    moves = game.possible_moves(agent)
    possible_results = []

    for move in moves:
        wins, games = 0, 0

        new_game = copy.deepcopy(game)
        new_game.move(move)
        curr_player = opponent(agent)

        for _ in range(n // len(moves)):
            win = new_game.is_over()
            # Game over
            if win != -1:
                games += 1
                wins += 1 if win == agent else 0

                new_game = copy.deepcopy(game)
                new_game.move(move)
                curr_player = opponent(agent)

            new_move = new_game.get_random_move(curr_player)
            new_game.move(new_move)

            curr_player = opponent(curr_player)

        score = 0 if not games else wins / games
        possible_results.append((move, score))

    # Pick a move with highest wining ratio
    return max(possible_results, key=lambda i: i[1])[0]


if __name__ == '__main__':
    MAX_MOVES = 20000
    game = Jungle()
    player = blue
    win = game.is_over()
    while win == -1:
        if player == blue:
            move = game.get_random_move(player)
            game.move(move)
        if player == red:
            move = get_agent_move(game, MAX_MOVES, player)
            game.move(move)

        win = game.is_over()
        player = opponent(player)

    print(f"Winner: {'Agent' if win == 0 else 'Random'}")
