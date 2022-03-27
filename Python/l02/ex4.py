import subprocess
import os
import random


def uprosc_zdanie(tekst, dl_slowa, liczba_slow):
    # Wyrzucenie zbyt długich słów
    tmp = filter(lambda x: len(x) <= dl_slowa, tekst.strip().split(" "))
    # Usunięcie białych znaków ze słów (np. końca linii)
    tekst2 = list(map(lambda slowo: "".join(
        filter(lambda litera: not litera.isspace(), slowo)), tmp))

    slowa = len(tekst2)

    for i in range(liczba_slow, slowa):
        kandydat = random.randint(0, len(tekst2) - 1)
        del tekst2[kandydat]

    return " ".join(tekst2)


przykladowy_napis = """I love the smell of napalm in the morning. \
You know, one time we had a hill bombed for 12 hours. When it was all over, \
I walked up. We didn’t find one of ’em, not one stinkin' dink body. \
The smell, you know that gasoline smell, the whole hill. Smelled like victory."""

tekst = "Podział peryklinalny inicjałów wrzecionowatych \
kambium charakteryzuje się ścianą podziałową inicjowaną \
w płaszczyźnie maksymalnej."

print(uprosc_zdanie(przykladowy_napis, 6, 30))
print(uprosc_zdanie(tekst, 10, 5))

# Przykładowy, dłuższy tekst (pobranie Pana Tadeusza z wolnelektury.pl, wyświetlenie i zapisanie outputu z terminalu)
os.system("wget -O pt.txt https://wolnelektury.pl/media/book/txt/pan-tadeusz.txt")
man_call = subprocess.run(["cat", "pt.txt"], stdout=subprocess.PIPE, text=True)
print(uprosc_zdanie(man_call.stdout, 7, 100))
