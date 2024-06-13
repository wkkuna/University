#!/usr/bin/env python3
from ex1 import Pos, Reversi, alphabeta_move

game = Reversi()
print("RDY")
while True:
    depth = 3
    line = input().split()
    cmd = line[0]

    if cmd == 'UGO':
        mv = alphabeta_move(game, depth)

        if mv is None:
            print('IDO -1 -1')
        else:
            print('IDO {mv.x} {mv.y}')

        game.move(mv)

    if cmd == 'HEDID':
        x, y = map(int, line[3:])

        # NOOP move
        if [x, y] != [-1, -1]:
            game.move(Pos(x, y))
        else:
            game.move(None)

        mv = alphabeta_move(game, depth)

        if mv is None:
            print('IDO -1 -1')
        else:
            print(f'IDO {mv.x} {mv.y}')

        game.move(mv)

    if cmd == 'ONEMORE':
        game = Reversi()
        print("RDY")

    if cmd == 'BYE':
        break
