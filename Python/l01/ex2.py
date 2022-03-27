def is_palindrom(sentence):
    sentence = "".join(filter(lambda c: c.isalnum(), sentence)).lower()
    return sentence == sentence[::-1]


print("Ala:", is_palindrom("Ala"))
print("Kajak:", is_palindrom("Kajak"))
print("Kobyła ma mały bok:", is_palindrom("Kobyła ma mały bok"))
print("Małe kaczuszki są super! Niestety nie są palindromem:",
      is_palindrom("Małe kaczuszki są super! Niestety nie są palindromem"))
print("Eine güldne, gute Tugend: Lüge nie!:",
      is_palindrom("Eine güldne, gute Tugend: Lüge nie!"))
