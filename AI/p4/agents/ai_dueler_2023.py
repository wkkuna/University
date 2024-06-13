#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Prosta sprawdzarka turniejowa.
'''

import argparse
import os
#import Queue as queue
import queue
import random
import signal
import subprocess
import threading
import time

import chess
import numpy as np

VERBOSE = 0

# Tests embedded into the validator.


def time_consuming_function(N): 
    d = {} 
    r = [] 
    for i in range(N): 
        s = str(i) 
        d[s] = 4 * s 
        r.append(s) 
    res1 = max(d) 
    res2 = max(d, key=lambda x:d[x]) 
    res3 = s.find('999999') 
    return res1 and res2 and res3 

t0 = time.time()
r = time_consuming_function(500_000)

TIME_MULTIPLIER = (time.time() - t0) / 0.425

CONFIG = {
   'reversi': {'ready_timeout': 5, 'move_timeout': 5, 'game_timeout': 60}, 
   'jungle': {'ready_timeout': 5, 'move_timeout': 5, 'game_timeout': 60}, 
   'chess': {'ready_timeout': 5, 'move_timeout': 5, 'game_timeout': 60}
}

for game in  ['reversi', 'jungle']:  # chess intentionally ommited!
    for field in ['ready_timeout', 'move_timeout', 'game_timeout']:
        CONFIG[game][field] *= TIME_MULTIPLIER


#
# Reversi
#

class Reversi:
    M = 8
    DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def __init__(self):
        self.board = self.initial_board()
        self.fields = set()
        self.move_list = []
        self.history = []
        for i in range(self.M):
            for j in range(self.M):
                if self.board[i][j] is None:
                    self.fields.add((j, i))

    def initial_board(self):
        B = [[None] * self.M for _ in range(self.M)]
        B[3][3] = 1
        B[4][4] = 1
        B[3][4] = 0
        B[4][3] = 0
        return B

    def draw(self):
        for i in range(self.M):
            res = []
            for j in range(self.M):
                b = self.board[i][j]
                if b is None:
                    res.append('.')
                elif b == 1:
                    res.append('#')
                else:
                    res.append('o')
            print(''.join(res))
        print('')

    def moves(self, player):
        res = []
        for (x, y) in self.fields:
            if any(self.can_beat(x, y, direction, player)
                   for direction in self.DIRS):
                res.append((x, y))
        return res

    def can_beat(self, x, y, d, player):
        dx, dy = d
        x += dx
        y += dy
        cnt = 0
        while self.get(x, y) == 1 - player:
            x += dx
            y += dy
            cnt += 1
        return cnt > 0 and self.get(x, y) == player

    def get(self, x, y):
        if 0 <= x < self.M and 0 <= y < self.M:
            return self.board[y][x]
        return None

    def do_move(self, move, player):
        self.history.append([x[:] for x in self.board])
        self.move_list.append(move)

        if move is None:
            return
        x, y = move
        x0, y0 = move
        self.board[y][x] = player
        self.fields -= set([move])
        for dx, dy in self.DIRS:
            x, y = x0, y0
            to_beat = []
            x += dx
            y += dy
            while self.get(x, y) == 1 - player:
                to_beat.append((x, y))
                x += dx
                y += dy
            if self.get(x, y) == player:
                for (nx, ny) in to_beat:
                    self.board[ny][nx] = player

    def result(self):
        res = 0
        for y in range(self.M):
            for x in range(self.M):
                b = self.board[y][x]
                if b == 0:
                    res -= 1
                elif b == 1:
                    res += 1
        return res

    def terminal(self):
        if not self.fields:
            return True
        if len(self.move_list) < 2:
            return False
        return self.move_list[-1] == self.move_list[-2] == None

    def random_move(self, player):
        ms = self.moves(player)
        if ms:
            return random.choice(ms)
        return [None]

    def update(self, player, move_string):
        assert player == len(self.move_list) % 2
        move = tuple(int(m) for m in move_string.split())
        if len(move) != 2:
            raise WrongMove
        possible_moves = self.moves(player)
        if not possible_moves:
            if move != (-1, -1):
                raise WrongMove
            move = None
        else:
            if move not in possible_moves:
                raise WrongMove
        self.do_move(move, player)
        if self.terminal():
            return self.result()
        else:
            return None

class Chess:
    def __init__(self):
        self.board = chess.Board()
        
    def update(self, unused_player, uci_move):
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
    
    def draw(self):
        print (self.board)  
        print ()  

    
class Jungle:
    PIECE_VALUES = {
        0: 4,
        1: 1,
        2: 2,
        3: 3,
        4: 5,
        5: 7,
        6: 8,
        7: 10
    }
    MAXIMAL_PASSIVE = 50 # This number could be changed (be aware!)
    DENS_DIST = 0.1
    MX = 7
    MY = 9
    traps = {(2, 0), (4, 0), (3, 1), (2, 8), (4, 8), (3, 7)}
    ponds = {(x, y) for x in [1, 2, 4, 5] for y in [3, 4, 5]}
    dens = [(3, 8), (3, 0)]
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    rat, cat, dog, wolf, jaguar, tiger, lion, elephant = range(8)

    def __init__(self):
        self.board = self.initial_board()
        self.pieces = {0: {}, 1: {}}

        for y in range(Jungle.MY):
            for x in range(Jungle.MX):
                C = self.board[y][x]
                if C:
                    pl, pc = C
                    self.pieces[pl][pc] = (x, y)
        self.curplayer = 0
        self.peace_counter = 0
        self.winner = None

    def initial_board(self):
        pieces = """
        L.....T
        .D...C.
        R.J.W.E
        .......
        .......
        .......
        e.w.j.r
        .c...d.
        t.....l
        """

        B = [x.strip() for x in pieces.split() if len(x) > 0]
        T = dict(zip('rcdwjtle', range(8)))

        res = []
        for y in range(9):
            raw = 7 * [None]
            for x in range(7):
                c = B[y][x]
                if c != '.':
                    if 'A' <= c <= 'Z':
                        player = 1
                    else:
                        player = 0
                    raw[x] = (player, T[c.lower()])
            res.append(raw)
        return res

    def random_move(self, player):
        ms = self.moves(player)
        if ms:
            return random.choice(ms)
        return None

    def can_beat(self, p1, p2, pos1, pos2):
        if pos1 in Jungle.ponds and pos2 in Jungle.ponds:
            return True  # rat vs rat
        if pos1 in Jungle.ponds:
            return False  # rat in pond cannot beat any piece on land
        if p1 == Jungle.rat and p2 == Jungle.elephant:
            return True
        if p1 == Jungle.elephant and p2 == Jungle.rat:
            return False
        if p1 >= p2:
            return True
        if pos2 in Jungle.traps:
            return True
        return False

    def pieces_comparison(self):
        for i in range(7,-1,-1):
            ps = []
            for p in [0,1]:
                if i in self.pieces[p]:
                    ps.append(p)
            if len(ps) == 1:
                return ps[0]
        return None
                
    def rat_is_blocking(self, player_unused, pos, dx, dy):        
        x, y = pos
        nx = x + dx
        for player in [0,1]:
            if Jungle.rat not in self.pieces[1-player]:
                continue
            rx, ry = self.pieces[1-player][Jungle.rat]
            if (rx, ry) not in self.ponds:
                continue
            if dy != 0:
                if x == rx:
                    return True
            if dx != 0:
                if y == ry and abs(x-rx) <= 2 and abs(nx-rx) <= 2:
                    return True
        return False

    def draw(self):
        TT = {0: 'rcdwjtle', 1: 'RCDWJTLE'}
        for y in range(Jungle.MY):

            L = []
            for x in range(Jungle.MX):
                b = self.board[y][x]
                if b:
                    pl, pc = b
                    L.append(TT[pl][pc])
                else:
                    L.append('.')
            print(''.join(L))
        print('')

    def moves(self, player):
        res = []
        for p, pos in self.pieces[player].items():
            x, y = pos
            for (dx, dy) in Jungle.dirs:
                pos2 = (nx, ny) = (x+dx, y+dy)
                if 0 <= nx < Jungle.MX and 0 <= ny < Jungle.MY:
                    if Jungle.dens[player] == pos2:
                        continue
                    if pos2 in self.ponds:
                        if p not in (Jungle.rat, Jungle.tiger, Jungle.lion):
                            continue
                        #if self.board[ny][nx] is not None:
                        #    continue  # WHY??
                        if p == Jungle.tiger or p == Jungle.lion:
                            if dx != 0:
                                dx *= 3
                            if dy != 0:
                                dy *= 4
                            if self.rat_is_blocking(player, pos, dx, dy):
                                continue
                            pos2 = (nx, ny) = (x+dx, y+dy)
                    if self.board[ny][nx] is not None:
                        pl2, piece2 = self.board[ny][nx]
                        if pl2 == player:
                            continue
                        if not self.can_beat(p, piece2, pos, pos2):
                            continue
                    res.append((pos, pos2))
        return res

    def victory(self, player):
        oponent = 1-player        
        if len(self.pieces[oponent]) == 0:
            self.winner = player
            return True

        x, y = self.dens[oponent]
        if self.board[y][x]:
            self.winner = player
            return True
        
        if self.peace_counter >= Jungle.MAXIMAL_PASSIVE:           
            self.winner = None  # Draw game!
            return True
        
        return False

    def do_move(self, m):
        self.curplayer = 1 - self.curplayer
        if m is None:
            return
        pos1, pos2 = m
        x, y = pos1
        pl, pc = self.board[y][x]

        x2, y2 = pos2
        if self.board[y2][x2]:  # piece taken!
            pl2, pc2 = self.board[y2][x2]
            del self.pieces[pl2][pc2]
            self.peace_counter = 0
        else:
            self.peace_counter += 1    

        self.pieces[pl][pc] = (x2, y2)
        self.board[y2][x2] = (pl, pc)
        self.board[y][x] = None

    def update(self, player, move_string):
        assert player == self.curplayer
        move = tuple(int(m) for m in move_string.split())
        if len(move) != 4:
            raise WrongMove
        possible_moves = self.moves(player)
        if not possible_moves:
            if move != (-1, -1, -1, -1):
                raise WrongMove
            move = None
        else:
            move = ((move[0], move[1]), (move[2], move[3]))
            if move not in possible_moves:
                raise WrongMove
        self.do_move(move)
        
        if self.victory(player):
            # returns game value
            if self.winner == None:
                return 0
            return 2 * self.winner - 1
        else:
            return None


#
# Dueller's implementation
#


def kill_proc(process):
    if process.poll() is None:
        print('Killing subprocess.')
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)


class Player(object):
    def __init__(self, command, name=""):
        self.name = name
        self.in_queue = queue.Queue()
        self.out_queue = queue.Queue()
        self.process = subprocess.Popen(
            command, bufsize=1, shell=False, text=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            preexec_fn=os.setpgrp)
        self.threads = [
            threading.Thread(target=self._reader),
            threading.Thread(target=self._writer), ]
        for t in self.threads:
            # [FIX python3.10] Deprecation warning
            t.daemon = True
            t.start()

        self.total_time = 0
        self.start_time = None

    def _reader(self):
        proc = self.process
        while proc.poll() is None:
            prompt = proc.stdout.readline()
            if VERBOSE > 1:
                print ("%s -> S: `%s`" % (self.name, prompt.rstrip('\n')))
            if self.start_time is not None:
                self.total_time += time.time() - self.start_time
                self.start_time = None
            self.in_queue.put(prompt)

    def _writer(self):
        proc = self.process
        stdin = proc.stdin
        while proc.poll() is None:
            try:
                prompt = self.out_queue.get(timeout=0.1)
                stdin.write(prompt)
                stdin.write('\n')
                stdin.flush()
                if VERBOSE > 1:
                    print ("S -> %s: `%s`" % (self.name, prompt))
            except (queue.Empty, IOError):
                pass

    def get(self, block=True, timeout=None):
        return self.in_queue.get(block, timeout)

    def expect(self, prompt, block=True, timeout=None):
        ret = self.get(block, timeout)
        if ret.startswith(prompt):
            return ret.lstrip(prompt).strip()
        else:
            raise WrongMove("Expected " + prompt + " got " + ret)

    def put(self, item, block=True, timeout=None, measure_time=False):
        if measure_time:
            assert self.start_time is None
            self.start_time = time.time()
        return self.out_queue.put(item, block, timeout)

    def kill(self):
        kill_proc(self.process)
        for t in self.threads:
            t.join()


class WrongMove(Exception):
    pass


def play(game_class, num_games, p0cmd, p1cmd,
         ready_timeout=10, move_timeout=10, game_timeout=60):
    """Play a game between player p0 and p1.
    """
    p = {}

    def reset(kill=False):
        if not p or kill:
            for player in p.values():
                player.kill()
            p[0] = Player(p0cmd, name='P0')
            p[1] = Player(p1cmd, name='P1')
        else:
            for player in p.values():
                player.put('ONEMORE')
                player.total_time = 0.0

    reset()

    results = []
    timeout_result = {  # map players to resulkts after a timeout
        0: -1000,
        1: 1000}

    def play_game():
        game = game_class()
        cur_player = start_player = len(results) % 2
        oponent = 1 - cur_player

        start_time = time.time()
        try:
            timeout_winner = cur_player
            _ = p[oponent].expect('RDY', timeout=ready_timeout)
            timeout_winner = oponent
            remaining_time = ready_timeout - (time.time() - start_time)
            _ = p[cur_player].expect('RDY', timeout=min(0.1, remaining_time))

            player_remaining_time = max(
                0, game_timeout - p[cur_player].total_time)
            player_move_time = min(move_timeout, player_remaining_time)
            p[cur_player].put(
                'UGO %f %f' % (player_move_time, player_remaining_time),
                measure_time=True)
            if VERBOSE:
                game.draw()
            while True:
                move = p[cur_player].expect(
                    'IDO', timeout=player_move_time)
                if start_player == 0:
                    result = game.update(cur_player, move)
                    rmult = 1.0
                else:
                    result = game.update(oponent, move)
                    rmult = -1.0
                if VERBOSE:
                    game.draw()
                if result is not None:
                    reset()
                    result *= rmult
                    if result == 0:
                        print ('DRAW')
                    elif result < 0:
                        print ('P0 WON')
                    else:
                        print ('P1 WON')
                        
                    return result
                oponent = cur_player
                cur_player = 1 - cur_player
                timeout_winner = oponent
                player_remaining_time = (
                    game_timeout - p[cur_player].total_time)
                if player_remaining_time <= 0:
                    raise queue.Empty
                player_move_time = min(move_timeout, player_remaining_time)
                p[cur_player].put(
                    'HEDID %f %f %s' % (
                        player_move_time, player_remaining_time, move),
                    measure_time=True)
        except WrongMove:
            reset()
            return timeout_result[timeout_winner]
        except queue.Empty:
            # Timeout, kill the players!
            reset(kill=True)
            return timeout_result[timeout_winner]

    while len(results) < num_games:
        results.append(play_game())

    for player in p.values():
        player.put('BYE')
        player.kill()
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", default=0, type=int)
    parser.add_argument("--num_games", default=10, type=int)
    parser.add_argument("game")
    parser.add_argument("p0")
    parser.add_argument("p1")

    args = parser.parse_args()
    VERBOSE = args.verbose

    game = {
        'reversi': Reversi,
        'jungle' : Jungle,
        'chess' : Chess
    }[args.game]

    common_args = []
    result = play(game, args.num_games,
                  common_args + [args.p0],
                  common_args + [args.p1], **CONFIG[args.game])
    result = np.array(result)
    print("P0 won-tied-lost %d-%d-%d times." %
          ((result < 0).sum(), (result == 0).sum(), (result > 0).sum()))
