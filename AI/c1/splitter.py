#!/usr/bin/python

def read_dictionary():
    dt = []
    with open("polish_words.txt") as f:
        dt = f.read().splitlines()
    return list(filter(lambda x: len(x) != 0, dt))

def sqr_sum(words):
    return sum(map(lambda x: len(x)**2, words))

def best_fit(text, dictionary):
    n = len(text)
    if n == 0:
        return []
    if n == 1 and text in dictionary:
        return [text]

    max_set = [[] for _ in range(n)]

    for start in reversed(range(0, n-1)):
        for stop in range(start + 1, n+1):
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
    simplfied_dict = [word for word in dictionary if word in text]
    return best_fit(text, simplfied_dict)

if __name__ == "__main__":
    with open("pantadeusz_bez_spacji.txt") as f, open("output.txt", 'w') as out:
        dictionary = read_dictionary()
        text = f.readline()
        while text:
            output = separate_text(text, dictionary) + "\n"
            text = f.readline()
            out.write(output)