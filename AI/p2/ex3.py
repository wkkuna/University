from heapq import heappop, heappush
from itertools import permutations
from math import sqrt


class Board:  # 2d array of W, G
    def __init__(self, board, goals, boxes=None):
        self.width = len(board[0])
        self.height = len(board)
        self.board = board  # stored row by row
        self.goals = goals
        if boxes is None:
            self.update_boxes()
        else:
            self.boxes = boxes

    def __getitem__(self, pos):  # accessed (x,y)
        return self.board[pos[1]][pos[0]]

    def __setitem__(self, pos, val):  # accessed (x,y)
        self.board[pos[1]][pos[0]] = val

    def __contains__(self, pos):
        return 0 <= pos[0] < self.width and 0 <= pos[1] < self.height and self[pos] != 'W'

    def __iter__(self):
        return (Pos(x, y) for x in range(self.width) for y in range(self.height))

    def copy(self):
        return Board([row.copy() for row in self.board], self.goals, self.boxes)

    def update_boxes(self):
        self.boxes = frozenset([pos for pos in self if self[pos] == 'B'])

    def move_box(self, pos, pos2):
        self[pos] = '.'
        self[pos2] = 'B'
        self.update_boxes()

    def __repr__(self):
        return str(self.boxes)

    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self.board[y][x], end='')
            print()

    def __hash__(self):
        return hash(self.boxes)

    def __eq__(self, other):
        return self.boxes == other.boxes


class Pos:
    def __init__(self, a, b=None):
        self.x, self.y = a if b is None else (a, b)

    def __add__(self, other):
        return Pos(self.x+other[0], self.y+other[1])

    def __sub__(self, other):
        return Pos(self.x-other[0], self.y-other[1])

    def __neg__(self):
        return Pos(-self.x, -self.y)

    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1]

    def __getitem__(self, num):
        return [self.x, self.y][num]

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __lt__(self, other):
        return self.x < other[0] or (self.x == other[0] and self.y < other[1])

    def __hash__(self):
        return hash((self.x, self.y))


def around(pos):
    return [pos+(1, 0), pos+(0, 1), pos+(-1, 0), pos+(0, -1)]


def get_meta_moves(board, start_pos):
    moves = []  # (Pos(x,y), side)
    queue = []
    seen = set()
    counter = 0
    heappush(queue, (0, start_pos))
    seen.add(start_pos)
    counter += 1
    min_pos = Pos(1000, 1000)
    while queue:
        _, pos = heappop(queue)
        for direction, new_pos in enumerate(around(pos)):
            if new_pos in board and new_pos not in seen:
                if board[new_pos] == 'B':
                    d = new_pos-pos
                    if new_pos+d in board and board[new_pos+d] != 'B':
                        walls = [p for p in around(
                            new_pos+d) if board[p] == 'W']
                        if len(walls) >= 3 or \
                                (len(walls) == 2 and walls[0].x != walls[1].x and walls[0].y != walls[1].y):
                            if new_pos+d not in board.goals:
                                continue
                        moves.append((new_pos, direction))
                else:
                    heappush(queue, (counter, new_pos))
                    seen.add(new_pos)
                    if new_pos < min_pos:
                        min_pos = new_pos
                    counter += 1
        seen.add(pos)
    return moves, min_pos


def get_board(board, move):
    d = [(1, 0), (0, 1), (-1, 0), (0, -1)][move[1]]
    new_board = board.copy()
    new_board.move_box(move[0], move[0]+d)
    return new_board


def get_path(board, start_pos, moves):
    path = ''
    for move in moves:
        box_pos, direction = move
        d = [(1, 0), (0, 1), (-1, 0), (0, -1)][direction]
        path += connect(board, start_pos, box_pos-d)
        path += 'RDLU'[direction]
        start_pos = box_pos
        board = get_board(board, move)
    return path


def connect(board, start_pos, end_pos):
    queue = []
    seen = set()
    seen.add(start_pos)
    heappush(queue, ('', start_pos))
    while queue:
        history, pos = heappop(queue)
        if pos == end_pos:
            return history
        for direction, new_pos in enumerate(around(pos)):
            if new_pos in board and board[new_pos] != 'B' and new_pos not in seen:
                heappush(queue, (history+'RDLU'[direction], new_pos))
                seen.add(pos)
    return "NOT POSSIBLE"


def meta_search(board, goals, sokoban):  # TODO: TOO MANY POSSIBLE STATES
    queue = []
    moves, min_position = get_meta_moves(board, sokoban)
    heappush(queue, (0, [], moves, board, min_position))
    seen = set()
    seen.add((board.boxes, min_position))
    depth = 0
    seen_size = 0
    while queue:
        priority, history, moves, board, min_position = heappop(queue)
        if all(board[goal] == 'B' for goal in goals):
            return history
        if len(history) > depth:
            depth = len(history)
        if len(seen) >= seen_size:
            seen_size += 100
        for move in moves:
            new_board = get_board(board, move)
            new_moves, new_min_position = get_meta_moves(new_board, move[0])
            if (new_board.boxes, new_min_position) not in seen:
                new_history = history+[move]
                # new_priority = len(new_history) + heuristic(new_board, goals)
                new_priority = heuristic(new_board, goals)
                heappush(queue, (new_priority, new_history,
                         new_moves, new_board, new_min_position))
                seen.add((new_board.boxes, new_min_position))
    else:
        return "NOT FOUND"


def m_dist(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


def e_dist(a, b):
    return sqrt((a.x-b.x)**2 + (a.y-b.y)**2)


def heuristic(board, goals):
    boxes = board.boxes
    return min(sum(m_dist(box, goal) for (box, goal) in zip(boxes, pgoals)) for pgoals in permutations(goals))


with open("zad_input.txt", "r") as in_f:
    board = []
    goals = []
    for line in in_f:
        board.append(list(line[:-1]))
    board = Board(board, goals)
    for y in range(board.height):
        for x in range(board.width):
            if board[x, y] == 'G':
                board[x, y] = '.'
                goals.append(Pos(x, y))
            elif board[x, y] == 'K':
                board[x, y] = '.'
                sokoban = Pos(x, y)
            elif board[x, y] == '+':
                board[x, y] = '.'
                goals.append(Pos(x, y))
                sokoban = Pos(x, y)
            elif board[x, y] == '*':
                board[x, y] = 'B'
                goals.append(Pos(x, y))
    board.update_boxes()
    assert len(set(board.boxes)) == len(set(goals))
    meta_moves = meta_search(board, goals, sokoban)
    with open("zad_output.txt", "w") as out_f:
        print(get_path(board, sokoban, meta_moves), file=out_f)
