#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Losowy agent do Dżungli
'''


import random
import sys

import chess


class Chess:
    def __init__(self):
        self.board = chess.Board()
        
    def update(self, uci_move):
        try:
            move = chess.Move.from_uci(uci_move)
        except ValueError:
            raise WrongMove

        if move not in self.board.legal_moves:
            raise WrongMove
            
        self.board.push(move)
        out = self.board.outcome()
        if out is None:
            return None
        if out.winner is None:
            return 0
        if out.winner:
            return -1
        else:
            return +1    
    
    def moves(self):
        return [str(m) for m in self.board.legal_moves]
        
    def draw(self):
        print (self.board)    


class Player(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.game = Chess()
        self.my_player = 1
        self.say('RDY')

    def say(self, what):
        sys.stdout.write(what)
        sys.stdout.write('\n')
        sys.stdout.flush()

    def hear(self):
        line = sys.stdin.readline().split()
        return line[0], line[1:]

    def loop(self):
        while True:
            cmd, args = self.hear()
            if cmd == 'HEDID':
                unused_move_timeout, unused_game_timeout = args[:2]
                move = args[2]
                
                self.game.update(move)
            elif cmd == 'ONEMORE':
                self.reset()
                continue
            elif cmd == 'BYE':
                break
            else:
                assert cmd == 'UGO'
                #assert not self.game.move_list
                self.my_player = 0

            moves = self.game.moves()
            
            move = random.choice(moves)
            self.game.update(move)

            self.say('IDO ' + move)


if __name__ == '__main__':
    player = Player()
    player.loop()
