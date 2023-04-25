from itertools import permutations
from collections import deque

maze = []
goals = []
visited = set()
N, M = 0, 0


def is_wall(x: int, y: int) -> bool:
    return maze[x][y] == '#'


def wander(moves):
    Q = []

    DX = {'U': -1, 'D': 1, 'R': 0, 'L': 0}
    DY = {'U': 0, 'D': 0, 'R': 1, 'L': -1}

    for i in range(N):
        for j in range(M):
            if maze[i][j] == 'S':
                Q.append((i, j))

    for m in moves:
        dx, dy = DX[m], DY[m]

        for i in range(len(Q)):
            new_x = Q[i][0]
            new_x += dx if new_x + dx in range(N) else 0

            new_y = Q[i][1]
            new_y += dy if new_y + dy in range(M) else 0

            if not is_wall(new_x, new_y):
                Q[i] = (new_x, new_y)

    Q = list(set(Q))
    return (Q, len(Q))


def can_visit(positions):
    h_s = tuple(positions)
    if h_s not in visited:
        visited.add(h_s)
        return True
    return False


def generate_new_positions(i, positions):
    dx = [0, 0, 1, -1]
    dy = [1, -1, 0, 0]
    new_positions = []
    for pos in positions:
        new_x, new_y = pos[0] + dx[i], pos[1] + dy[i]

        new_positions.append((new_x, new_y) if all(
            [new_x in range(N), new_y in range(M), not is_wall(new_x, new_y)])
            else pos)

    return new_positions


def win(state):
    return all([s in goals for s in state])


def reduce_positions(positions):
    pos = list(sorted(positions))
    for i in range(len(positions) - 1):
        if pos[i] == pos[i + 1]:
            positions.remove(pos[i])
            return True
    return False


def solve():
    global N, M
    directions = ['R', 'L', 'D', 'U']
    moves = ['U', 'D', 'L', 'R']
    perms = list(permutations(moves))
    best_seq = ''
    minimal_moves = 1e9
    best_positions = []

# For each permutation of possible move direction we
# try to move min(N,M)//2 steps in each.
# We search for such permutation that is going to cause our
# commandos to move the least steps possible - moving closer to
# the walls will reduce the number of our steps towards the goal.
    for permutation in perms:
        move_sequence = "".join([min(N, M) // 2 * p for p in permutation])

        positions, length = wander(move_sequence)

        if length < minimal_moves:
            minimal_moves = length
            best_seq = move_sequence
            best_positions = positions

    Q = deque()
    Q.append((best_positions, best_seq))
    visited.add(tuple(best_positions))

    while len(Q) > 0:
        positions, moves = Q.popleft()

        # Merge if paths meet
        if reduce_positions(positions):
            visited.clear()
            Q.clear()

        if win(positions):
            return moves

        for i in range(4):
            new_positions = generate_new_positions(i, positions)

            if can_visit(new_positions):
                Q.append((new_positions, moves + directions[i]))


def setup():
    global maze, N, M, goals
    with open('zad_input.txt') as f:
        for line in f:
            maze.append(list(line.strip()))
    N, M = len(maze), len(maze[0])

    # Save goals coordinates
    for i in range(N):
        for j in range(M):
            if maze[i][j] == 'B':
                goals.append((i, j))


if __name__ == "__main__":
    setup()
    result = solve()

    with open('zad_output.txt', 'w') as out:
        out.write(result)
