#!/usr/bin/env python3

from ex4 import agent_alt
from jungle import Jungle, blue, red


def make_a_move(game, player):
    move = agent_alt(game, player)
    if not move:
        (x0, y0), (x1, y1) = ((-1, -1), (-1, -1))
    else:
        (x0, y0), (x1, y1) = move
    game.move(move)
    print(f'IDO {x0} {y0} {x1} {y1}')


game = Jungle()
player = -1
print("RDY")
while True:
    line = input().split()
    cmd = line[0]

    # Our turn
    if cmd == 'UGO':
        if player == -1:
            player = red
        make_a_move(game, player)

    # Opponent moved
    if cmd == 'HEDID':
        if player == -1:
            player = blue
        x0, y0, x1, y1 = map(int, line[3:])
        # NOOP move
        if [x0, y0, x1, y1] != [-1, -1, -1, -1]:
            game.move(((x0, y0), (x1, y1)))
        make_a_move(game, player)

    # Reset
    if cmd == 'ONEMORE':
        game = Jungle()
        player = -1
        print("RDY")

    if cmd == 'BYE':
        break
