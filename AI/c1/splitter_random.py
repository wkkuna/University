import random


def read_dictionary():
    dt = []
    with open("polish_words.txt") as f:
        dt = f.read().splitlines()
    return list(filter(lambda x: len(x) != 0, dt))


def random_separate(line, dictionary):
    max_word_len = 25
    length = len(line)

    indices = list(range(1, min(max_word_len, length + 1)))
    random.shuffle(indices)

    if line == '':
        return ''

    for i in indices:
        if (line[0:i] in dictionary):
            output = random_separate(line[i:], dictionary)

            if output != -1:
                return line[0:i] + ' ' + output

    return -1


if __name__ == '__main__':
    with open("pantadeusz_bez_spacji.txt") as f, open("outputrandom.txt", 'w') as out:
        line = f.readline()[:-1:]

        while line:
            output = random_separate(line, read_dictionary())[:-1] + '\n'
            out.write(output)
            line = f.readline()[:-1:]
