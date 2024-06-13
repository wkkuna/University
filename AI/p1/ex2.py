# Start splitting given text in reversed order
# from the longest possible word.
# Using a list of length of the text we save
# splitted word of maximum square sum (so far)
# at the beginning index of a first word in a current
# sequence.
# The whole text with word split maximizing
# square sum is at the index 0 of the list.

# Read words into a set
def read_dictionary():
    dt = None
    with open("words_for_ai1.txt") as f:
        dt = list(f.read().splitlines())
    return list(filter(len, dt))


# Square sum of word length
def sqr_sum(words):
    return sum(map(lambda x: len(x)**2, words))


# Chose the word that:
# a) exists in a dictionary
# b) maximizes word length square sum
def best_fit(text, dictionary):
    n = len(text)
    if n == 0:
        return []
    if n == 1 and text in dictionary:
        return [text]

    max_set = [[] for _ in range(n)]

    for start in reversed(range(n - 1)):
        for stop in range(start + 1, n + 1):
            sub = text[start:stop].strip()
            if sub in dictionary:
                if stop < n:
                    if len(max_set[stop]):
                        tmp_set = max_set[stop].copy()
                        tmp_set.insert(0, sub)

                        if sqr_sum(tmp_set) > sqr_sum(max_set[start]):
                            max_set[start] = tmp_set
                else:
                    if sqr_sum([sub]) > sqr_sum(max_set[start]):
                        max_set[start] = [sub]

    return " ".join(max_set[0])


def separate_text(text, dictionary):
    simplified_dict = [word for word in dictionary if word in text]
    return best_fit(text, simplified_dict)


if __name__ == "__main__":
    with open("zad2_input.txt") as f, open("zad2_output.txt", 'w') as out:
        dictionary = read_dictionary()
        for text in f.readlines():
            out.write(f"{separate_text(text, dictionary)}\n")
