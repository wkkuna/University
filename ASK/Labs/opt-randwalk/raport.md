# Raport do zadania `randwalk`

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

Doświadczenia były wykonywane parami dla tego samego ziarna oraz z opcją `-t 5` oraz `-S 0x593d3feeb3dc9b71` - aby porównać wydajność funkcji dla takich samych zestawów danych.

### Ogólne porównanie i deasemblacja

Wydruki deasemblacji procedur `randwalk0` i `randwalk1` z wykorzystaniem programu *objdump* w [wydruki](https://hackmd.io/Ps9bA80MQXmCq1v4eEWx-A) lub w pliku wydruki.md.


|                                            | `randwalk0` | `randwalk1` |
|:------------------------------------------:|:-----------:|:-----------:|
|                 Instrukcje                 |     78      |     79      |
| Instrukcje warunkowe<br>(zaznaczone `***`) |     10      |     10      |
|               Średnie `IPC`                |    0.759    |    3.08     |
|           Średnie branch misspr.           |   19.39%    |    0.33%    |

Doświadczenie zostało przeprowadzone i przeanalizowane na podstawie wydruku uruchomienia programu:
```
./randwalk -S 0x593d3feeb3dc9b71 -n {5,10} -p {ipc,branch} -s {0..30} -t 5 -v {0,1}
```

### Badanie wpływu kolejności instrukcji w pętli na IPC zoptymalizowanej funkcji
Kod po optymalizacji ma następującą postać:
```C=
  do
  {
    sum += arr[i * n + j];
    k -= 2;
    if (k < 0)
    {
      k = 62;
      dir = fast_random();
    }

    int d = (dir >> k) & 3;


    // case 1
    i -= (d==0) & (i > 0);

    // case 2
    i += (d==1) & (i < n - 1);

    // case 3
    j -= (d==2) & (j > 0);

    // case 4
    j += (d==3) & (j < n - 1);

  } while (--len);
```

Przeprowadzone zamiany:
- $(0)$ Przeniesienie linijki 8 (sumowanie) na początek pętli.
- $(1)$ Zamiana `case 1` z `case 3`
- $(2)$ Zamiana `case 1` z `case 2`
- $(3)$ Zamiana `case 1` z `case 4`
- $(4)$ Zamiana `case 2` z `case 3`
- $(5)$ Zamiana `case 2` z `case 4`
- $(6)$ Zamiana `case 3` z `case 4`

| Zmiana | Średnie `IPC` |
|:------:|:-------------:|
| $(0)$  |     3.079     |
| $(1)$  |     3.079     |
| $(2)$  |     3.119     |
| $(3)$  |     3.124     |
| $(4)$  |     1.961     |
| $(5)$  |     2.971     |
| $(6)$  |     2.904     |


### Badanie wpływu wielkości tablicy na działanie programu

Aby wyniki były stosunkowo miarodajne porównywane były uruchomienia programu:
```
./randwalk -S 0x593d3feeb3dc9b71 -n {} -p {} -s 15 -t 5 -v {0,1}
```

#### Miss ratio

***Tabela 2*** `miss ratio` i `branch missprediction` dla randwalk0 
|  n  | size[KiB] |  l1   |   l2   |  l3   |  tlb  | branch |
|:---:|:---------:|:-----:|:------:|:-----:|:-----:|:------:|
|  0  |   0.001   | 0.02% | 0.02%  | 0.00% | 0.00% | 21.24% |
|  1  |   0.003   | 0.02% | 0.03%  | 0.00% | 0.00% | 21.25% |
|  2  |   0.016   | 0.04% | 0.09%  | 0.15% | 0.00% | 21.25% |
|  3  |   0.063   | 0.04% | 0.10%  | 0.05% | 0.00% | 21.25% |
|  4  |   0.25    | 0.02% | 0.12%  | 0.05% | 0.00% | 21.26% |
|  5  |     1     | 0.02% | 0.04%  | 0.01% | 0.00% | 21.24% |
|  6  |     4     | 0.02% | 0.02%  | 0.00% | 0.00% | 21.26% |
|  7  |    16     | 0.15% | 0.14%  | 0.12% | 0.00% | 21.23% |
|  8  |    64     | 1.00% | 0.34%  | 0.07% | 0.00% | 21.23% |
|  9  |    256    | 1.79% | 1.54%  | 0.01% | 0.01% | 21.22% |
| 10  |   1024    | 2.95% | 3.88%  | 0.05% | 0.01% | 21.24% |
| 11  |   4096    | 5.31% | 6.77%  | 0.27% | 0.02% | 21.24% |
| 12  |   16384   | 7.21% | 15.17% | 1.57% | 0.03% | 21.20% |
| 13  |   65536   | 6.00% | 19.03% | 3.59% | 0.07% | 21.22% |
| 14  |  262144   | 5.81% | 19.89% | 3.41% | 0.06% | 21.23% |
| 15  |  1048576  | 4.85% | 20.78% | 5.98% | 0.07% | 21.22% |




***Tabela 3*** `miss ratio` i `branch missprediction` dla randwalk1
|  n  | size[KiB] |   l1   |   l2   |  l3   |  tlb  | branch |
|:---:|:---------:|:------:|:------:|:-----:|:-----:|:------:|
|  0  |   0.001   | 0.01%  | 0.04%  | 0.02% | 0.00% | 0.01%  |
|  1  |   0.004   | 0.01%  | 0.04%  | 0.05% | 0.00% | 0.01%  |
|  2  |   0.016   | 0.01%  | 0.05%  | 0.03% | 0.00% | 0.01%  |
|  3  |   0.063   | 0.02%  | 0.04%  | 0.03% | 0.00% | 0.01%  |
|  4  |   0.25    | 0.03%  | 0.01%  | 0.01% | 0.00% | 0.01%  |
|  5  |     1     | 0.03%  | 0.03%  | 0.03% | 0.00% | 0.01%  |
|  6  |     4     | 0.07%  | 0.02%  | 0.01% | 0.00% | 0.02%  |
|  7  |    16     | 0.15%  | 0.12%  | 0.01% | 0.00% | 0.01%  |
|  8  |    64     | 1.52%  | 0.70%  | 0.03% | 0.00% | 0.02%  |
|  9  |    256    | 2.81%  | 2.66%  | 0.83% | 0.01% | 0.01%  |
| 10  |   1024    | 4.81%  | 5.61%  | 0.20% | 0.02% | 0.03%  |
| 11  |   4096    | 7.85%  | 9.69%  | 0.36% | 0.02% | 0.12%  |
| 12  |   16384   | 10.24% | 21.83% | 3.02% | 0.04% | 0.01%  |
| 13  |   65536   | 8.68%  | 21.98% | 4.79% | 0.09% | 0.01%  |
| 14  |  262144   | 8.75%  | 28.62% | 4.67% | 0.08% | 0.00%  |
| 15  |  1048576  | 6.49%  | 28.28% | 5.50% | 0.09% | 0.02%  |




#### `IPC`
***Wykres 1*** `IPC` w zależności od wielkości tablicy
![](https://i.imgur.com/bSebmlw.png)




#### Czas wykonania programów
***Wykres 2*** Czas wykonania w zależności od wielkości tablicy
![](https://i.imgur.com/0dSpJ4s.png)




Wnioski
---
### Ogólne porównanie
Po przeprowadzeniu optymalizacji można zaobserowować kilkukrotny wzrost `IPC`.  

Problemem w funkcji `randwalk0` były skoki warunkowe zależące od losowych liczb, przez co procesor nie mógł ich dobrze przewidzieć i zoptymalizować. Pozbywając się tych problematycznych instrukcji w `randwalk1` zwiększyłam wydajność programu o równowartość kosztu źle przewidzianych skoków - stąd diametralna różnica w wartości `branch missprediction`, a tym samym `IPC`.

### Kolejność instrukcji a IPC

Można zaobserwować znaczną różnicę `IPC` w zależności od wykonania instrukcji. Podglądając kolejne deasemblacje modyfikowanego programu, zmiana kolejności `case1/2/3/4` nie generowała innych instrukcji potrzebnych do przetworzenia danego bloku.

Zauważyłam jednak, że dla `case1/3` użyta zostaje instrukcja `test`, który wykonuje `and` ignorując wynik, natomiast dla `case2/4` instrukcja `cmp`, wykonująca odejmowanie.

Biorąc pod uwagę, że najgorsze `IPC` uzyskałam dla kolejności `case1 case3 case2 case4`, podejrzewam, że fakt występowania po sobie bloków z instrukcją `test`, a następnie kolejnych z instrukcją `cmp` może utrudniać przetwarzanie potokowe (jest ograniczona ilość instrukcji danego typu, która może być przetwarzana jednocześnie).

### Rozmiar tablicy a działanie programu
Na ***wykresie 1*** można zaobserwować większy spadek w `IPC` dla `randwalk1` w porównaniu do `randwalk0`. Możnaby uzasadnić to większymi chybieniami dla `randwal1` niż `randwalk0`.

Ponieważ funkcje wywoływane były dla tych samych wartości, nie powinno mieć to wpływu na chybienia - ze względu na to, że odczytują wartości z tych samych miejsc z tablicy. Ta różnica może więc wynikać z błędów pomiarowych. Natomiast owe chybienia mogą wpływać na `IPC` - ze względu na potrzebę ściągnięcia bloku z niższego poziomu pamięci.

Mimo wszystko, na obydwie funkcje wielkość tablicy raczej nie ma większego wpływu.

Dlaczego poprzedni raport był błędny
---
Po napisaniu raportu zauważyłam znaczącą różnicę między używaniem `-v -1`, a używaniem `-v 0` a `-v 1` po sobie. Ponieważ wyniki znacząco się różnią zaczęłam szukać tego przyczyny. Otóż nie zauważyłam, że w `main.c` w przypadku `-v -1` funkcja `run` ***nie jest*** uruchamiana asynchronicznie. Skutkuje to tym, że najprawdopodobniej obydwa wywołania owej funkcji zostały przetworzone potokowo, a ponieważ liczniki nie działają dla każdej z tych funkcji osobno, to część z danych dla wywołania `randwalk0` nałożyła się z tymi z `randwalk1`. Oczywiście skutkuje to zafałszowanymi danymi, stąd też mogłyby wypłynąć nieprawdziwe wnioski.

###### tags: `ask`
