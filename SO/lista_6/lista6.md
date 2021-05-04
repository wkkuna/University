
## Zadanie 6-1

**Tożsamość** to opis użytkownika ułatwiający systemowi operacyjnemu zarządzenie kontrolą dostępów. W rzeczywistości jest to krotka trzech liczb: rzeczyiwsty (*real id*), obowiązujący (*effective if*), zachowany (*saved-set user id*).

Początkowa tożsamość procesu w tym zadaniu to `ruid=1000, euid=0, suid=0`.

a) `setuid(2000)` $\rightarrow$ `ruid=2000, euid=2000, suid=2000`, bo byliśmy superużytkownikiem

b) `setreuid(-1, 2000)` $\rightarrow$ `ruid=1000, euid=2000, suid=2000`, ustawia `ruid` i `euid`, chyba że `-1`, to wtedy zostawia to co było

c) `seteuid(2000)` $\rightarrow$ `ruid=1000, euid=2000, suid=0`

d) `setresuid(-1, 2000, 3000)` $\rightarrow$ `ruid=1000, euid=2000, suid=3000`

Czy proces z tożsamością `ruid=0, euid=1000, suid=1000` jest uprzywilejowany?

Nie jest, ale możemy jeszcze bez pomocy uprzywilejowanego użytkownika sprawić, aby był (`seteuid(0)`).

## Zadanie 6-2

**upoważnienie** - proces sprawdzania, czy proces o zadanej tożsamości ma dostęp do zasobu

**Jaką  rolę  pełnią  bity  uprawnień  `rwx`  dla  katalogów  w  systemach  uniksowych?**

- `r` - uprawnia do wyświetlania zawartości katalogu
- `w` - uprawnia do modyfikacji katalogu poprzez tworzenie lub kasowanie plików/katalogów. Wymagane jest uprawnienie `x`
- `x` - uprawnia do dostania się do katalogu (ustawnienie tego katalogu jako katalogu roboczego)


**Opisz  znaczenie  bitów  «set-gid»  i  «sticky»  dla  katalogów.**

- `set-gid` - ustawiony na katalogu powoduje, że pliki i podkatalogi dziedziczą grupę przypisaną do katalogu
- `sticky` - pliki mogą być usuwane lub przemianowywane tylko przez właściciela pliku lub owego katalogu, lub jeśli proces ma prawo ich modyfikacji.

**Procedura w psuedokodzie**

```c=
bool my_access(struct stat* sb, int mode)
```

```text=
perm <- uprawnienia rwx z mode, używając makr R_OK, W_OK oraz X_OK;
// user (USR)
Jeśli sb->st_mode==getuid(), czyli gdy jest właścicielem pliku
    Jeśli uprawnienia rwx użytkownika zawarte w sb->st_mode (makra S_IRUSR, S_IWUSR, S_IXUSR) są równe perm
        zwróć prawdę
        wpp zwróć fałsz
// group (GRP)
Dla każdej grupy z getgroups()
    Jeśli ID grupy == sb->st_gid
        Jeśli uprawnienia grupy w sb->st_mode (makra S_IRGRP, S_IWGRP, S_IXGRP) są równe perm
            zwróć prawdę
            wpp zwróć fałsz
// other (OTH)
Sprawdź, czy uprawnienia dla innych użytkowników z sb->st_mode (makra S_IROTH, S_IWOTH, S_IXOTH) są równe perm.
```

## Zadanie 6-3

**Uwierzytelnianie** to proces polegający na dowiedzeniu swojej deklarowanej tożsamości przez coś lub kogoś, w rozważanym tutaj wypadku na podstawie weryfikacji "sekretnej wiedzy" w postaci hasła.

`su` rozpocznie pracę z tożsamością: ruid=1000, euid=0, suid=0


1. Ustalamy, kim jest użytkownik "docelowy" - jeśli nie został podany przez użytkownika wywołującego `su`, przyjmujemy, że jest nim `root`.
2. Za pomocą funkcji `getspnam` wyciągamy odpowiedni (na podstawie nazwy) rekord z `/etc/shadow`, reprezentowany jako:

   ```
   struct spwd {
     char          *sp_namp; /* user login name */
     char          *sp_pwdp; /* encrypted password */
     long int      sp_lstchg; /* last password change */
     long int      sp_min; /* days until change allowed. */
     long int      sp_max; /* days before change required */
     long int      sp_warn; /* days warning for expiration */
     long int      sp_inact; /* days before account inactive */
     long int      sp_expire; /* date when account expires */
     unsigned long int  sp_flag; /* reserved for future use */
   }
   ```
3. Sprawdzamy, czy _wywołujący_ użytkownik jest rootem - jeśli tak, przeskakujemy do punktu 4.
4. Oglądamy pierwszy bajt `sp_pwdp` w powyższej strukturze. Jeśli nie jest nim `$`,
    uznajemy, że konto, do którego użytkownik próbował się dostać wyłączyło możliwość
    logowania się na nie przy użyciu hasła, bezwarunkowo odmawiamy dostępu i kończymy działanie.
5. Rozpoczynamy proces pytania użytkownika o hasło - zaczynamy od ustawienia terminala w tryb raw (`cfmakeraw()`), w którym to trybie echo jest wyłączone, a input nie podlega buforowaniu - będzie dostępny bajt po bajcie.
6. Rejestrujemy (nie robiący nic ciekawego) handler do obsłużenia sygnału SIGINT, dzięki czemu nadesłany od usera ctrl+C nie zakończy się natychmiastową terminacją całego procesu, a zamiast tego pozwoli użytkownikowi na zakomunikowanie
    utraty chęci do dalszej współpracy.
7. Czytamy (pojedynczo) wpisywane przez usera bajty, w razie błędu (wynikłego z np przerwania wykonania przez wspomniany wyżej SIGINT) lub informacji o końcu transmisji (np 0 == read(...)) przerywamy i kończymy działanie z błędem.
    W przypadku napotkania backspace'a usuwamy poprzednio podany znak.
    Kontynuujemy proces aż do napotkania znaku końca linii lub powrotu karetki.
8. Przywracamy ustawienia terminala oraz obsługi sygnałów do ich poprzednich wartości.
9. Za pomocą `crypt(3)` generujemy ("posolony") hash otrzymanego przed chwilą ciągu znaków - użyta sól oraz algorytm są zawarte w `sp_pwdp`.
10. Jeśli wygenerowany string różni się od prawidłowego -> odmawiamy dostępu
11. Przy użyciu `getpwnam(3)` wymieniamy nazwę użytkownika _docelowego_ na reprezentujący go `struct passwd`.
12. Używając `initgroups()`, `setgid()` oraz `setuid()` zmieniamy tożsamość procesu na tę należącą do użytkownika, za którego chcemy się podać.
   Jest to możliwe dzięki bitowi set-uid ustawionemu na pliku wykonywalnym `su`.
13. W zależności od podanych w argumentach programu flag resetujemy (bądź nie) zmienne środowiskowe
14. Na podstawie reszty flag szykujemy odpowiedni shell oraz przekazujemy mu (o ile jakaś była) pożądaną przez użytkownika wywołującego komendę

## Zadanie 6-4

**Program uprzywilejowany** ma ustawiony bit set-user-ID (set-group-ID) przez co jego obowiązujący identyfikator ustawiany jest na identyfikator użytkownika, który go stworzył, a nie który go uruchomił.

Uprzywilejowane programy powinny być projektowane z **jak najmniejszym zestawem uprawnień** by zapobiegać problemom z bezpieczeństwem i żeby ograniczyć potencjalne szkody, które dany program mógłby wyrządzić.

Większość programów potrzebuje wykonać konkretne operacje (np. zapis do pliku, do którego nie ma dostępu), stąd też nie potrzebuje zestawu uprawnień superużytkownika. Wystarczy stworzyć **grupę dającą odpowiednie przywileje**. Zwiększy to nasze bezpieczeństwo i zmniejszy ewentualny zasięg błędów w przypadku nieprawidłowego działania.

Ponadto należy pamiętać o **pozbywaniu się przywilejów jak szybko jest to możliwe**. Używamy odpowiednich funkcji, gdy chcemy pozbyć się przywilejów **tymczasowo** (*seteuid()*, *setegid()*) lub **permamentnie** (*setreuid()*, *setregid()*) - należy pamiętać o zachowanym id.

**Przed wywołaniem *exec()*** powinniśmy **pozbyć się niepotrzebnych przywilejów** jak i zamknąć pliki, do których mieliśmy uprzywilejowany dostęp.

Należy też **unikać wykonywania powłoki** ani interpreterów takich jak awk bez uprzedniego pozbycia się przywilejów. Nawet jeśli nie umożliwia ona interakcji, nie da się przewidzieć ewentualnych luk bezpieczeństwa w tak złożonych programach.


Standardowy zestaw funkcji unix do implementacji programów uprzywilejowanych zawiera jedną dużą wadę. W przypadku, gdy chcemy pozwolić procesowi wykonać operację, do której uprawnienia ma tylko superużytkownik (np. zmiana czasu) musimy dać mu uprawnienia superużytkownika. Pozwalając mu także na np. wgląd i władzę nad ważnymi plikami. W ten sposób tworzymy dużą lukę bezpieczeństwa, która może zostać wykorzystana przez błąd programu, nieuwagę użytkownika lub po prostu złośliwe programy. 


Zdolności dzielą przywileje superużytkownika na małe części. Tym samym chcąc upoważnić proces do zmiany czasu systemowego nie będzie on mógł przeczytać naszych kluczy prywatnych.

Zdolność:
- **CAP_DAC_READ_SEARCH** pozwala ominąć sprawdzanie uprawnień do odczytu pliku i odczytu i wykonywania katalogów (pozwala się przez nie swobodnie przemieszczać),
- **CAP_KILL** pozwala ominąć sprawdzanie uprawnień do wysyłania sygnałów,

Sygnały mogą być wysyłane do innego procesu jeśli:
- proces jest uprzywilejowany (zdolność CAP_KILL),
- rzeczywisty lub zachowany id procesu wysyłającego sygnał jest taki sam jak rzeczywisty lub zachowany id procesu docelowego.
(wyjątkiem jest SIGCONT - wystarczy wtedy, że procesy należą do tej samej sesji)


## Zadanie 6-5

W przypadku wywołań **fork** problemem jest skopiowanie zawartości bufforów stdio. Może to spowodować duplikację wypisywanych danych. fflush(NULL) przed fork() zapobiegnie temu poprzez spłukanie wszystkich bufforów.

Dla **execve** problematyczny może być odczyt. Załóżmy następującą sytuację:
1. wysyłamy 'asdfghjkl\n' do wejścia programu #1
2. program #1 wywołuje fgets(buf, 1, stdin)
3. program #1 drukuje zawartość buf
4. program #1 wywołuje execve(#2)
5. program #2 wywołuje fgets(buf, 1, stdin)
6. program #2 drukuje zwartość buf

Wynikiem działania tego programu będzie 'a', mimo że moglibyśmy się spodziewać 'as'. Jest tak dlatego, że fgets() wywoła pod spodem read(stdin, 'asdfghjkl\n', 4096) = 10, co wczyta całą linię do bufora. Wtedy wywołanie fgets() w programie #2 będzie próbowało odczytać puste stdin. Można zapobiec temu problemowi przez wyłączenie buforowania.

Strategie buforowania:
a) buforuj do napotkania znaku nowej linii, bądź przepełnienia bufora,
b) buforuj do przepełnienia bufora,
c) nie buforuj, by brak pamięci nie przeszkodził w wypisaniu błędu

Rozwiązania dla SIGINT:
1) Nie buforować. Zadziała ale zapłacimy dużą stratą wydajności,
2) Blokować sygnał SIGINT na czas wykonywania operacji stdio i w handlerze wywołać fflush(NULL). Problematyczne, bo musimy starannie blokować sygnał dla każdej operacji na stdio oraz fflush nie jest tak naprawdę bezpieczną funkcją do użycia w obsłudze przerwań.
3) W miejscach, w których używamy stdio sprawdzać co jakiś czas flagę, którą ustawimy w obsłudze sygnału. Po zauważeniu zapalonej flagi wywołać fflush(NULL) w standardowym przepływie programu i zamknąć program.

## Zadanie 6-6

**Buforowanie liniami** - sposób buforowania, w którym znaki są zapisywane do bufora, a ten jest opróżniany dopiero w momencie napotkania znaku nowej linii. Ten rodzaj buforowania jest stosowany w przypadku komunikacji z terminalem.

**Buforowanie pełne** - rodzaj buforowania, w którym znaki są procesowane w blokach - bufor jest opróżniany, gdy bufor wielkości bloku się zapełni. Domyślne buforowanie w przypadku interakcji ze zwykłymi plikami.

* **write**
```c=
  if (strcmp(choice, "write") == 0) {
    for (int j = 0; j < times; j++)
      for (int k = 0; k < length; k++)
        write(STDOUT_FILENO, line + k, length + 1 - k); 
  }
```

* **fwrite, fwrite-line, fwrite-full**
```c=
  if (strncmp(choice, "fwrite", 6) == 0) {
    size_t size;
    int mode;
    void *buf; 

    if (strcmp(choice, "fwrite-line") == 0) {
      mode = _IOLBF;
      size = length + 1;
    } else if (strcmp(choice, "fwrite-full") == 0) {
      mode = _IOFBF;
      size = getpagesize();
    } else {
      mode = _IONBF;
      size = 0;
    }

    /* TODO: Attach new buffer to stdout stream. */
    buf = malloc(size);
    setvbuf(stdout, buf, mode, size);

    for (int j = 0; j < times; j++)
      for (int k = 0; k < length; k++)
        fwrite(line + k, length + 1 - k, 1, stdout); 
    fflush(stdout);

    free(buf);
  }
```

* **writev**
```c=
  if (strcmp(choice, "writev") == 0) {
    int n = sysconf(_SC_IOV_MAX);
    struct iovec iov[n];
    /* TODO: Write file by filling in iov array and issuing writev. */
    for (int k = 0; k < length; k++) {
	 iov[k].iov_base = line + k;
	 iov[k].iov_len = length + 1 - k;
    }
    for (int j = 0; j < times; j++)
	 writev(STDOUT_FILENO, iov, length);
  }
```

Wyniki testów:
```
Method: write

real    0m2.084s
user    0m0.420s
sys     0m1.589s

Method: fwrite

real    0m2.146s
user    0m0.461s
sys     0m1.593s

Method: fwrite-line

real    0m2.122s
user    0m0.496s
sys     0m1.552s

Method: fwrite-full

real    0m0.463s
user    0m0.119s
sys     0m0.322s

Method: writev

real    0m0.394s
user    0m0.000s
sys     0m0.371s
```

Dodatkowe opcje `-t 1 -l 1000`:

|    Opcja    | Liczba wywołan `write` |
|:-----------:|:----------------------:|
|    write    |         1000          |
|   fwrite    |         1000          |
| fwrite-line |         1000          |
| fwrite-full |          123           |
|   writev    |           1            |

Możemy zauważyć, że mała liczba wywołań `write` bezpośrednio pozytywnie wpływa na wydajność programu - im mniej wywołań tym mniej szybszy czas działania.

:::spoiler Rozwiązanie v2
```c=
if (strcmp(choice, "writev") == 0) {
  int n = sysconf(_SC_IOV_MAX);
  struct iovec iov[n];

  int cnt = 0;
  for (int i = 0; i < times; ++i) {
    for (int j = 0; j < length; ++j) {
      iov[cnt].iov_base = line + j;
      iov[cnt].iov_len = length + 1 - j;
      cnt++;

      if(cnt == n) {
        Writev(STDOUT_FILENO, iov, n);
        cnt = 0;
      }
    }
  }

  if(cnt)
    Writev(STDOUT_FILENO, iov, cnt);
}
```

Dodatkowe opcje `-t 1000 -l 1000`:
Ostatnia opcja woła _writev_ zamiast _write_.

|    Opcja    | Liczba wywołan `write` |
|:-----------:|:----------------------:|
|    write    |         $10^6$         |
|   fwrite    |         $10^6$         |
| fwrite-line |         $10^6$         |
| fwrite-full |         $122437$       |
|   writev    |         $977$          |
:::

## Zadanie 6-7

Tożsamość procesu Uniksowego
* użytkownik → getuid(2)
* grupa podstawowa → getgid(2)
* grupy rozszerzone → getgroups(2)

```c= 
#include "csapp.h"

static const char *uidname(uid_t uid) {
  /* TODO: Something is missing here! */
  return getpwuid(uid)->pw_name;
}

static const char *gidname(gid_t gid) {
  /* TODO: Something is missing here! */
  return getgrgid(gid)->gr_name;
}

static int getid(uid_t *uid_p, gid_t *gid_p, gid_t **gids_p) {
  gid_t *gids = NULL;
  int ngid = 2;
  int groups;

  /* TODO: Something is missing here! */
  *uid_p = getuid();
  *gid_p = getgid();
  
  //Jeśli rozmiar wynosi zero, lista nie jest modyfikowana, 
  //ale zwracana jest liczba dodatkowych identyfikatorów grup dla procesu.
  ngid = getgroups(0, gids);
  if((gids = realloc(gids, sizeof(gid_t)*ngid)) != NULL) {
    groups = getgroups(ngid,gids);
  } else {
    exit(-1);
  }
  
  *gids_p = gids;
  return groups;
}

int main(void) {
  uid_t uid;
  gid_t *gids, gid;
  int groups = getid(&uid, &gid, &gids);

  printf("uid=%d(%s) gid=%d(%s) ", uid, uidname(uid), gid, gidname(gid));
  printf("groups=%d(%s)", gids[0], gidname(gids[0]));
  for (int i = 1; i < groups; i++)
    printf(",%d(%s)", gids[i], gidname(gids[i]));
  putchar('\n');

  free(gids);

  return 0;
}
```

