# Ćwiczenia 13, grupa KBa 10-12, 14 stycznia 2021

## Zadanie 12-1
Zmienna jest współdzielona, gdy więcej niż jeden wątek odnosi się (dokonuje dereferencji) do przechowującego ją adresu w pamięci.

Wyścig - sytuacja, w której wynik działania wielowątkowego programu jest zależny od przeplotu, w jaki zostały wykonane jego wątki.

```c=
__thread long myid;
static char **strtab;

void *thread(void *vargp) {
  myid = *(long *)vargp;
  static int cnt = 0;
  printf("[%ld]: %s (cnt=%d)\n", myid, strtab[myid], ++cnt);
  return NULL;
}

int main(int argc, char *argv[]) {
  ...
  strtab = argv;
  while (argc > 0) {
  myid = --argc;
  pthread_create(&tid, NULL, thread, (void *)&myid);
  }
 ...
}
```

- `myid` - dzięki słowu kluczowemu `__thread` każdy z wątków posiada własną instancję tej zmiennej.   Instancja należąca do wątku, który wykonuje procedurę `main()` jest jednak współdzielona - a ponieważ wątki wykonujące `thread()` otrzymują jej adres, jest ona również źródłem wyścigów; wartość, którą poszczególne wątki odczytają z argumentów swoich funkcji i przypiszą do swoich prywatnych instancji `myid` zależą od kolejności, w jakiej zostaną wykonane.

- `strtab` - jest współdzielona, ale ponieważ wątki ograniczają się jedynie do jej odczytu, nie jest ona źródłem potencjalnych problemów.

- `vargp` - są współdzielone, ponieważ każdy z nich jest jedynie wskaźnikiem na instancję `myid` należącą do wątku "głównego"

- `cnt` - jest współdzielona, i o ile nie założymy atomowości operatora pre-inkrementacji, operacje zwiększania jej wartości będą grozić wyścigiem (jeśli pomiędzy instrukcjami pobrania z pamięci i inkrementacji nastąpi wywłaszczenie, zapisana wartość będzie mniejsza, niz powinna być)

- `argc` - nie jest współdzielona. Co prawda na jej podstawie `main()` wylicza `myid`, które przydziela utworzonym przez siebie wątkom, jednak przekazana zostaje im jedynie aktualna w momencie tworzenia wartość tejże zmiennej, a wątki nie są informowane o adresie, z którego ta wartość pochodzi

- `argv[0]` - współdzielenie zależy od przeplotu, podczas przebiegu wykonania wątków, który wydaje się być tym prawidłowym i zamierzonym
  powinna zostać odczytana przez dokładnie jeden wątek i nie podlegać współdzielenie, jednak na skutek wyścigów powodowanych przez metodę przekazywania wątkom parametru `vargp` może być inaczej. Natomiast niezależnie od ułożenia ścieżek wykonania poszczególnych wątków nie będzie ona źródłem wyścigów - jej wartość jest jedynie odczytywana.


## Zadanie 12-2

**sekcja krytyczna** - fragment kodu, który może być wykonywany tylko przez jeden wątek jednocześnie.
Założenia dotyczące sekcji krytycznej:
- nigdy nie będzie dostępna dla więcej niż jednego wątku jednocześnie - zapobiega to sytuacji wyścigu,
- nie dokonujemy założeń co do liczby procesorów ani ich szybkości - chcemy, by nasz kod był przenośny między różnymi procesorami jak i możliwy do wykonania w środowiskach zarówno jedno jak i wielowątkowych,
- do wstrzymania pracy wątku może dojść tylko w sekcjach krytycznych - chcemy, by do wstrzymania pracy wątku dochodziło tylko na początku sekcji krytycznej, gdy w jej obrębie znajduje się już jakiś wątek. Ułatwia to analizę programu.
- czas oczekiwania na wejście do sekcji krytycznej powinien być skończony - jeśli byłoby inaczej to dochodziłoby do marnowania zasobów na oczekiwanie zdjęcia blokady, która nigdy nie nastąpi

**wyłączanie przerwań** - wyłączenie przerwań spowoduje, że nie będzie mogło dość do przełączenia kontekstu. Oznacza to, że od momentu wyłączenia przerwań do ich ponownego włączenia operujemy cały czas w obrębie jednego wątku. Problem pojawia się, gdy proces nie przywróci obsługi procesów co może skutkować tym, że tylko jeden proces będzie działał w systemie. Dlatego nie jest dobrym pomysłem dawanie takiej możliwości programom w przestrzeni użytkownika, by nie dopuścić do sytuacji unieruchomienia całego systemu przez jeden proces. W przypadku wielu rdzeni rozwiązanie i tak nie będzie działać, bo inne wątki będą działać na współdzielonych danych z poziomu innych rdzeni.


Ograniczanie długości sekcji krytycznych zwiększa udział kodu, który jest możliwy do zrównoleglenia. Jak wiemy z prawa Admahala im większy udział współdzielonego kodu tym więcej pracy możemy wykonać w tym samym czasie dla wielu procesorów. **Drobno-ziarniste blokowanie** polega na blokowaniu możliwie najmniejszych fragmentów programu, czyli np. zamiast całej struktury drzewa to tylko liście, bądź gałęzie co zwiększa poziom zrównoleglenia programu.

## Zadanie 12-3

**Instrukcja atomowa** to taka, że patrząc w dowolnym momencie na stan wykonania programu, jesteśmy albo w całości przed wykonaniem tej instrukcji, albo w całości po.

**Blokada wirująca** to rodzaj blokady polegający na tym, że w momencie zakładania blokady czekamy w pętli `while` aż obecna blokada zostanie zwolniona.

Implementacje funkcji (z podanej książki):

```c=
int CompareAndSwap(int *ptr, int expected, int new) {
    int original = *ptr;
    if (original == expected)
        *ptr = new;
    return original;
}
```

Lock:

```c=
void lock(lock_t *lock) {
    while (CompareAndSwap(&lock->flag, 0, 1) == 1)
        ; // spin
}
```

Unlock:

```c=
void unlock(lock_t *lock) {
    lock->flag = 0;
}
```

*Czemu blokada wirująca nie jest sprawiedliwa?*

Blokada to nie jest sprawiedliwa, ponieważ wybrany wątek może czekać w nieskończoność na zasób. W szczególności jeżeli dwa wątki czekają na zasób, to nie mamy żadnej kontroli nad tym, który go zdobędzie, bo zasób dostanie ten, na który jądro się przełączy po raz pierwszy po zwolnieniu zasobu. Zatem potencjalnie już przy 3 wątkach możemy zablokować kompletnie dostęp dla jednego z wątków.

*Wiemy, że w przestrzeni użytkownika wątek może zostać wywłaszczony, jeśli znajduje się w sekcji krytycznej chronionej dowolną blokadą. Jakie problemy to rodzi?*

Problemem jest to, że jeśli mamy dwa wątki i jeden aktywnie czeka na zasób, a drugi go posiada, to w przypadku wywłaszczenia tego drugiego na rzecz pierwszego (przyjmijmy jeden rdzeń), procesor przez jakiś czas będzie wykonywał same bezsensowne obroty pętli while.

## Zadanie 12-4
**Cztery warunki konieczne do zaistnienia zakleszczenia:**
* Wzajemne wykluczanie: wątki po założeniu blokady mają wyłączny dostęp nad zasobami, ma które założyły blokady
* "trzymaj i czekaj" (ang. *hold-and-wait*): Wątki przechowują przydzielone im zasoby (np. blokady, które już założyły), czekając na dodatkowe zasoby (np. blokady, które chcą założyć)
* Brak wywłaszczania: zasobów (np. blokad) nie można odebrać na siłę z wątków, które je przechowują
* Cykliczne oczekiwanie: istnieje cykliczny łańcuch wątków, tak że każdy wątek zawiera jeden lub więcej zasobów (np. blokad), których żąda następny wątek w łańcuchu

**W jaki sposób można przeciwdziałać zakleszczeniom (ang. *deadlock prevention*)?**
**Hold-and-wait**: wątek może zakładać wszystkie blokady naraz. Dzięki temu nie wystąpi sytuacja, w której nastąpi zmiana wątku podczas zakładania blokad, wątek zablokuje od razu wszystkie zasoby, do których chce uzyskać dostęp.
> pthread_mutex_lock(prevention); // begin acquisition
pthread_mutex_lock(L1);
pthread_mutex_lock(L2);
...
pthread_mutex_unlock(prevention); // end

Przykład z *Arpaci-Dusseau 32.3*

Wadami tego podejścia jest ograniczenie współbieżności (zatrzymujemy działanie innych wątków, które chcą uzyskać dostęp do tych samych zasoboów co nasz wątek), oraz to, że musimy z góry znać wszystkie zasoby, z których wątek będzie korzystał.

**Brak wywłaszczania**: przy zakładaniu wątków można używać specjalnych funkcji bibliotecznych (np. `pthread mutex trylock()`), które zwracają 1, gdy uda się założyć blokadę albo 0, gdy się nie uda. Wtedy, gdy wywołanie takiej funkcji wzróci 0, program może zwolnić blokadę na innym zasobie, tak, aby udostępnić go innym wątkom.
> pthread_mutex_lock(L1);
if (pthread_mutex_trylock(L2) != 0) {
pthread_mutex_unlock(L1);
goto top;
}

Przykład z *Arpaci-Dusseau 32.3*

Rozwiązanie to może jednak prowadzić do uwięzienia (ang. *livelock*) -- jest możliwe, że dwa wątki będą wielokrotnie próbować wykonać tę sekwencję na przemian blokując i zwalniając zasoby, z których oba korzystają.

**Cykliczne oczekiwanie**: zapewnienie uporządkowania przy zakładaniu blokad, np. jeśli w systemie są dwie blokady L1 i L2, uporządkowanie wymusza, aby L1 było uzyskiwane przez L2. Metoda ta jest stosowana w Linuksie przy mapowaniu pamięci.

> if (m1 > m2) { // grab in high-to-low address order
pthread_mutex_lock(m1);
pthread_mutex_lock(m2);
} else {
pthread_mutex_lock(m2);
pthread_mutex_lock(m1);
}
// Code assumes that m1 != m2 (not the same lock)

Przykład z *Arpaci-Dusseau 32.3*


**Wzajemne wykluczanie**: rezygnacja z używania blokad i zastąpienie ich przez funkcje, umożliwiające wykonywanie innych procedur atomowo.

> int CompareAndSwap(int *address, int expected, int new) {
if (*address == expected) {
*address = new;
return 1; // success
}
return 0; // failure
}

> void AtomicIncrement(int *value, int amount) {
do {
int old = *value;
} while (CompareAndSwap(value, old, old + amount) == 0);
}

Przykład z *Arpaci-Dusseau 32.3*

## Zadanie 12-5

**wzajemne wykluczanie (mutual exclusion)** - to mechanizm zabezpieczania się przed jednoczesnym dostępem wielu wątków do jednego, współdzielonego zasobu. Wątek, który zdobędzie dostęp do tego zasobu wyklucza taką możliwość dla innych wątków do momentu zwolnienia zasobu. Użycie mechanizmu wzajemnego wykluczania w kodzie powoduje stworzenie sekcji krytycznej - fragmentu kodu, który będzie wykonywany sekwencyjnie, pomimo istnienia potencjalnie wielu wątków.

#### Opis porażki kodu:

* wątek $id=1$ rozpoczyna działanie
```c=
shared boolean blocked [2] = { false, false };
shared int turn = 0;

void P(int id) {
    while (true) {
        blocked[id] = true;
        while (turn != id) {
            while (blocked[1 - id])
                continue;
            turn = id;
        }
        /* put code to execute in critical section here */
        blocked[id] = false;
    }
}

void main() {
    parbegin (P(0), P(1)); // (0), (1)
}
```

* wątek $id=1$ kończy działanie tuż przed $turn = id$ z linii $10$
```c=
shared boolean blocked [2] = { false, false };
shared int turn = 0;

void P(int id) {
    while (true) {
        blocked[id] = true;
        while (turn != id) {
            while (blocked[1 - id])
                continue;
            turn = id; // (1)
        }
        /* put code to execute in critical section here */
        blocked[id] = false;
    }
}

void main() {
    parbegin (P(0), P(1)); // (0)
}
```

* wątek $id=0$ rozpoczyna działanie i kończy po dojściu do sekcji krytycznej (nie wchodzi do pętli, bo $turn \neq id$)
```c=
shared boolean blocked [2] = { false, false };
shared int turn = 0;

void P(int id) {
    while (true) {
        blocked[id] = true;
        while (turn != id) {
            while (blocked[1 - id])
                continue;
            turn = id; // (1)
        }
        /* put code to execute in critical section here */
        // (0)
        blocked[id] = false;
    }
}

void main() {
    parbegin (P(0), P(1));
}
```

* wątek $id=1$ wznawia działanie i wchodzi do sekcji krytycznej
```c=
shared boolean blocked [2] = { false, false };
shared int turn = 0;

void P(int id) {
    while (true) {
        blocked[id] = true;
        while (turn != id) {
            while (blocked[1 - id])
                continue;
            turn = id;
        }
        /* put code to execute in critical section here */
        // (0) (1)
        blocked[id] = false;
    }
}

void main() {
    parbegin (P(0), P(1));
}
```

## Zadanie 12-6
**Aktywne czekanie** - proces sprawdza jakiś warunek w pętli, zamiast zasnąć aż ten warunek będzie spełniony.
Aby się tego uniknąć możemy skorzystać z instrukcji `yield`, która oddaje procesor innemu wątkowi kiedy blokada jest zajęta.
Jednak nie jest to rozwiązanie perfekcyjne. Jeżeli nasz scheduler jest złośliwy i zawsze uruchamia najpierw wątki czekające na blokadę, nadal będziemy musieli przełączyć kontekst dla każdego z tych wątków, co może być kosztowne.
Nie unikamy też możliwości głodzenia - wątek może być zawsze uruchamiany, gdy blokada mu potrzebna jest już zabrana.

![](https://i.imgur.com/TMA2GcJ.png)

Aby założyć blokadę flag, czekamy aż blokada guard będzie wolna. Następnie sprawdzamy, czy flag jest wolna - jeśli tak, bierzemy ją i zwalniamy guard. W przeciwnym przypadku dodajemy aktualny wątek do kolejki, zwalniamy guard i zasypiamy. 
Aby zwolnić blokadę, znowu najpierw zdobywamy guard. Następnie patrzymy na kolejkę. Jeżeli jest pusta, zwalniamy flag, a jeżeli nie - budzimy pierwszy wątek, przekazując mu zajętą blokadę. Ostatecznie zwalniamy guard.

W tym kodzie jest drobny problem: jeżeli wątek zostanie wywłaszczony tuż przed park(), a następnie blokada zostanie zwolniona i nikt już nie będzie jej używał, tamten wątek będzie czekał w kolejce na zawsze.
Aby tego uniknąć, między linią 20 a 21 wstawiamy instrukcję setpark(). Jeżeli między setpark() a park() zostanie wywołane unpark(), park wraca natychmiast.

Tutaj głodzenie nie jest problemem, gdyż blokadę dostają kolejne wątki z kolejki.

## Zadanie 12-7

:::danger
Autor: Michał Myczkowski
:::

**Semafor zliczający** - przechowywana globalnie zmienna będąca liczbą naturalną, służąca do synchronizacji między wątkowej. Wartość semafora jest kontrolowana przy pomocy operacji P() i V().
**Semafor binarny** - jest semaforem w którym dopuszczamy tylko jeden zasób ( V zwiększa s tylko jeżeli s było 0).

#### Jaka jest główna różnica między semaforem binarnym, a muteksem?

Główna różnica leży w zastosowaniu muteksów i semafor binarnych.

Muteks ( Semafor wzajemnego wykluczenia ) - stosowany do zabezpieczenia współdzielonych danych przed wyścigami. Możnaby powiedzieć, że Muteks ma swojego właściciela ponieważ zawsze wątek który go blokuje musi go odblokować. Muteksy rozwiązują problemy odwróconych priorytetów.

Semafory binarne służą do porozumiewania się między wątkami. V( ) może zostać wywołane w dowolnym wątku.


```c=
struct csem {
    bsem mutex;
    bsem delay;
    int count;
};

void csem::csem(int v) {
    mutex = 1;
    delay = 0;
    count = v;
}
```
```c=
void csem::P() {
     P(mutex);
     count--;
     if(count < 0) {
         V(mutex);
         P(delay);
     } else {
         V(mutex);
     }
}
```
```c=
void csem::V() {
    P(mutex);
    count++;
    if(count <= 0)
        V(delay);
    V(mutex);
}
```


Kontrprzykład:

![](https://i.imgur.com/8KzaGqn.png)

## Zadanie 12-8
Czemu nikt nie zrobił tego zadania ?
