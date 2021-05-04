## Zadanie 10-1

System jest **współbieżny** jeżeli wykonuje kilka zadań na raz. Nie musi wykonywać ich w tej samej chwili, może wykonać część jednego, wstrzymać, wykonać drugie i powrócić do pierwszego.

Przetwarzanie **równoległe** występuje, gdy program dzieli zadania na mniejsze części i wykonuje je w tym samym momencie, tj. wiele wątków wykonuje jednocześnie (w tym samym cyklu zegara procesora) instrukcje.

**Procedura wielobieżna** to taka, której wykonanie może zostać wstrzymać (np. przez sygnał) i może ona później być bezpiecznie wznowiona. Kiedy wystąpi wstrzymać pierwszego wywołania procedury, może ona zostać wywyołana po raz drugi (a te i każde inne wywołanie też może być wstrzymane i procedura może być wywołana po raz kolejny podczas), zakończyć drugie wywołanie i wznowić pierwsze.

**Procedura bezpieczna wątkowo** to taka procedura, która może być bezpiecznie wykonywana **współbieżnie**, czyli na przykład z kilku wątków na raz.

Procedura bezpieczna wątkowo, ale nie wielobieżna: `malloc i free`.
Obie te procedury są oczywiście bezpieczne-wątkowo, bo możemy alokować pamięć w wielu wątkach.
Nie są one jednak wielobieżne, tak jak wszystkie inne procedury, które na początku zakładają blokadę, a na końcu ją zwalniają. Przerwanie takiej procedury i wywołanie jej ponownie sprawi, że będziemy nieskończenie czekać na zwolnienie blokady.

Procedura wielobieżna, ale nie bezpieczna-wątkowo:
```c=
int t;

void swap(int *x, int *y)
{
    int s;
    s = t;
    t = *x;
    *x = *y;
    *y = t;
    t = s;
}
```
W powyższej procedurze występuje niezabezpieczona sekcja krytyczna `t = s`, więc nie jest wątkowo bezpieczna. Jest jednak wielobieżna - wartość `t` zostanie poprawnie przywrócona w przypadku przerwania i wywołania.

W jednowątkowym procesie uniksowym może wystąpić współbieżność. Np. kiedy proces otrzyma sygnał i zostanie wywołany signal handler.

## Zadanie 10-2

:::info
Treść:
Wybierz odpowiedni scenariusz zachowania wątków, w którym konkurują o dostęp do zasobów,i  na  tej  podstawie  precyzyjnie  opisz zjawisko zakleszczenia(ang.deadlock), uwięzienia(ang.livelock) oraz głodzenia(ang.starvation). Dalej  rozważmy  wyłącznie  ruch  uliczny. Kiedy  na  jednym  lub  wieluskrzyżowaniach  może  powstać  każde  z  tych  zjawisk? Zaproponuj  metodę  (a)wykrywania i usuwaniazakleszczeń (b)zapobieganiazakleszczeniom.
:::
![](https://i.imgur.com/ylnEgnE.png)

Zakleszczenie(deadlock) - Zakleszczenie to stan, w którym każdy wątek czeka, aż inny wątek zwolni blokadę.

![](https://i.imgur.com/g8SZdSO.png)

Uwięzienie (livelock) - Livelock występuje, gdy dwa lub więcej procesów nieustannie powtarza tę samą interakcję w odpowiedzi na zmiany w innych procesach, nie wykonując żadnej użytecznej pracy. Te procesy nie są w stanie oczekiwania i działają jednocześnie. Różni się to od zakleszczenia, ponieważ w zakleszczeniu wszystkie procesy są w stanie oczekiwania.

Głodzienie (starvation) - mimo dostępności zasobu, odmawiamy dostępu jakiemuś wątkowi z niskim prioritetem. Na przykład, jeśli system wielozadaniowy zawsze przełącza się między pierwszymi dwoma zadaniami, podczas gdy trzecie nigdy się nie uruchamia, to trzecie zadanie jest głodzone(pozbawione czasu procesora).


Przykłady ze skrzyżowaniem:
**Deadlock**
![](https://i.imgur.com/AfYvQUx.png)
Każdy oczekuje na pojazd po prawej.
**Starvation**
![](https://i.imgur.com/Ple51oe.png)
![](https://i.imgur.com/3MdRgCD.png)
Poruszamy się na skrzyżowaniu tylko w jedną stronę.

**Livelock**
![](https://i.imgur.com/qQf59Nd.png)
Kiedy jesteśmy zablokowani przez nieudolny zbieg okoliczności cały czas(opis do obrazka: każdy ustępuje, a później każdy rusza, zmieniają swój stan, natomiast przez zbieg okoliczności zawsze znajdują się w pułapce)

a)
Jeśli zasoby mają jedną instancję:
W tym przypadku w celu wykrycia zakleszczenia możemy uruchomić algorytm sprawdzający cykl na wykresie alokacji zasobów. Obecność cyklu na wykresie jest warunkiem wystarczającym do zakleszczenia.
![](https://i.imgur.com/cyDahA4.png)
Na powyższym diagramie zasoby 1 i 2 mają pojedyncze instancje. Istnieje cykl R1 → P1 → R2 → P2. Tak więc deadlock został potwierdzony.
Metody Usuwania zakleszczenia:
- Zabijanie procesu: zabijanie całego procesu związanego z deadlockiem. Zabijanie jednego po drugim. Po zabiciu każdego procesu sprawdź ponownie, czy nie ma zakleszczenia, powtarzaj proces, aż system odzyska sprawność po zakleszczeniu.
- Wywłaszczanie zasobów: zasoby są wywłaszczane z procesów zaangażowanych w zakleszczenie, zasoby wywłaszczone są przydzielane innym procesom, dzięki czemu istnieje możliwość przywrócenia systemu z zakleszczenia.

b) Wycofać się z utrzymuj i czekaj
- Alokuj wszystkie wymagane dla wątku zasoby przed rozpoczęciem jego wykonywania, w ten sposób warunek wstrzymania i oczekiwania zostanie wyeliminowany, ale spowoduje to niskie wykorzystanie urządzenia.
- Proces wyśle nowe żądanie zasobów po zwolnieniu bieżącego zestawu zasobów. Takie rozwiązanie może prowadzić do głodzenia.


## Zadanie 10-3

Mamy kod:

```c=
const int n = 50;
shared int tally = 0;

void total() {
    for (int count = 1; count <= n; count++)
        tally = tally + 1;
}

void main() { 
    parbegin (total(), total()); 
}
```

Biorąc pod uwagę nieprzewidywalność w doborze kolejności wykonywania podanych dwóch wątków możemy dojść do wniosku, że maksymalna możliwa wartość $tally$, czyli $tally_{max}$ jest różna od minimalnej, czyli $tally_{min}$.

### 2 wątki

$$
tally_{min} == 2 \\
tally_{max} == 2n
$$

#### wartość $tally_{max}$

Jeśli wątki nie będą wchodziły sobie w drogę, to wykona się po kolei wczytywanie wartości $tally$, zwiększanie jej o $1$, a następnie zapisywanie. W takiej sytuacji wartość $tally$ będzie równa $tally_{max} == 2n$.

#### wartość $tally_{min}$

Może nastąpić sytuacja, w której 
1. pierwszy wątek $t_1$ wczyta zawartość $tally == 0$. 
2. drugi wątek $t_2$ również wczyta zawartość $tally==0$, ponieważ jej zawartość nie została jeszcze zmieniona. 
3. następnie $t_2$ przejdzie przez $n-1$ iteracji zwiększając $tally$
4. po tym wtrąci się $t_1$ zwiększając wczytane wcześniej przez niego $tally==0$ i nadpisując teraz zawartość zmiennej jako $tally \leftarrow 1$. 
5. $t_2$ zacznie ostatnią iterację od wczytania zawartości $tally == 1$
6. po wczytaniu zawartości $tally$ przez $t_2$ do rejestru, $t_1$ wykona swoje wszystkie kolejne iteracje zwiększając $tally$
7. $t_2$ dokończy ostatnią iterację pozostawiając $tally \leftarrow 2$

### k wątków

$$
tally_{min} == 2 \\
tally_{max} == kn
$$

#### wartość $tally_{max}$

To samo co w przypadku dwóch wątków. Żaden wątek nie wchodzi sobie w drogę, więc $tally$ zostanie $kn$ razy zwiększona o $1$.

#### wartość $tally_{min}$

Pomiędzy krokiem 3., a krokiem 4. wszystkie $k-2$ wątki przejdą przez swoje pętle (obojętnie jak). 
Następne kroki wykonuję się tak jak w przypadku dwóch wątków.

## Zadanie 10-4

![](https://i.imgur.com/Mgs4eFi.png)

##### pthread_create
```c=
int pthread_create(pthread_t *thread, const pthread_attr_t *attr, void *(*start_routine) (void *), void *arg)
```
Funkcja tworzy nowy wątek w procesie. `thread` wskazuje na bufor, w którym funkcja zapisuje ID tworzonego wątku. Parametr `attr` przechowuje atrybuty, z jakimi ma zostać utworzony wątek; ustanwienie go na `NULL` oznacza domyślne atrybuty. Wątek po utworzeniu rozpocznie wykonywanie funkcji podanej w `start_routine`. Argumenty funkcji przekazywanej w  `start_routine` należy umieścić w strukturze, a adres tej struktury podać w parametrze `arg`. Funkcja zwraca 0 w razie zakończenia powidzeniem albo numer błędu.


##### pthread_exit
```c=
void pthread_exit(void *retval)
```
Funkcja kończy działanie wątku. `retval` to wskaźnik na adres, pod którym zostanie umieszczony exitcode wątku.

##### pthread_join
```c=
int pthread_join(pthread_t thread, void **retval)
```
Funkcja czeka na zakończenie wątku podanego w `thread`. Jeśli `retval` nie ma wartości `NULL`, to exitcode wątka `thread` zostanie umieszczony pod adresem wskazywanym przez `retval`. Jeśli wątek został zakończony przez inny wątek, do `retval` trafia `PTHREAD_CANCELED`. Funkcja zwraca 0 w razie zakończenia powidzeniem albo numer błędu.

##### pthread_cleanup_push
```c=
void pthread_cleanup_push(void (*routine)(void *), void *arg)
```
Funkcja ta powoduje ustawienie funkcji podanej w `routine` jako handlera, który wywołuje się, gdy wątek wykona `pthread_exit`, zostanie na nim wywołany `pthread_cancel` albo wątek wywoła `pthread_cleanup_pop` z argumentm `execute` ustawionym na niezerową wartość. W `arg` jest przechowywany argument dla `routine` albo wskaźnik na strukturę argumentów, gdy jest ich więcej niż jeden. Takich handlerów dla wątku można ustawić więcej niż jeden, są one wrzucane na stos.

##### pthread_cancel
```c=
int pthread_cancel(pthread_t thread)
```
Funkcja wysyła do wątku podanego w `thread` żądanie zakończenia działania oraz ustawia jego exitcode na `PTHREAD_CANCELED`.

**wątki przyczepione** (ang. *attached*) -- inaczej *joinable*, na taki wątek można czekać przy użyciu `pthread_join` i pobrać jego exitcode. Po tej operacji zasoby zajmowane przez wątek są zwracane do systemu operacyjnego. Domyślnie wątki są tworzone jako przyczepione.

**wątki odczepione** (ang. *detached*) -- po zakończeniu działania wszystkie zasoby wątku są automatycznie zwalniane. Nie można uzyskać exitcode takiego wątku. Aby uczynić wątek odczepionym, trzeba ustawić to w atrybutach wątku przy użyciu funkcji `pthread_attr_setdetachstate`.

Akapit o przyczepionych i odczepionych wątkach z [Linux manual page dla `pthread_create`](https://man7.org/linux/man-pages/man3/pthread_create.3.html).

> A thread may either be joinable or detached.  If a thread is joinable, then another thread can call pthread_join(3) to wait for the thread to terminate and fetch its exit status.  Only when a terminated joinable thread has been joined are the last of its resources released back to the system.  When a detached thread terminates, its resources are automatically released back to the system: it is not possible to join with the thread in order to obtain
> its exit status.  Making a thread detached is useful for some types of daemon threads whose exit status the application does not need to care about.  By default, a new thread is created in a joinable state, unless attr was set to create the thread in a detached state (using pthread_attr_setdetachstate(3)).

## Zadanie 10-5

- Po wywołaniu `fork()` proces-dziecko składa się z jednego wątku - jest to kopia wątku w procesie-rodzicu, który zawołał `fork()`. Jednocześnie `fork()` powoduje stworzenie kopii przestrzenii adresowej rodzica, a więc również stanu wszystkich założonych blokad, zmiennych warunkowych. Blokady, które były założone przez inne wątki w trakcie wywołania `fork()` nie zostaną już nigdy zwolnione.
- Wywołanie `_exit()` - nawet jeśli tylko w jednym wątku powoduje zakończenie działania programu, a więc zakończenie pracy wszystkich wątków.
- Wywołanie `execve()` powoduje zastąpienie przestrzeni adresowej nową przestrzenią, więc również wszystkie wątki kończą swoje działanie niespodziewanie.
- W przypadku procedury obsługi sygnału, procedura taka jest rejestrowana dla wszystkich wątków, ale w momencie wysłania sygnału do procesu, sygnał jest odbierany na losowym (z punktu widzenia użytkownika) wątku. Wyjątkiem są sygnały związane z usterką sprzętu - sygnał taki jest zwykle odbierany w wątku, który spowodował wysłanie sygnału.
- Domyślnym zachowaniem przy przyjściu sygnały SIGPIPE jest zakończenie działania programu. W przypadku, gdy jeden wątek próbuje zapisać do rury, której drugi koniec został zamknięty, wygenerowany zostanie SIGPIPE, który spowoduje zakończenie działania całego programu, czyli również pracy innych wątków.
- Korzystając z jednego deskryptora plików w wielu wątkach (czytanie), wątki będą dzielić ten deskryptor, a więc również wszystkie skutki operacji wykonywanych na nim, tzn. kursor pliku będzie się przemieszczał dla wszystkich wątków. To oraz fakt, że nie możemy przewidzieć tego jak przeplatać będzie się działanie poszczególnych wątków sprawi, że każdy z nich będzie czytać "losowe" fragmenty pliku.

## Zadanie 10-6

Uzupełniona funkcja `main()` (zmianie uległy jedynie linie 17-26):

```c=
int main(int argc, char **argv) {
  if (argc != 5)
    app_error("usage: %s <textfile> <nthreads> <host> <port>\n", argv[0]);

  size_t nthreads = atol(argv[2]);
  assert(nthreads > 0 && nthreads <= THREADMAX);

  char *text = readtext(argv[1]);

  c_nlines = splitlines(text, &c_lines);
  c_host = argv[3];
  c_port = argv[4];

  Signal(SIGINT, sigint_handler);

  /* DONE: Start threads and wait for them to finish. */
  pthread_t threads[nthreads];
  size_t thread_no;

  for (thread_no = 0; thread_no < nthreads; thread_no++) {
    pthread_create(&threads[thread_no], NULL, &thread, NULL);
  }

  for (thread_no = 0; thread_no < nthreads; thread_no++) {
    pthread_join(threads[thread_no], NULL);
  }

  free(text);
}
```

Ponieważ mechanizm działania `pthread_join(3)` jest inny niż jego odpowiednika dla procesów (`wait()`) musimy śledzić utworzone wątki i czekać na każdy z nich z osobna. Cytując podręcznik systemowy:

> There is no pthreads analog of waitpid(-1, &status, 0), that is, "join with any terminated thread". If you believe you need this functionality, you probably need to rethink your application design.

Być może wynika to z dużo prostszej niż w przypadku procesów hierarchii - ponieważ zamiast drzewa tworzą one płaską strukturę pozbawioną relacji rodzic-dziecko, operacja "zaczekaj na wszystkie wątki" najprawdopodobniej oznaczałaby również czekanie na "(pra)\*wnuków", t.j. wątki utworzone nie przez wołający proces, a jego potomków, co niekoniecznie jest zachowaniem jakiego oczekiwalibyśmy od takiej procedury.


## Zadanie 10-7

fragment echoserver-poll.c który mieliśmy uzupełnić:

```c=

  while (!quit) {
    int nready = Poll(fds, nfds, 500);
    if (nready == 0)
      continue;

    /* TODO: If listening descriptor ready, add new client to the pool. */
    
    
    if ( fds[0].revents == POLLIN ) {

      struct sockaddr_storage clientaddr;
      socklen_t clientlen = sizeof(struct sockaddr_storage);
      int connfd = Accept(listenfd, (SA *)&clientaddr, &clientlen);
      

      char client_hostname[MAXLINE], client_port[MAXLINE];
      Getnameinfo((SA *)&clientaddr, clientlen, client_hostname, MAXLINE, client_port, MAXLINE, 0);
      
      addclient(connfd, client_hostname, client_port);
      nready--;
    }
    /* TODO: Echo a text line from each ready connected descriptor.
     * Delete a client when end-of-file condition was detected on socket. */
    int i = 1;
    while (nready > 0) {
      if ( fds[i].revents == POLLIN ) {
        if( !clientread(i) ) {
          delclient(i);
          i--;
        }
        nready--;
      }
      i++;
    }
  }
  
```

#### struktura pollfd:

```
 struct pollfd {
               int   fd;         /* file descriptor */
               short events;     /* requested events */
               short revents;    /* returned events */
           };
```

domyślnie events w programie jest ustawione na POLLIN:

```
POLLIN There is data to read.
```


## Zadanie 10-8

Bug-1
```c=
/* WARNING: This code is buggy! */
#include "csapp.h"

/* Global shared variable */
static volatile long cnt = 0; /* Counter */

/* Thread routine */
static void *thread(void *vargp) {
  long i, niters = *((long *)vargp);

  for (i = 0; i < niters; i++)
    cnt++;

  return NULL;
}

int main(int argc, char **argv) {
  /* Check input argument */
  if (argc != 2)
    app_error("usage: %s <niters>\n", argv[0]);

  long niters = atoi(argv[1]);
  pthread_t tid1, tid2;

  /* Create threads and wait for them to finish */
  Pthread_create(&tid1, NULL, thread, &niters);
  Pthread_create(&tid2, NULL, thread, &niters);
  Pthread_join(tid1, NULL);
  Pthread_join(tid2, NULL);

  /* Check result */
  if (cnt != (2 * niters)) {
    printf("BOOM! cnt=%ld\n", cnt);
    return EXIT_FAILURE;
  }

  printf("OK cnt=%ld\n", cnt);
  return EXIT_SUCCESS;
}
```
Problem pojawi się przy dużych wartościach niters.
Występuje tu wyścig między wątkami w dostępie do cnt. Potwierdza to Thread Sanitizer:
```
==================
WARNING: ThreadSanitizer: data race (pid=4736)
  Write of size 8 at 0x0000006020d0 by thread T2:
    #0 thread /home/ania/studia/czwarty semestr/so/so20_lista_10/bug-1.c:12 (bug-1+0x000000400c57)
    #1 <null> <null> (libtsan.so.0+0x0000000230d9)

  Previous read of size 8 at 0x0000006020d0 by thread T1:
    #0 thread /home/ania/studia/czwarty semestr/so/so20_lista_10/bug-1.c:12 (bug-1+0x000000400c42)
    #1 <null> <null> (libtsan.so.0+0x0000000230d9)

  Location is global 'cnt' of size 8 at 0x0000006020d0 (bug-1+0x0000006020d0)
[...]
SUMMARY: ThreadSanitizer: data race /home/ania/studia/czwarty semestr/so/so20_lista_10/bug-1.c:12 thread
==================
BOOM! cnt=11692
ThreadSanitizer: reported 1 warnings
```
Aby naprawić kod, używamy mutexa:
```c=
static volatile long cnt = 0; /* Counter */
pthread_mutex_t mutex;

/* Thread routine */
static void *thread(void *vargp) {
  long i, niters = *((long *)vargp);

  for (i = 0; i < niters; i++) {
    pthread_mutex_lock(&mutex);
    cnt++;
    pthread_mutex_unlock(&mutex);
  }

  return NULL;
}
```
Bug-2
```c=
/* WARNING: This code is buggy! */
#include "csapp.h"
#define N 4

static void *thread(void *vargp) {
  int myid = *((int *)vargp);
  printf("Hello from thread %d\n", myid);
  return NULL;
}

int main(void) {
  pthread_t tid[N];
  int i;

  for (i = 0; i < N; i++)
    Pthread_create(&tid[i], NULL, thread, &i);
  for (i = 0; i < N; i++)
    Pthread_join(tid[i], NULL);

  return EXIT_SUCCESS;
}
```
Tutaj problemem są wątki korzystające z wartości na stosie wątku głównego, która może się zmieniać.
```
==================
WARNING: ThreadSanitizer: data race (pid=5846)
  Read of size 4 at 0x7ffd02cc55cc by thread T1:
    #0 thread /home/ania/studia/czwarty semestr/so/so20_lista_10/bug-2.c:6 (bug-2+0x000000400beb)
    #1 <null> <null> (libtsan.so.0+0x0000000230d9)

  Previous write of size 4 at 0x7ffd02cc55cc by main thread:
    #0 main /home/ania/studia/czwarty semestr/so/so20_lista_10/bug-2.c:15 (bug-2+0x000000400c76)

  Location is stack of main thread.

  [...]

SUMMARY: ThreadSanitizer: data race /home/ania/studia/czwarty semestr/so/so20_lista_10/bug-2.c:6 thread
==================
Hello from thread 2
Hello from thread 0
Hello from thread 0
Hello from thread 0
ThreadSanitizer: reported 1 warnings
```
Aby naprawić ten problem, skorzystamy z malloca aby zapisać aktualną wartość i.
```c=
static void *thread(void *vargp) {
  int myid = *((int *)vargp);
  printf("Hello from thread %d\n", myid);
  free(vargp);
  return NULL;
}

int main(void) {
  pthread_t tid[N];
  int i;

  for (i = 0; i < N; i++) {
    int *j = Malloc(sizeof(int));
    *j = i;
    Pthread_create(&tid[i], NULL, thread, j);
  }
  for (i = 0; i < N; i++)
    Pthread_join(tid[i], NULL);

  return EXIT_SUCCESS;
}
```

