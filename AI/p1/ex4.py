# Iterate through a row and count the cost
# of inserting D consecutive ones at each position
# and choose the minimal cost

def opt_dist(puzzle, D):
    puzzle.split()
    bits = list(map(int, puzzle))
    min_cost = len(bits)

    # Check the cost for each position of D consequtive ones
    for i in range(len(bits) - D + 1):
        min_cost = min(D - sum(bits[i:i+D]) +
                       sum(bits[:i]) + sum(bits[i+D:]), min_cost)

    return min_cost


if __name__ == "__main__":
    with open("zad4_input.txt") as f, open("zad4_output.txt", 'w') as out:
        for line in f.readlines():
            l, D = line.split(' ')
            output = opt_dist(l, int(D))
            out.write(f"{output}\n")
