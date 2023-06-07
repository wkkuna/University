import copy
import heapq

direction_to_str = {(-1, 0): "U", (1, 0): "D", (0, -1): "L", (0, 1): "R"}
directions = direction_to_str.keys()

height, width = 0, 0
board = []
goals = set()
visited = set()


def is_wall(y, x):
    return board[y][x] == "W"


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

        for dxy in directions:
            new_pos = move(pos, dxy)

            if not is_wall(*new_pos) and new_pos not in visited:
                queue.append((dist + 1, new_pos))
                visited.add(new_pos)

    return distances

# We want as little moves as possible
def heuristic(start_state, distances):
    return sum([distances[crate[0]][crate[1]] for crate in start_state[0]])


def generate_states(state):
    old_pos = state[1]
    new_states = []

    for dxy in directions:
        crates = copy.deepcopy(state[0])
        new_pos = move(old_pos, dxy)
        one_ahead = move(new_pos, dxy)

        if not is_wall(*new_pos):
            if new_pos not in crates:
                new_states.append(
                    [crates, new_pos, state[2] + direction_to_str[dxy]])
            # Some dead state detection
            elif one_ahead not in crates and not is_wall(*one_ahead):
                crates.remove(new_pos)
                crates.add((new_pos[0] + dxy[0], new_pos[1] + dxy[1]))
                new_states.append(
                    [crates, new_pos, state[2] + direction_to_str[dxy]])

    return new_states


def run(start_state):
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
            cost = heuristic(new_state, distances) + len(new_state[2])
            value = visited.get((frozenset(new_state[0]), new_state[1]))

            if value is None or value > cost:
                heapq.heappush(queue, (cost, new_state))
                visited[(frozenset(new_state[0]), new_state[1])] = cost


# Parse the board symbols to game state
# Returns the initial state of the game
def init_game():
    global board, height, width, player, crates
    height, width = len(board), len(board[0])
    player = (0, 0)
    crates = set()

    for y in range(height):
        for x in range(width):
            c = board[y][x]
            if c in ['G', '*', '+']:
                goals.add((y, x))
            if c in ['K', '+']:
                player = (y, x)
            if c in ['B', '*']:
                crates.add((y, x))
    return [crates, player, '']


if __name__ == "__main__":
    with open("zad_input.txt", "r") as f, open("zad_output.txt", 'w') as out:
        board = list(map(lambda x: x.strip(), f.readlines()))
        out.write(run(init_game())[2])
