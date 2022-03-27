def is_palindrom(sentence):
    """
    Sprawdzenie czy napis jest palindromem ignorując wielkość liter.
    :param sentence: napis
    :return: True/False
    """
    sentence = "".join(filter(lambda c: c.isalnum(), sentence)).lower()
    return sentence == sentence[::-1]
