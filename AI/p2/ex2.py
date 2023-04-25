import copy
import heapq

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
direction_to_str = {(-1, 0): "U", (1, 0): "D", (0, -1): "L", (0, 1): "R"}

height = 0
width = 0
board = []

goals = set()
visited = set()


def is_not_wall(y, x):
    return board[y][x] != "W"


def is_terminal(state):
    return all(pos in goals for pos in state[0])


def move(position, direction):
    return (position[0] + direction[0], position[1] + direction[1])


def calculate_distances():
    queue = []
    visited = set()
    distances = [[0 for _ in range(width)] for _ in range(height)]

    for end in goals:
        queue.append((0, end))
        visited.add(end)

    while queue:
        dist, pos = queue.pop(0)
        distances[pos[0]][pos[1]] = dist

        for direction in directions:
            new_pos = move(pos, direction)

            if is_not_wall(new_pos[0], new_pos[1]) and new_pos not in visited:
                queue.append((dist + 1, new_pos))
                visited.add(new_pos)

    return distances


def heuristic(start_state, distances):
    return sum([distances[crate[0]][crate[1]] for crate in start_state[0]])


def search(start_state):
    if is_terminal(start_state):
        return start_state

    queue = []
    distances = calculate_distances()

    heapq.heappush(queue, (heuristic(start_state, distances) +
                   len(start_state[2]), start_state))
    visited = {(frozenset(start_state[0]), start_state[1]): 0}

    while queue:
        state = heapq.heappop(queue)[1]

        if is_terminal(state):
            return state

        new_states = generate_states(state)

        for new_state in new_states:
            value = visited.get((frozenset(new_state[0]), new_state[1]))
            cost = heuristic(new_state, distances) + len(new_state[2])

            if value is None or value > cost:
                heapq.heappush(queue, (cost, new_state))
                visited[(frozenset(new_state[0]), new_state[1])] = cost


def generate_states(state):
    old_pos = state[1]
    new_states = []

    for direction in directions:
        crates = copy.deepcopy(state[0])
        new_pos = move(old_pos, direction)
        one_ahead = move(new_pos, direction)

        if is_not_wall(new_pos[0], new_pos[1]):
            if new_pos not in crates:
                new_states.append(
                    [crates, new_pos, state[2] + direction_to_str[direction]])
            elif one_ahead not in crates and is_not_wall(one_ahead[0], one_ahead[1]):
                crates.remove(new_pos)
                crates.add((new_pos[0] + direction[0],
                           new_pos[1] + direction[1]))
                new_states.append(
                    [crates, new_pos, state[2] + direction_to_str[direction]])

    return new_states


if __name__ == "__main__":
    with open("zad_input.txt", "r") as f:
        for line in f:
            height += 1
            board.append(line.strip())

    width = len(board[0])
    start_state = [set(), (0, 0), '']
    player = (0, 0)
    crates = set()

    for y in range(height):
        for x in range(width):
            char = board[y][x]

            if char == 'K':
                player = (y, x)
            if char == 'B':
                crates.add((y, x))
            if char == 'G':
                goals.add((y, x))
            if char == '*':
                crates.add((y, x))
                goals.add((y, x))
            if char == '+':
                player = (y, x)
                goals.add((y, x))

    start_state = [crates, player, '']
    end_state = search(start_state)

    with open("zad_output.txt", 'w') as f:
        f.write(end_state[2])
