from collections import deque
import heapq

maze = []
goals = []
dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]
visited = set()
amazonDelivery = []
DISTANCES = {}
N, M = 0, 0


def can_visit(positions):
    global visited
    coords = tuple(positions)
    if coords in visited:
        return False

    visited.add(coords)
    return True


def is_wall(x: int, y: int) -> bool:
    return maze[x][y] == '#'


def generate_new_positions(i, positions):
    global dx, dy
    new_positions = []
    for x, y in positions:
        new_x, new_y = x + dx[i], y + dy[i]

        new_positions.append((new_x, new_y) if all(
            [new_x in range(N), new_y in range(M), not is_wall(new_x, new_y)])
            else (x,y))

    return new_positions


def win(state):
    return all([s in goals for s in state])


def heuristic(positions, moves_number):
    global DISTANCES
    distances = [DISTANCES[pos] for pos in positions]
    return max(distances) + moves_number


def BFS(coord):
    global dx, dy, DISTANCES
    DISTANCES[coord] = 1e9
    Q = deque()
    visited = {}
    visited[coord] = True
    Q.append((coord, 0))

    while Q:
        co, dist = Q.popleft()

        if co in goals:
            DISTANCES[coord] = min(DISTANCES[coord], dist)

        for i in range(4):
            new_x, new_y = co[0] + dx[i], co[1] + dy[i]

            if not (new_x, new_y) in visited and not is_wall(new_x, new_y):
                visited[(new_x, new_y)] = True
                Q.append(((new_x, new_y), dist + 1))


def shortest_paths():
    for i in range(N):
        for j in range(M):
            if not is_wall(i, j):
                BFS((i, j))


def solve():
    global amazonDelivery, visited
    directions = ['R', 'L', 'D', 'U']
    shortest_paths()
    Q = []
    heapq.heappush(Q, (heuristic(amazonDelivery, 0), amazonDelivery, ''))
    visited.add(tuple(amazonDelivery))

    while Q:
        _, positions, moves = heapq.heappop(Q)

        if win(positions):
            return moves

        for i in range(4):
            new_positions = generate_new_positions(i, positions)

            if can_visit(new_positions):
                heapq.heappush(Q, (heuristic(new_positions, len(
                    moves) + 1), new_positions, moves + directions[i]))


def setup():
    global maze, N, M, goals, amazonDelivery
    with open('zad_input.txt') as f:
        for line in f:
            maze.append(list(line.strip()))
    N, M = len(maze), len(maze[0])

    for i in range(N):
        for j in range(M):
            if maze[i][j] in ['G', 'B']:
                goals.append((i, j))

            if maze[i][j] == 'S':
                amazonDelivery.append((i, j))


if __name__ == "__main__":
    setup()
    result = solve()

    with open('zad_output.txt', 'w') as out:
        out.write(result)
