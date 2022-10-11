import numpy as np
import copy
import random

MAP = None
DEN_0 = (3, 0)
DEN_1 = (3, 8)
DIR = [(0, 1), (1, 0), (-1, 0), (0, -1)]
MAX_TO_DRAW = 30

start_down = """
..#1#..
...#...
.......
.~~.~~.
.~~.~~.
.~~.~~.
.......
...#...
..#0#..
"""

start_up = """
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

GRASS = 2
WATER = 3
TRAP = 4


draw_down = {0: '*',
             1: '*',
             2: '.',
             3: '~',
             4: '#'}

draw_down_rev = {v: k for k, v in draw_down.items()}

draw_up = {0: '.',
           1: 'r',
           -1: 'R',
           2: 'c',
           -2: 'C',
           3: 'd',
           -3: 'D',
           4: 'w',
           -4: 'W',
           5: 'j',
           -5: 'J',
           6: 't',
           -6: 'T',
           7: 'l',
           -7: 'L',
           8: 'e',
           -8: 'E'}

draw_up_rev = {v: k for k, v in draw_up.items()}


def build_board():
    board_up = np.zeros((7, 9), dtype='int8')
    for x, row in enumerate(start_up.split()):
        for y, letter in enumerate(row):
            board_up[y][x] = draw_up_rev[letter]
    return board_up


def init_map():
    global MAP
    MAP = np.zeros((7, 9), dtype='int8')
    for y, row in enumerate(start_down.split()):
        for x, letter in enumerate(row):
            if letter == '0':
                MAP[x][y] = 0
            elif letter == '1':
                MAP[x][y] = 1
            else:
                MAP[x][y] = draw_down_rev[letter]


def info(board_up):
    for y in range(9):
        for x in range(7):
            if board_up[x][y] == 0:
                print(draw_down[MAP[x][y]], end='')
            else:
                print(draw_up[board_up[x][y]], end='')
        print()


class State:

    def __init__(self, board, animals, player, idle):
        self.board = copy.deepcopy(board)
        self.player = copy.deepcopy(player)
        self.idle = copy.deepcopy(idle)
        self.animals = copy.deepcopy(animals)
        self.opponent = 1 - self.player

    def info(self):
        print('=========')
        print('Player:', self.player, 'Idle:', self.idle)
        info(self.board)
        print('=========')

    def terminal(self):  # CHECK IF STATE IS TERMINAL
        if self.idle == 0:
            return True
        if self.board[DEN_0[0]][DEN_0[1]] > 0:
            return True
        if self.board[DEN_1[0]][DEN_1[1]] < 0:
            return True
        return False

    def result(self):
        if self.idle == 0:
            player0 = []
            player1 = []
            for ani in self.animals:
                if ani > 0:
                    player0.append(ani)
                else:
                    player1.append(ani)
                player1 = [abs(x) for x in player1]
            player0.sort()
            player1.sort()
            short = min(len(player0), len(player1))
            for i in range(short):
                if player0[i] > player1[i]:
                    return 0
                if player0[i] < player1[i]:
                    return 1
            return -1
        if self.is_occupied((3, 8)):
            return 1
        if self.is_occupied((3, 0)):
            return 0
        return self.opponent

    def remove_animal(self, animal_pos):
        x, y = animal_pos
        to_remove = self.board[x][y]
        self.board[x][y] = 0
        del self.animals[to_remove]

    def n_tiles(self, position):
        x, y = position
        tiles = []
        for d_x, d_y in DIR:
            if 0 <= x + d_x < 7 and 0 <= y + d_y < 9:
                if (self.player == 0 and (x + d_x, y + d_y) != (3, 8)) or\
                   (self.player == 1 and (x + d_x, y + d_y) != (3, 0)):
                    tiles.append((x + d_x, y + d_y))
        return tiles

    def push(self, animal, place):
        old_x, old_y = self.animals[animal]
        self.remove_animal((old_x, old_y))
        self.animals[animal] = place
        self.board[place[0]][place[1]] = animal

    def non_water(self, tiles):
        new_tiles = []
        for x, y in tiles:
            if MAP[x][y] != WATER:
                new_tiles.append((x, y))
        return new_tiles

    def can_beat(self, animal1, field):
        animal2 = self.board[field[0]][field[1]]
        if animal1 * animal2 > 0:
            return False
        if MAP[field[0]][field[1]] == TRAP:
            return True
        first = abs(animal1)
        second = abs(animal2)
        if (animal1 == -1 and animal2 == 8) or (animal1 == 1 and animal2 == -8):
            return True
        return first >= second

    def is_water(self, tile):
        x, y = tile
        return MAP[x][y] == WATER

    def is_occupied(self, tile):
        x, y = tile
        return self.board[x][y] != 0

    def value(self):  # POSITIVE FOR PLAYER 0, NEGATIVE FOR PLAYER 1
        fitness = 0

        des0 = (3, 0)
        des1 = (3, 8)

        def dist(animal):
            if animal > 0:
                des = des0
            else:
                des = des1
            ani_x, ani_y = self.animals[animal]
            des_x, des_y = des
            return abs(ani_x - des_x) + abs(ani_y - des_y)

        figures = {-1: -3,
                   -2: -2,
                   -3: -3,
                   -4: -4,
                   -5: -5,
                   -6: -6,
                   -7: -7,
                   -8: -7,
                   1: 3,
                   2: 2,
                   3: 3,
                   4: 4,
                   5: 5,
                   6: 6,
                   7: 7,
                   8: 7}
        if self.is_occupied((3, 0)):
            fitness += 1000
        if self.is_occupied((3, 8)):
            fitness -= 1000

        for animal in [-8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8]:
            if animal in self.animals:
                fitness += 2 * figures[animal]
        fitness += sum([dist(x) for x in self.animals if x < 0]) - sum([dist(x) for x in self.animals if x > 0])
        return fitness

    def moves(self):  # TODO: RETURN ALL adjacent states
        new_states = []
        if self.player == 0:
            rat = 1
        else:
            rat = -1
        if rat in self.animals:
            x, y = self.animals[rat]
            for tile in self.n_tiles(self.animals[rat]):
                if self.is_occupied(tile):
                    if MAP[x][y] != WATER and self.can_beat(rat, tile):
                        new_state = State(self.board, self.animals, self.opponent, MAX_TO_DRAW)
                        new_state.remove_animal((tile[0], tile[1]))
                        new_state.push(rat, tile)
                        new_states.append(new_state)
                else:
                    new_state = State(self.board, self.animals, self.opponent, self.idle - 1)
                    new_state.push(rat, tile)
                    new_states.append(new_state)
        if self.player == 0:
            normal = [2, 3, 4, 5, 6, 7, 8]
        else:
            normal = [-2, -3, -4, -5, -6, -7, -8]
        for ani in normal:
            if ani in self.animals:
                for tile in self.non_water(self.n_tiles(self.animals[ani])):
                    if self.is_occupied(tile):
                        if self.can_beat(ani, tile):
                            new_state = State(self.board, self.animals, self.opponent, MAX_TO_DRAW)
                            new_state.remove_animal((tile[0], tile[1]))
                            new_state.push(ani, tile)
                            new_states.append(new_state)
                    else:
                        new_state = State(self.board, self.animals, self.opponent, self.idle - 1)
                        new_state.push(ani, tile)
                        new_states.append(new_state)
        if self.player == 0:
            predators = [6, 7]
        else:
            predators = [-6, -7]
        for predator in predators:
            if predator in self.animals:
                x, y = self.animals[predator]
                for tile in [t for t in self.n_tiles(self.animals[predator]) if self.is_water(t)]:
                    vec_x, vec_y = tile[0] - x, tile[1] - y
                    flag = True
                    i = 1
                    while MAP[x + i * vec_x][y + i * vec_y] == WATER:
                        if self.board[x + i * vec_x][y + i * vec_y] == 0 or\
                           self.board[x + i * vec_x][y + i * vec_y] == rat:
                            pass
                        else:
                            flag = False
                            break
                        i += 1
                    if flag:
                        des_x, des_y = x + i * vec_x, y + i * vec_y
                        des = des_x, des_y
                        if self.is_occupied(des):
                            if self.can_beat(predator, des):
                                new_state = State(self.board, self.animals, self.opponent, MAX_TO_DRAW)
                                new_state.remove_animal(des)
                                new_state.push(predator, des)
                                new_states.append(new_state)
                        else:
                            new_state = State(self.board, self.animals, self.opponent, self.idle - 1)
                            new_state.push(predator, des)
                            new_states.append(new_state)

        return new_states


def initial_state(player):
    new_board = build_board()
    new_player = player
    new_idle = MAX_TO_DRAW
    animals = {}
    for x, row in enumerate(new_board):
        for y, letter in enumerate(row):
            if new_board[x][y] != 0:
                animals[new_board[x][y]] = (x, y)

    return State(new_board, animals, new_player, new_idle)


def random_game(state, starting_player):
    local = copy.deepcopy(state)
    acc = 0
    while not local.terminal():
        acc += 1
        all_moves = local.moves()
        if all_moves:
            local = random.choice(all_moves)
        else:
            break
    res = local.result()
    if res == -1:
        return 1 - starting_player, acc
    else:
        return res, acc


def multi(state, starting_player):
    LIMIT = 20000
    local = copy.deepcopy(state)
    options = {}
    for m in local.moves():
        options[m] = 0
    acc = 0
    while acc < LIMIT:
        for m in options:
            if acc >= LIMIT:
                break
            win, n = random_game(m, starting_player)
            options[m] += win
            acc += n
    return max(options, key=lambda s: options[s])


def game(debug=False):
    starting_player = 1 if random.random() > 0.5 else 0
    start = initial_state(starting_player)
    state = start
    if debug:
        state.info()
    while not state.terminal():
        if state.player == 0:
            all_moves = state.moves()
            if all_moves:
                state = max(all_moves, key=lambda s: s.value())
            else:
                break
        else:
            state = multi(state, starting_player)
            if not state:
                break
        if debug:
            state.info()
    if debug:
        state.info()
    res = state.result()
    if res == -1:
        return 1 - starting_player
    else:
        return res


init_map()

player0 = 0
player1 = 0
'''
test = initial_state(1)
test.board[2][1] = -1
test.board[0][2] = 0
test.animals[-1] = (2, 1)
test.remove_animal((0, 8))
test.board[3][2] = 1
test.animals[6] = 3, 1
test.board[3][1] = 6
test.info()
ms = test.moves()
for m in ms:
    m.info()
'''
for i in range(100):
    score = game(debug=True)
    if score == 0:
        player0 += 1
    if score == 1:
        player1 += 1
    print('SINGLE GAME WON BY:', score)
print('P0:', player0, 'P1:', player1)
