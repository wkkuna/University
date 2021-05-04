# Raport do zadania `matmult`

### Autor: Wiktoria Kuna
### Numer indeksu: 316418

Konfiguracja
---

Informacje o systemie:

 * Dystrybucja: Pop!_OS 19.10
 * Jądro systemu: Linux 5.3.0-7625-generic
 * Kompilator: GCC 9.2.1
 * Procesor: Intel(R) Core(TM) i7-6700K CPU @ 4.00GHz
 * Liczba rdzeni: 4

Pamięć podręczna:

 * L1d: 32 KiB, 8-drożny (per rdzeń), rozmiar linii 64B
 * L2: 256 KiB, 4-drożny (per rdzeń), rozmiar linii 64B
 * L3: 8 MiB , 16-drożny (współdzielony), rozmiar linii 64B

Pamięć TLB:

 * L1d: 4KiB strony, 4-drożny, 64 wpisy
 * L2: 4 KiB + 2 MiB strony, 12-drożny, 1536 wpisów

Informacje o pamięciach podręcznych uzyskano na podstawie wydruku programu
`x86info` oraz [wikichip](https://en.wikichip.org/wiki/intel/microarchitectures/coffee_lake).

Wyniki eksperymentów
---
### Powtórzenie eksperymentu z wykładu

Wykres przedstawiający ilość cykli na wewnętrzną iterację pętli (analogiczny do tego z wykładu ze slajdu 48):

![](https://i.imgur.com/0J7OmNL.png)



### Pomiary dla różnych wartości parametru `BLOCK` 
Doświadczenie wykonane dla parametrów:
```
T long;

#define A_OFFSET NITEMS(BLOCK_SIZE * 2, T);
#define B_OFFSET NITEMS(BLOCK_SIZE * 1, T);
#define C_OFFSET NITEMS(BLOCK_SIZE * 0, T);
```

Rozmiar bloku `s` w zależności od typu `T` i parametru `BLOCK`

```
s = BLOCK * BLOCK * sizeof(T);
```

W zależności od parametru `BLOCK` w pliku `matmult.h` otrzymujemy następujące uśrednione wyniki dla współczynnika chybienia:

|     |   1    |   2    |   4   |   8   |  16   |  32   |   64   | 128    |
|:---:|:------:|:------:|:-----:|:-----:|:-----:|:-----:|:------:| ------ |
| L1  | 49.91% | 12.24% | 4.85% | 1.89% | 2.69% | 6.59% | 32.18% | 50.52% |
| L2  | 50.26% | 19.30% | 9.64% | 3.15% | 2.43% | 2.02% | 11.09% | 19.61% |
| L3  | 3.05%  | 1.28%  | 1.20% | 0.52% | 0.32% | 0.21% | 0.17%  | 0.24%  |
| TLB | 3.26%  | 0.47%  | 0.17% | 0.12% | 0.03% | 0.02% | 0.01%  | 0.01%  |

Wykres zależności wielkości bloku od czasu:
![](https://i.imgur.com/vYP6LVl.png)

Wykres dla offsetów 0-0-0:
![000](https://i.imgur.com/xxSoRAl.png)

Wykres dla offsetów 2-1-0
![](https://i.imgur.com/0pmIrjx.png)


Wnioski
---

### Powtórzenie eksperymentu z wykładu

Na pierwszy rzut oka, wykres może w żadnym stopniu nie przypominać tego z wykładu. Dzieje się tak ze względu na niemożliwe do przeoczenia uskoki (szczególnie dla mutmult2).

Pomijając błędy pomiarowe, obserwujemy względnie podobne różnice w wydajności funkcji. 

Na slajdach z wykładu dla n = 700 matmult0(jki) bliski jest osiągnięcia 80 cykli na iteracje, gdzie dla mojego komputera jest to około 10. Zjawisko to możnaby było wytłumaczyć różnicą procesorów. Do wygenerowania wykresu z wykładu użyty został 2 rdzeniowy procesor o częstotliwości 2GHz. Dla porównania - mój jest 4 rdzeniowy 4GHz.


### Pomiary dla różnych wartości parametru `BLOCK` 
Obserwujemy znaczną różnicę dla użycia bloków o parametrze `BLOCK` $\in \{4,6,8\}$, do tych o `BLOCK` $\in {2,32}$, a w szczególności dla tych o `BLOCK` $\in \{1,64,128\}$.

Optypamizacja z podziałem na bloki (kafelkowanie) ma na celu dostosować dane na których operujemy do parametrów naszej pamięci podręcznej - im mniej długich wędrówek w coraz niższe poziomy pamięci - tym lepiej.

W wypadku doświadczenia najlepiej wypadło kafelkowanie dla `BLOCK = 8`, czyli dla bloków 512 B, co dobrze współgra w organizacją 8-drożną sekcyjno-skojarzeniową. Wybieranie parametrów `BLOCK` $\in \{1, 2, 64, 128\}$ sprawia, że nie jesteśmy lokalni w dysponowaniu pamięcią i skutkuje częstszą wymianą linii w poziomach L1, L2.

### Podsumowanie 
Powyższe eksperymenty pozwoliły pokazać, że korzystanie z parametrów sprzętowych może znacznie wpłynąć na wydajność napisanych programów. Warto zatem (przy odpowiedniej wielkości danych) zadbać o lokalność używanej pamięci.

#### AD offset
Wykonując testy dla różnych kombinacji parametrów offset nie spostrzegłam istonego wpływu na wydajność.
