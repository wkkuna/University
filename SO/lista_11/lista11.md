# Ćwiczenia 12, grupa KBa 10-12, 7 stycznia 2021

## Zadanie 11-1
**Superblok** przechowuje informacje na temat systemu plików.
**Tablica deskryptorów grup bloków** zawiera informacje o ułożeniu i konfiguracji grup bloków.
**Grupa bloków** -- bloki podzielone są na grupy, aby dzięki lokalności przyspieszyć czytanie powiązanych ze sobą plików.

Rozmiar bloku można obliczyć następująco:

> **s_log_block_size**
The block size is computed using this 32bit value as the number of bits to shift left the value 1024. This value may only be non-negative.

`block size = 1024 << s_log_block_size;`

Liczba i-węzłow jak i liczba bloków jest przechowana bezpośrednio:

> **s_inodes_count**
32bit value indicating the total number of inodes, both used and free, in the file system. This value must be lower or equal to (s_inodes_per_group * number of block groups). It must be equal to the sum of the inodes defined in each block group.

> **s_blocks_count**
32bit value indicating the total number of blocks in the system including all used, free and reserved. This value must be lower or equal to (s_blocks_per_group * number of block groups). It can be lower than the previous calculation if the last block group has a smaller number of blocks than s_blocks_per_group du to volume size. It must be equal to the sum of the blocks defined in each block group.

Deskryptorów grup bloków jest tyle samo co grup bloków:

> For each block group in the file system, such a group_desc is created.

Liczbę tą można policzyć w następujący sposób:
`s_blocks_count / s_blocks_per_group`

Liczbę bloków w grupie również można odczytać bezpośrednio z superbloku:

> **s_blocks_per_group**
32bit value indicating the total number of blocks per group. This value in combination with s_first_data_block can be used to determine the block groups boundaries. Due to volume size boundaries, the last block group might have a smaller number of blocks than what is specified in this field.

![](https://i.imgur.com/tNeV6Ja.png)

Na grupę bloków składają się:
* być może superblok i tablica deskryptorów grup bloków
* bloki z danymi
* bitmapa bloków
* bitamapa i-węzłów
* tabela i-węzłów

Rozmiar składowych w blokach podany na ilustracji.

Domyślnie superblok i tablica deskryptorów bloków jest kopiowana do każdej grupy bloków.
Wraz z pierwszą rewizją `ext2` została wprowadzona opcja przechowania superbloku i tablicy deskryptorów grup bloków jedynie w niektórych grupach bloków, a konkretnie takich o następujących numerach: 0, 1 oraz potęgi 3, 5 i 7.

## Zadanie 11-2

**blok pośredni** - blok, który zawiera wskaźniki na inne bloki. Wykorzystywany, gdy plik zajmuje dużo miejsca i wymaga dużo bloków.

![](https://i.imgur.com/E7w9Wpc.png)

**zapis synchroniczny** - zapis, na którego zakończenie czekamy i dopiero wtedy kontynuujemy pracę. Do braku spójności może dojść, gdy na przykład dwa pliki używają tego samego bloku

**spójność systemu plików** jest wtedy, gdy system plików zawsze operuje na poprawnie zainicjalizowanych strukturach wewnętrznych, nie dochodzi do konfliktów wskaźników (np. dwa pliki niebędące dowiązaniem używają tego samego bloku) oraz nie zawiera wiszących zasobów (np. blok jest zaalokowany ale nie jest używany przez żaden zasób)

##### Dopisanie n bloków, bądź dopisanie plików do katalogu:
- znajdź niezaalokowany jeszcze blok i oznacz go jako zaalokowany,
- zapisz do niego dane,
- spróbuj dopisać blok z danymi do inoda pliku docelowego:
    - spróbuj dopisać wskaźnik do bloków bezpośrednich,
    - jeśli nie ma miejsca to spróbuj dopisać do listy bloków pośrednich,
    - jeśli w drzewie bloków pośrednich nie ma miejsca to zaalokuj nowe bloki dla bloków pośrednich,
    - powiąż ze sobą nowo zaalokowane bloki (bloki pośrednie będziemy alokować od dołu (liścia) do góry, by zapobiec problemom ze spójnością w przypadku awarii),
    - dopisz nową gałąź bloków pośrednich do inoda pliku docelowego,
- dopisz wskaźnik na blok z danymi do inoda pliku, do którego chcemy dopisać dane,
- zaktualizuj metadane inoda pliku docelowego (rozmiar, ilość używanych bloków),
- powtórz dopóki są dane do zapisu

## Zadanie 11-3

Operacja jest **atomowa**, gdy możemy założyć, że nie jest podzielona na żadne mniejsze operacje, w szczególności nie może się wykonać tylko jej mniejsza część (np. w przypadku awarii zewnętrznej).

---

Czemu `rename` zakończy się błędem `EXDEV` kiedy próbujemy przenieść plik do innego systemu plików?

Sposób reprezentacji oraz zawartość metadanych, czy reprezentacji katalogu może się różnić w zależnośći od systemu plików, dlatego używamy VFS, wtedy wystarczy aby każdy system plików dostarczył swoje sposoby odczytania metadanych. Nie możemy zatem na przykład wstawić reprezentacji i-węzła pomiędzy inne w pliku katalogu.

---

1) Gdy te dwa pliki są w różnych systemach plików.

Aby przenieść plik i nie naruszyć spójności, musimy najpierw przenieść bloki z danymi i na końcu zaznaczyć w bitmapie bloków, że wybrane bloki są zajęte.

Potem możemy utworzyć (znaleźć nieużywany) i-węzeł w systemie plików do którego przenosimy, następnie wypełniamy go: tablice wskaźników na bloki i bloki pośrednie, bloki pośrednie oraz pozostałe metadane (rozmiar, czasy modyfikacji i dostępu itp.). Wstawiamy i-węzeł do odpowiedniego katalogu.

Gdy mamy gotowy nowy i-węzeł, stary możemy najpierw bezpiecznie usunąć z reprezentacji katalogu, a później usunąć go (zaznaczyć w bitmapie i-węzłów, że jest nieaktywny), a dopiero później poodznaczać w bitmapie bloków, że są nieaktywne.

2) Gdy te dwa pliki są w obrębie tego samego systemu plików.

* Nie musimy przepisywać bloków z danymi.
* Wstawiamy rekord katalogu do pliku katalogu, do którego przenosimy.
* Zmniejszamy odległość do kolejnego rekordu w poprzednim rekordzie katalogu względem nowego rekordu.
* Zwiększamy odległość do kolejnego rekordu w poprzednim rekordzie względem starego.

## Zadanie 11-4

- Usuwamy wpis w katalogu (lub po prostu przepinamy sąsiadów, zostawiając niewykorzystane, lecz niepuste miejsce), który przekazano jako argument
- Modyfikujemy zawartość inode'a - obniżamy liczbę referencji, jeśli nie spadła ona do zera, to w tym miejscu możemy zakończyć działanie
- Jeśli aktualnie istnieją w systemie otwarte deskryptor/y pliku wskazujące na usuwanego inode'a, robimy sobie przerwę do momentu zamknięcia ostatniego z nich
- Wygaszamy bity zajętości w należących do pliku blokach danych-liściach
- Wygaszamy bity w blokach przechowujących tablice wskaźników do bloków niebezpośrednich
- Gasimy bit użycia w mapie zajętości inode'ów odpowiedniej grupy

Przy takim ułożeniu kroków operację usuwania powinno dać się kontynuować nawet w razie nagłej awarii prądu - ponieważ inode zostaje oznaczony jako nieużywany na samym końcu, ewentualna powtórka tej operacji jest prosta - wystarczy odczytać wskaźniki na bloki przechowujące dane tego pliku i wygasić brakujące z nich. Gdybyśmy zamienili te kroki kolejnością, t.j. najpierw "usunęli" inode, a dopiero potem jego dane, ryzykowalibyśmy, że zanim uda się dokończyć kasowanie jego miejsce zająłby nowy wpis - wtedy utracilibyśmy informację o tym, które bloki powinny zostać usunięte (alternatywą mogłoby wtedy być przeskanowanie _wszystkich_ bloków i wykrycie takich, które nie są przypisane do żadnego inode'a). 
Odkasowanie _jakichś_ danych należących do pliku jest możliwe do momentu nadpisania zawartości jego inode'a, jednak nie mamy niestety gwarancji, że będzie to jego całość - poszczególne bloki mogą zostać nadpisane nową zawartością, nie możemy również dowiedzieć się, które z nich to dotknęło - wygaszona flaga zajętości bloku niekoniecznie oznacza, że nie został on w międyczasie zmodyfikowany; mogło nastąpić zarówno zajęcie jak i zwolnienie.


## Zadanie 11-5

**Dowiązanie twarde** to nowy wpis w katalogu z numerem inode pliku, na który wskazuje.
**Dowiązanie symboliczne** to osobny i-węzeł zawierający ścieżkę do pliku, na który wskazuje.

Krótka ścieżka może być przechowywana bezpośrednio w i-węźle, dłuższa wymaga osobnego bloku.

Można stworzyć pętlę poleceniem ```ln -s loop .```
Jądro trzyma stałą MAXSYMLINKS i nie pozwala na rozwiązanie większej liczby dowiązań symbolicznych podczas rozwiązywania ścieżki.
Fragment ```strace link loop/loop link```:
```
link("loop/loop", "link")               = -1 ELOOP (Too many levels of symbolic links)
```

Nie da się stworzyć pętli z użyciem dowiązania twardego, gdyż nie jest możliwe stworzenie takiego dowiązania do katalogu.

## Zadanie 11-6

**Czemu fragmentacja systemu plików jest szkodliwym zjawiskiem?**
Plik jest pofragmentowany, jeśli jest przechowywany na dysku w więcej niż jednym spójnym fragmencie.
Zmiana pozycji głowicy dysku magnetycznego jest kosztowna. Losowe dostępy do dysku SSD są również wolniejsze niż sekwencyjne.

**Opisz w jaki sposób odroczony przydział bloków(ang. delayed allocation) [§3.2] zapobiega powstawaniu fragmentacji**
Alokacja odroczona jest dobrze znaną techniką, w której alokacje bloków są odkładane, a nie podczas operacji write(). Ta metoda zapewnia możliwość połączenia wielu żądań alokacji bloków w jedno żądanie, zmniejszając ilość operacji write(). Odroczony przydział bloków pozwala również uniknąć niepotrzebnego przydziału bloków dla plików o krótkim czasie trwania.

Sytuacja, w której przyda się odroczony przydział bloków:
Kiedy często wpisujemy małymi porcjami.

Fragmentacja systemu plików może być zmniejszona, ponieważ wszystkie (lub duża liczba) bloków dla pojedynczego pliku mogą być przydzielone w tym samym czasie. Znajomość całkowitej liczby bloków w każdym pliku pozwala alokatorowi bloków (mballoc) znaleźć odpowiednią porcję wolnego miejsca dla każdego pliku zamiast wybierać wolną część, która jest zbyt duża lub zbyt mała.

**Wytłumacz jak zakresy (ang. extents) pomagają w ograniczaniu rozmiaru metadanych przechowujących adresy bloków należących do danego pliku. Czy po defragmentacji systemu plików ext4 liczba wolnych bloków może wzrosnąć?**
![](https://i.imgur.com/JMvtW6c.png)
Zakresy zmniejszają ilość metadanych potrzebnych do śledzenia bloków danych. Zamiast przechowywać listę wszystkich bloków tworzących plik, chodzi o to, aby przechowywać tylko adres pierwszego i ostatniego bloku każdego ciągłego zakresu bloków. Te ciągłe zakresy bloków danych (i par liczb, które je reprezentują) nazywane są zakresami.

Po defragmentacji systemu plików ext4 liczba wolnych bloków może wzrosnąć.

**Jak mógłby wyglądać najprostszy algorytm defragmentacji?**
Dla każdego pliku algorytm tworzy tymczasowy i-node i przydziela ciągłe zakresy do tymczasowego i-node'a przy użyciu (multiple block allocation). Następnie kopiuje oryginalne dane pliku do podręcznej pamięci, usuwamy z poprzedniego miejsca(zwalniamy), później znowu zapisujemy.

## Zadanie 11-7

```
>>>sudo debugfs /dev/sda5
>>>debugfs: freefrag
Opisuje fragmentację wolnego miejsca w aktualnie otwartym systemie plików. 
Jeśli podano opcję -c, polecenie wypisze ile wolnych fragmentów 
o podanym rozmiarze można znaleźć w systemie plików.

>>>debugfs: stats
Wypisz zawartość superbloku i deskryptory grup bloków. 
Jeśli podano opcję -h, wypisuje tylko zawartość superbloku.

>>>fallocate -l 10GB largefile
>>>sudo debugfs -R "dump_extents home/usr/largefile" /dev/sda5

Wypisuje drzewo przydziałów specyfikacji pliku i-węzła. Flaga -n spowoduje, że dump_extents wyświetli tylko wewnętrzne węzły w drzewie przydziałów. Flaga -l spowoduje, że dump_extents wyświetli tylko węzły liści w drzewie przydziałów.

>>>ln -s /home/usr/so/lista9/so20_lista_9 /home/usr
>>>sudo debugfs /dev/sda5
>>>inode_dump /home/usr/so20_lista_9

0000  ffa1 e803 2100 0000 f02a f65f f02a f65f  ....!....*._.*._
0020  f02a f65f 0000 0000 e803 0100 0000 0000  .*._............
0040  0000 0000 0100 0000 2f68 6f6d 652f 6567  ......../home/us
0060  6f72 2f73 6f2f 6c69 7374 6139 2f73 6f32  r/so/lista9/so20
0100  305f 6c69 7374 615f 3900 0000 0000 0000  _lista_9........
0120  0000 0000 0000 0000 0000 0000 0000 0000  ................
0140  0000 0000 f460 d809 0000 0000 0000 0000  .....`..........
0160  0000 0000 0000 0000 0000 0000 7eaa 0000  ............~...
0200  2000 0bf4 00e0 7b81 00e0 7b81 a805 7082   .....{...{...p.
0220  f02a f65f 00e0 7b81 0000 0000 0000 0000  .*._..{.........
0240  0000 0000 0000 0000 0000 0000 0000 0000  ................

>>>debugfs:  blocks /home/usr/jbs
>>>3737548 3737549 3737550
>>>debugfs:  icheck 3737549
>>>Block	Inode number
   3737549	924778
>>>debugfs:  ncheck 924778
>>>Inode	Pathname
   924778	/home/usr/jbs


>>>debugfs:  blocks /home/usr/Downloads
>>>3681327
>>>debugfs:  block_dump 3681327
>>>
0000  9b60 0e00 0c00 0102 2e00 0000 e119 0e00  .`..............
0020  0c00 0202 2e2e 0000 ec06 0400 1c00 1301  ................
0040  736f 3230 5f6c 6973 7461 5f39 2e74 6172  so20_lista_9.tar
0060  2e67 7a00 e904 0600 c00f 0901 3267 7261  .gz.........2gra
0100  6d73 2e67 7a00 0000 5b02 0e00 ac0f 0601  ms.gz...[.......
0120  3267 7261 6d73 2e67 7a2e 7061 7274 0000  2grams.gz.part..
0140  0000 0000 0000 0000 0000 0000 0000 0000  ................
*
7760  0000 0000 0000 0000 0c00 00de f9c0 f568  ...............h

```

## Zadanie 11-8

**Fork zasobu** (ang. Resource fork) zestaw danych powiązanych z obiektem systemu plików w klasycznych systemach Mac OS, który przechowuje informacje w danej formie zawierające szczegóły, takie jak mapy bitowe ikon, kształty okien, definicje menu i ich zawartości oraz kod aplikacji (kod maszynowy). Ułatwia przechowywanie wielu dodatkowych informacji.
Służył do:
- przechowywania wszystkich danych graficznych na dysku, dopóki nie były potrzebne, a następnie pobrane, rysowane na ekranie i wyrzucane (zmniejszyło to wymagania dotyczące pamięci),
- można było go wykorzystać do dystrybucji prawie wszystkich komponentów aplikacji w jednym pliku, zmniejszając bałagan i upraszczając instalację i usuwanie aplikacji.

Dostęp do forka zasobu działa bardziej jak wyodrębnianie uporządkowanych rekordów z bazy danych. 

Plik Uniksowy jest po prostu ciągiem bajtów. Przez co, każdy program, który chce zapisać do pliku musi wiedzieć o jego rodzaju (definiującego zawartość). Sprowadza się to do tego, że przy każdej operacji modyfikującej plik, program musi pozostawić typ niezmieniony lub przepisać go zgodnie z innym rodzajem.

W przeciwieństwie do systemów operacyjnych Macintosh (wersja 9 lub niższa), w których jeden plik składał się z fork danych - który odpowiadał Uniksowemu ciągowi bajtów z danymi jak i z forka zasobów, który przechowywał dodatkowe informacje. Umożliwiał on np. wyświetlenie właściwej ikony pliku i otwarcie go bez konieczności rozszerzenia w nazwie pliku.

**Rozszerzone atrybuty pliku** to pary nazwa (ciąg znaków zakończony zerem poprzedzony odpowiednim namespacem):wartość skojarzone z plikami i katalogami. Atrybuty mogą być zdefiniowane (niepusta wartość) lub nie. Są rozszerzeniem zwykłych atrybutów związanych z systemem i-węzłów. Często zapewniają jakieś dodatkowe funkcje, np. zwiększenie bezpieczeństwa.

Rozszerzone atrybuty mogą zostać zaalokowane **na końcu i-węzła**, a jeśli nie ma tam wystarczająco miejsca to ext4 dopuszcza zaalokowanie **nowego bloku** specjalnie na te atrybuty.

```bash=
$ getfattr obrazek.png -d
<nic>
$ setfattr -n user.md5sum -v $(md5sum obrazek.png) obrazek.png
$ getfattr obrazek.png -d
# file: obrazek.png
user.md5sum="bddd76287d6cdb775bae878899a70fba"
```

## Zadanie 11-9

Pierwszym krokiem w HTree jest zastąpienie nazw elementów ich haszami. Po tej zmianie, tak naprawdę możemy myśleć, że wejścia katalogów są liczbami, a to co my chcemy zrobić to dodać liczbę, usunąć liczbę i znaleźć liczbę w zbiorze. Są potencjalne drobne problemy zw. z konfliktem haszy, ale są to szczegóły, które nie są potrzebne do zrozumienia struktury.

Rozwiązanie zastosowane w HTree polega na tym, że będziemy sobie wyobrażali, że nasz ciąg liczb jest posortowany (co jest dość bliskie pełni prawdy). Żeby utrzymać jednak spójność z _ext2_, to dzielimy te elementy na bloki w jakich będą przebywać, elementy w bloku nie muszą być posortowane. Strukturą na tych blokach, którą zbudujemy jest uproszczona wersja $B$-drzewa.

Zbudujemy teraz drzewo na tych blokach w taki sposób, że liśćmi będą kolejne elementy ciągu, a wierzchołkami wewnętrznymi będą pełne bloki pamięci, które będą zawierały co najwyżej $\frac{\texttt{rozmiar bloku} - 32}{8}$ synów, co dla bloków o rozmiarze $4 \texttt{ KiB}$, daje $508$ synów. Dla każdego drzewa, jego synowie są posortowani po minimalnym haszu w poddrzewie. Implementacja opisana w artykule pozwala tylko na drzewa o głębokości $2$.

Bardzo prosto jest teraz zaimplementować lookup. Wystarczy na danym poziom wykonać wyszukiwanie binarne i znaleźć syna, który ma odpowiedniego hasza i do niego zejść. Powtarzamy to, aż dojdziemy do liścia. Ponieważ w bloku w liściu, nasze elementy nie są posortowane, to tam już liniowo wszystkie przeglądamy. Warto tu wspomnieć, że może się okazać, że w wypadku kolizji haszy możemy być zmuszeni do przejrzenia też kolejnych bloków.

Usunięcie elementu też jest dość proste, ponieważ nie przejmujemy się potencjalnymi nieużytkami, które mogą powstać i po prostu usuwamy dane wejście z bloku. Dodawanie elementu jest proste o ile mamy wystarczająco dużo miejsca w odpowiednim bloku. Jeśli mamy, to dodajemy tam nasz element po prostu. Jeśli nie, to musimy podzielić ten blok na dwie części. Robimy to sortując elementy bloku i dzieląc je po równo na dwa nowe bloki. Musimy też przepiąć wskaźniki od rodzica, jeśli rodzic ma za dużo dzieci, to go też musimy rekurencyjnie podzielić na dwie części.
