# Raport do zadania `transpose`

### Autor: Wiktoria Kuna 
### Numer indeksu: 316418

Konfiguracja
---

Informacje o systemie:

 * Dystrybucja: Pop!_OS 19.10
 * Jądro systemu: Linux 5.3.0-7648-generic
 * Kompilator: GCC 9.2.1
 * Procesor: Intel(R) Core(TM) i7-8750H CPU @ 2.20GHz
 * Liczba rdzeni: 6

Pamięć podręczna:

 * L1d: 32 KiB, 8-drożny (per rdzeń), rozmiar linii 64B
 * L2: 256 KiB, 4-drożny (per rdzeń), rozmiar linii 64B
 * L3: 9 MiB , 12-drożny (współdzielony), rozmiar linii 64B

Pamięć TLB:

 * L1d: 4KiB strony, 4-drożny, 64 wpisy
 * L2: 4KiB + 2MiB strony, 12-drożny, 1536 wpisów

Informacje o pamięciach podręcznych uzyskano na podstawie wydruku programu
`lscpu` oraz [wikichip](https://en.wikichip.org/wiki/intel/microarchitectures/coffee_lake).

Wyniki eksperymentów
---
### Zależność między rozmiarem bloku a wydajnością
***Tabela 1.1*** *Uśrednione miss ratio dla `transpose0` i kolejnych wartości parametru `BLOCK`*
|         |   L1   |   L2    |   L3   |  TLB   |
|:-------:|:------:|:-------:|:------:|:------:|
|  **1**  | 63.57% | 116.06% | 10.86% | 31.37% |
|  **2**  | 63.57% | 115.59% | 10.76% | 31.36% |
|  **4**  | 63.55% | 115.25% | 10.89% | 31.35% |
|  **8**  | 63.56% | 114.96% | 11.10% | 31.37% |
| **16**  | 63.56% | 115.16% | 11.24% | 31.33% |
| **32**  | 63.56% | 115.13% | 11.23% | 31.35% |
| **64**  | 66.23% | 126.85% | 13.82% | 31.17% |
| **128** | 70.35% | 133.55% | 18.88% | 31.74% |


***Tabela 1.2*** *Uśrednione miss ratio dla `transpose1` i kolejnych wartości parametru `BLOCK`*
|         |   L1   |   L2    |   L3   |  TLB   |
|:-------:|:------:|:-------:|:------:|:------:|
|  **1**  | 63.55% | 115.61% | 10.97% | 31.35% |
|  **2**  | 26.96% | 47.68%  | 7.75%  | 12.71% |
|  **4**  | 14.58% | 25.33%  | 7.29%  | 6.56%  |
|  **8**  | 10.35% | 19.28%  | 7.98%  | 4.15%  |
| **16**  | 8.19%  | 13.72%  | 7.85%  | 2.07%  |
| **32**  | 9.80%  | 14.79%  | 7.85%  | 1.06%  |
| **64**  | 20.25% | 17.93%  | 8.39%  | 0.58%  |
| **128** | 61.66% | 39.00%  | 9.54%  | 0.44%  |


Rozmiar bloku w zależności od parametu BLOCK:
```
size = BLOCK * BLOCK * 4 
```

***Wykres 1*** *Porównanie czasu wykonania transpose1 dla różnych wartości parametru `BLOCK`*
![transpose1 execution time dep. on BLOCK](https://i.imgur.com/XSdgpQT.png)

### Czas wykonania transpozycji macierzy w zależności od jej wielkości

***Wykres 2*** *Porównanie czasu wykonania transpozycji dla różnych konfiguracji (od n)*

![Transposition comparison](https://i.imgur.com/eUr882c.png)

***Wykres 3*** *Porównanie czasu wykonania transpozycji dla różnych konfiguracji (od KiB)*
![Transposition](https://i.imgur.com/ZGLAZaK.png)

Wnioski
---
Jak widzimy na ***wykresie 2*** odpowiednie dobranie rozmiaru bloku może wielokrotnie zwiększyć wydajność naszego programu.

***transpose0*** uzupełniając macierz wynikową iteruje wertykalnie. Stosując takie podejście niepotrzebnie sprowadzamy kilku-(kilkunastu-)krotnie te same bloki pamięci.

***transpose1***, w przeciwieństwie do poprzedniego podejścia redukuje niepotrzebne chybienia spowodowane konfliktami i stara się wykorzystać jak najwięcej danych ze ściągniętych już bloków.

Wyraźnie także obserwujemy różnicę w zależności od wyboru parametru `BLOCK` - wybór ten wpływa na to, jak efektywnie będziemy wykorzystywać każdy ściągnięty blok pamięci. W moim przypadku przy transpozycji najlepiej wypadły bloki o wielkości 1KiB (widoczne jest to przede wszystkim w średnim miss ratio oraz wykresie 2). Biorąc pod uwagę, że moje L1 jest 8-drożne, wielkość słowa to 64B, a na każdy z 64 zbiorów przypada 512B, wynik nie jest odrealnioną wartością.

Z ***wykresu 1*** czy ***wykresu 2*** ciężko byłoby wywnioskować cokolwiek o rozmiarze pamięci podręcznej - widać za to wyraźnie, że obie funkcje działają w złożoności kwadratowej, ale z inną stałą. 

Gdy popatrzymy zaś na związek między czasem a ilością pamięci do przetworzenia na ***wykresie 3*** zaobserwujemy wyraźne zwiększanie się różnicy czasu wykonania między funkcją ***transpose0*** a ***transpose1***. Pamiętając o tym, że ***transpose1*** została zaprogramowana tak, aby jak najbardziej korzystać z lokalności macierzy dst i jak najmniej ściągać dane z niższych poziomów pamięci, widoczna różnica pokazuje niejako 'krytyczną' wartość dla ***transpose0***, zmuszającą ją do zbyt częstego odwoływania się do coraz niższych poziomów pamięci.

Wiedząc, że czytanie danych z pamięci głównej jest o wiele bardziej kosztowne od odczytywania danych z pamięci podręcznej, moglibyśmy oszacować, że jej rozmiar wynosi między 8 a 10 KiB (zakres może wydawać się spory, ale należy również pamiętać o błędach pomiarowych spowodowanych np. innymi procesami w tle).


### Podsumowanie
Warto dla większych rozmiarów danych zadbać o lokalność - szczególnie w przypadkach, gdy nasz program powinnien cechować się dużą wydajnością. 


###### tags: `ask`
