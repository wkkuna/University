
## Zadanie 4-1

Wywołania read(2) i write(2) nie działają na katalogach, ponieważ to system zarządza strukturą katalogu. Dzięki temu, że nie możemy dowolnie manipulować bitami reprezentującymi dane katalogu, a modyfikować je przeznaczonymi do tego wywołaniami, mamy gwarancję spójności.

**rekord katalogu** jest to krotka w postaci (nazwa_pliku, inode), która mapuje plik po nazwie do miejsca na dysku. Katalog składa się z wielu takich krotek.

*getdents(2)* - wczytuje podaną liczbę rekordów katalogu do bufora
*open(2)* - otwiera plik i zwraca fd
*close(2)* - zamyka plik dla podanego fd
*opendir(3)* - otwiera strumień pozwalający wczytywać rekordy katalogu
*closedir(3)* - zamyka wcześniej otwarty strumień
![](https://i.imgur.com/XO9w1iq.png)


![](https://i.imgur.com/qV6XSKZ.png)

Zawartość katalogu nie jest posortowana. Jest to oczekiwane pod względem wydajności, bo gdyby system utrzymywał np. kolejność leksykalną to dodanie jednego pliku mogłoby wywołać przeniesienie dużej ilości danych.


**metadane** pliku to dane opisujące plik. Możemy odczytać je przy pomocy polecenia *stat*. Przykładowe metadane to data modyfikacji, data stworzenia, rozmiar, uprawnienia, inode.
![](https://i.imgur.com/lJAwIg0.png)

**dowiązanie** (hard link) to plik, który posiada inną ścieżkę, lecz wskazuje na ten sam inode co inny plik.

Nie możemy ręcznie tworzyć dowiązań dla katalogów. Są one tworzone przez system. W każdym katalogu mamy dowiązanie '.', które reprezentuje obecny katalog, oraz dowiązanie '..', które reprezentuje rodzica. Oznacza to, że jeśli nasz katalog / ma n dowiązań to mamy n-2 podkatalogów.

## Zadanie 4-2

**Jednokierunkowość** w przypadku pipe oznacza, że poprzez rurę możemy przesyłać dane, ale tylko w jedną stronę, to znaczy jeden proces pisze do rury, a drugi z niej czyta.

**Bufor** rury to miejsce w pamięci, gdzie zapisujemy dane które przekazują sobie procesy, w pamięci jądra, ma skończoną długość.

Zachowanie `write` gdy bufor rury jest:

* pusty -- po prostu zapisze,
* pełny -- czeka zablokowany na dane, chyba że flaga `O_NONBLOCK` jest ustawiona, wtedy będzie błąd.

Zachowanie `read` gdy bufor rury jest:

* pusty -- uśpi się do momentu gdy coś się pojawi (druga strona napisze) lub gdy druga strona zostanie zamknięta,
* pełny -- odczyta.

Zapisy są **atomowe**, to znaczy niepodzielne, czyli nie może się stać tak, że zapisywane dane się przeplotą, np. gdy zapisujemy `aa` i `bb` to dostaniemy `aabb` lub `bbaa`, ale na pewno nie `abab` czy `baab`.

Jeśli zamkniemy koniec odpowiedzialny za `write`, to na drugim końcu rury przestaniemy czekać na `read` (dostaniemy znak EOF -- koniec pliku), jeśli zamkniemy `read`, to nie będziemy mogli już odczytać rzeczy przekazywanych z drugiego końca i proces, który zamknął `read` wyśle sygnał `SIGPIPE` do drugiego procesu. Jeśli zostanie on zignorowany, to przy wywołaniu `write` otrzymamy błąd `EPIPE`. Short count otrzymujemy większy od 0, gdy na przykład chcieliśmy przeczytać 4 bajty, a przeczytaliśmy 3, wtedy short count wynosi 1. Short count może wystąpić wtedy, gdy mamy `wrtie` więcej niż `PIPE_BUF` znaków (bo dla mniejszej liczby mamy atomowość) i ustawioną flagę `O_NONBLOCK`, wtedy możemy zapisać mniej chcemy i wystąpi short count, a w przypadku `read` gdy mamy w buforze mniej niż chcemy odczytać.

Czy można połączyć rodzica i dziecko rurą, która została utworzona po uruchomieniu dziecka?

Nie, jeśli wywołamy `pipe()` po `fork()`, to zarówno w dziecku jak i rodzicu utworzy się rura, ale będą to kompletnie dwie różne, niepowiązane rury. Ewentualnie jeśli istnieje już jakaś rura między nimi, to wtedy można u jednego z procesów stworzyć nową rurę i przesłać jej deskryptory do durgiego procesu, ale to i tak wymaga stworzonej przed `fork` rury między nimi.

## Zadanie 4-3

**potok** -- jest to zbiór procesów połączonych razem w taki sposób, że wyjście pierwszego to wejście drugiego, wyjście drugiego, to wejście trzeciego itd. Procesy te działają współbieżnie.

:::spoiler Kolejność wywołań z zadania z ```sudo strace -e trace=process,openat,dup2,close,pipe -f -p 10218```
```bash=
strace: Process 10218 attached
pipe([3, 4])                            = 0 #rura między ps a grep
pipe([5, 6])                            = 0   
clone(strace: Process 10338 attached
child_stack=NULL, flags=CLONE_CHILD_CLEARTID|CLONE_CHILD_SETTID|SIGCHLD, child_tidptr=0x7f4d90123a10) = 10338
[pid 10218] close(4)                    = 0
[pid 10218] close(4)                    = -1 EBADF (Bad file descriptor)
[pid 10218] pipe([4, 7])                = 0 #rura między grep a wc
[pid 10218] clone( <unfinished ...>
[pid 10338] close(6)                    = 0
strace: Process 10339 attached
[pid 10218] <... clone resumed> child_stack=NULL, flags=CLONE_CHILD_CLEARTID|CLONE_CHILD_SETTID|SIGCHLD, child_tidptr=0x7f4d90123a10) = 10339
[pid 10218] close(3)                    = 0
[pid 10218] close(7)                    = 0
[pid 10218] close(3)                    = -1 EBADF (Bad file descriptor)
[pid 10218] close(7)                    = -1 EBADF (Bad file descriptor)
[pid 10218] clone( <unfinished ...>
[pid 10339] close(5)                    = 0
[pid 10339] close(6)                    = 0
strace: Process 10340 attached
[pid 10339] close(4 <unfinished ...>
[pid 10218] <... clone resumed> child_stack=NULL, flags=CLONE_CHILD_CLEARTID|CLONE_CHILD_SETTID|SIGCHLD, child_tidptr=0x7f4d90123a10) = 10340
[pid 10339] <... close resumed> )       = 0
[pid 10339] dup2(3, 0)                  = 0    #kopiujemy odpowiedni koniec potoka, jako stdin dla grep (rura od ps)
[pid 10339] close(3)                    = 0
[pid 10339] dup2(7, 1)                  = 1    #kopiujemy odpowiedni koniec potoka jako stdout dla grep (rura do wc)
[pid 10339] close(7)                    = 0
[pid 10218] close(4)                    = 0
[pid 10340] close(5)                    = 0
[pid 10340] close(6)                    = 0
[pid 10340] dup2(4, 0)                  = 0    #kopiujemy odpowiedni koniec potoka, jako stdin dla wc (rura od grep)
[pid 10340] close(4)                    = 0
[pid 10218] close(5)                    = 0
[pid 10218] close(6)                    = 0
[pid 10338] close(5)                    = 0
[pid 10338] close(3)                    = 0
[pid 10338] dup2(4, 1)                  = 1    #kopiujemy odpowiedni koniec potoka, jako stdout dla ps (rura do grep)
[pid 10338] close(4)                    = 0
[pid 10339] execve("/bin/grep", ["grep", "--color=auto", "sh"], 0x561136014070 /* 62 vars */ <unfinished ...>
[pid 10340] openat(AT_FDCWD, "cnt", O_WRONLY|O_CREAT|O_TRUNC, 0666 <unfinished ...>
[pid 10218] wait4(-1,  <unfinished ...>
[pid 10340] <... openat resumed> )      = 3
[pid 10340] dup2(3, 1)                  = 1    #jest to stdout dla wc (cnt)
[pid 10340] close(3 <unfinished ...>
[pid 10339] <... execve resumed> )      = 0
[pid 10340] <... close resumed> )       = 0
[pid 10340] execve("/usr/bin/wc", ["wc", "-l"], 0x561136014070 /* 62 vars */ <unfinished ...>
[pid 10339] openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
[pid 10339] close(3)                    = 0
[pid 10339] openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libpcre.so.3", O_RDONLY|O_CLOEXEC <unfinished ...>
[pid 10340] <... execve resumed> )      = 0
[pid 10339] <... openat resumed> )      = 3
[pid 10338] execve("/bin/ps", ["ps", "-ef"], 0x561136014070 /* 62 vars */ <unfinished ...>
[pid 10340] openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
[pid 10340] close(3)                    = 0
[pid 10339] close(3)                    = 0
[pid 10338] <... execve resumed> )      = 0
[...]
[pid 10338] close(6)                    = 0
[pid 10338] close(5)                    = 0
[pid 10338] close(1)                    = 0
[pid 10338] close(2 <unfinished ...>
[pid 10339] close(1 <unfinished ...>
[pid 10338] <... close resumed> )       = 0
[pid 10339] <... close resumed> )       = 0
[pid 10339] close(2)                    = 0
[pid 10339] exit_group(0 <unfinished ...>
[pid 10338] exit_group(0 <unfinished ...>
[pid 10339] <... exit_group resumed>)   = ?
[pid 10338] <... exit_group resumed>)   = ?
[pid 10339] +++ exited with 0 +++
[pid 10218] <... wait4 resumed> [{WIFEXITED(s) && WEXITSTATUS(s) == 0}], WSTOPPED|WCONTINUED, NULL) = 10339
[pid 10218] wait4(-1,  <unfinished ...>
[pid 10338] +++ exited with 0 +++
[pid 10340] close(0 <unfinished ...>
[pid 10218] <... wait4 resumed> [{WIFEXITED(s) && WEXITSTATUS(s) == 0}], WSTOPPED|WCONTINUED, NULL) = 10338
[pid 10340] <... close resumed> )       = 0
[pid 10218] wait4(-1,  <unfinished ...>
[pid 10340] close(1)                    = 0
[pid 10340] close(2)                    = 0
[pid 10340] exit_group(0)               = ?
[pid 10340] +++ exited with 0 +++
<... wait4 resumed> [{WIFEXITED(s) && WEXITSTATUS(s) == 0}], WSTOPPED|WCONTINUED, NULL) = 10340
close(4)                                = -1 EBADF (Bad file descriptor)
--- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=10339, si_uid=1000, si_status=0, si_utime=0, si_stime=0} ---
wait4(-1, 0x7ffc58c0e090, WNOHANG|WSTOPPED|WCONTINUED, NULL) = -1 ECHILD (No child processes)
```
:::

Możemy zauważyć stąd, że wszystkie programy są klonowane z terminala (za pomocą _clone_). Są one tworzone w kolejności takiej, jakiej podaliśmy polecenie (czyli _ps_, później _grep_, a na końcu _wc_), aczkolwiek exec już jest w trochę innej kolejności -- najpierw jest _grep_, później _ps_, a na końcu _wc_.
Na koniec mamy _wait4_, którym czekamy na procesy potomne.

_Execve_ może zwrócić błąd np. przy próbie uruchomienia pliku, który nie jest wykonywalny (tj. nie ma uprawnień). Jeśli jest to ostatni program, to zwróci on błąd _execve_, a wpp. otrzymamy to co zwróci ostatni program. Po prostu to co się dzieje, to kolejne rury za tym programem co sfailował _execve_ będą otrzymywały $EOF$. Poprzednie otrzymają $SIG\_PIPE$.

Na przykładzie ```./1 | cat | grep x```, który jest śledzony przy użyciu ```strace``` otrzymujemy, że potok zwróci wówczas $1$ zamiast $0$ (oznacza to błąd wykonania), ponieważ _grep_ jak nie znajdzie żadnego dopasowania to zwraca $1$. Gdyby zamiast _grep_ był _wc_ to otrzymalibyśmy wynik $1$.


:::spoiler Co jeśli _execve_ zwróci błąd?
```bash=
strace: Process 21070 attached
clone(child_stack=NULL, flags=CLONE_CHILD_CLEARTID|CLONE_CHILD_SETTID|SIGCHLD, child_tidptr=0x7f469b004a10) = 22239
strace: Process 22239 attached
[pid 21070] clone(strace: Process 22240 attached
child_stack=NULL, flags=CLONE_CHILD_CLEARTID|CLONE_CHILD_SETTID|SIGCHLD, child_tidptr=0x7f469b004a10) = 22240
[pid 21070] clone(child_stack=NULL, flags=CLONE_CHILD_CLEARTID|CLONE_CHILD_SETTID|SIGCHLD, child_tidptr=0x7f469b004a10) = 22241
strace: Process 22241 attached
[pid 22240] execve("/bin/cat", ["cat"], 0x56391fe03430 /* 62 vars */) = 0
[pid 22241] execve("/bin/grep", ["grep", "--color=auto", "x"], 0x56391fe03430 /* 62 vars */ <unfinished ...>
[pid 21070] wait4(-1,  <unfinished ...>
[pid 22239] execve("./1", ["./1"], 0x56391fe03430 /* 62 vars */ <unfinished ...>
[pid 22241] <... execve resumed> )      = 0
[pid 22239] <... execve resumed> )      = -1 EACCES (Permission denied)
[pid 22240] arch_prctl(ARCH_SET_FS, 0x7fcd0dbda540) = 0
[pid 22241] arch_prctl(ARCH_SET_FS, 0x7f4d41a1ab80) = 0
[pid 22239] exit_group(126)             = ?
[pid 22239] +++ exited with 126 +++
[pid 21070] <... wait4 resumed> [{WIFEXITED(s) && WEXITSTATUS(s) == 126}], WSTOPPED|WCONTINUED, NULL) = 22239
[pid 21070] wait4(-1,  <unfinished ...>
[pid 22240] exit_group(0)               = ?
[pid 22240] +++ exited with 0 +++
[pid 21070] <... wait4 resumed> [{WIFEXITED(s) && WEXITSTATUS(s) == 0}], WSTOPPED|WCONTINUED, NULL) = 22240
[pid 21070] wait4(-1,  <unfinished ...>
[pid 22241] exit_group(1)               = ?
[pid 22241] +++ exited with 1 +++
<... wait4 resumed> [{WIFEXITED(s) && WEXITSTATUS(s) == 1}], WSTOPPED|WCONTINUED, NULL) = 22241
--- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=22239, si_uid=1000, si_status=126, si_utime=0, si_stime=0} ---
wait4(-1, 0x7ffd8d0eea10, WNOHANG|WSTOPPED|WCONTINUED, NULL) = -1 ECHILD (No child processes)
```
:::

## Zadanie 4-4

**urządzenie znakowe** --- urządzenie, w którym operacja wejścia/wyjścia realizowana jest przez transfer strumienia bajtów bez możliwości zaadresowania konkretnego fragmentu danych, np. port szeregowy, terminal.
**urządzenie blokowe** --- urządzenie, które umożliwia odczyt/zapis danych w blokach ustalonego rozmiaru (z reguły 512B oraz wielokrotności tej liczby) z możliwością adresowania konkretnego bloku, np. dyskietka, płyta CD, dysk twardy.

Wywołanie `ioctl(2)` (input/output control) służy do manipulowania urządzeniami. Wykonuje polecenie kodowane przez `request`. Trzeci parametr jest argumentem dla tego polecenia.

`int ioctl(int d, unsigned long request, ...)`

`request` ma następującą strukturę:
```
/*
 * Ioctl's have the command encoded in the lower word, and the size of
 * any in or out parameters in the upper word.  The high 3 bits of the
 * upper word are used to encode the in/out status of the parameter.
 *
 *	 31 29 28                     16 15            8 7             0
 *	+---------------------------------------------------------------+
 *	| I/O | Parameter Length        | Command Group | Command       |
 *	+---------------------------------------------------------------+
 */
```
Znaczenie pól:
I/O --- określa rodzaj argumentu wykonywanego polecenia (parametr wejścia, wyjścia, wejścia/wyjścia).
Parameter Length --- rozmiar argumentu (w bajtach) podanego poprzez "..."
Command Group i Command --- identyfikują polecenie do wykonania

Trzeci parametr wywołania `ioctl` --- "..." --- to tak naprawdę jedyny argument dla polecenia zakodowanego przy pomocy parametru `request`.
Skąd zatem notacja "..."?
W dokumentacji możemy przeczytać, że jest to spowodowane tym, że zdefiniowanie tego parametru jako (void*) generowało ostrzeżenia kompilatora.
Argument ten może być różny dla różnych poleceń określonych przez `request`.

---

```c
#define DIOCEJECT	_IOW('d', 112, int)	/* eject removable disk */
#define	_IOW(g,n,t)	_IOC(IOC_IN,	(g), (n), sizeof(t))
```
Umożliwia wyjęcie nośnika ze stacji dyskietek/dysków.

---

```c
#define	KIOCTYPE	_IOR('k', 9, int)	/* get keyboard type */
#define	_IOR(g,n,t)	_IOC(IOC_OUT,	(g), (n), sizeof(t))
```
Zwraca typ klawiatury.

---

```c
#define	SIOCGIFCONF	_IOWR('i', 38, struct ifconf)	/* get ifnet list */
#define	_IOWR(g,n,t)	_IOC(IOC_INOUT,	(g), (n), sizeof(t))
```
Zwraca listę struktur `ifnet`.
Każde urządzenie sieciowe ma przypisaną taką strukturę.

Definicja `ifconf` wygląda następująco.
```c
/*
 * Structure used in SIOCGIFCONF request.
 * Used to retrieve interface configuration
 * for machine (useful for programs which
 * must know all networks accessible).
 */
struct	ifconf {
  	int	ifc_len;		/* size of associated buffer */
  	union {
  		void *	ifcu_buf;
  		struct	ifreq *ifcu_req;
  	} ifc_ifcu;
#define	ifc_buf	ifc_ifcu.ifcu_buf	/* buffer address */
#define	ifc_req	ifc_ifcu.ifcu_req	/* array of structures returned */
};
```

---

```c
#define	_IOC(inout, group, num, len) \
          ((inout) | (((len) & IOCPARM_MASK) << IOCPARM_SHIFT) | \
          ((group) << IOCGROUP_SHIFT) | (num))
```
Powyższe makro przenosi podane argumenty w odpowiadające im miejsca parametru `request` wywołania `ioctl`.

## Zadanie 4-5

**TOCTTOU** (Time Of Check To Time Of Use) to błąd, w którym pomiędzy sprawdzeniem statusu zasobu a jego użyciem (nie są one wykonane atomowo) zakłada się, że jego status się nie zmienił, jednak sprawia to, że program w tym krótkim odstępie czasu staje się podatny na wykorzystanie.

```C=
#include "csapp.h"

bool f_lock(const char *path) 
{
    if (access(path, F_OK) == 0)    //sprawdza czy plik istnieje
        return false;
    
    (void)Open(path, O_CREAT|O_WRONLY, 0700);// otwórz plik o podanej
                                             // ścieżce (stwórz jeśli 
                                            // nie istnieje) do zapisu
    return true;
}

void f_unlock(const char *path) 
{
    Unlink(path);    // usuń nazwę pliku z systemu plików
                    // usuwa plik w przypadku, gdy żaden
                    // inny proces nie miał go otwartego
}
```
Funkcja open wywoływana jest z flagą O_CREAT (która zapewnia nas o utworzeniu pliku o podanej nazwie w przypadku jego braku) z uprawnieniami do odczytu, zapisu i wykonywania (trzeci argument).

W przerwie pomiędzy sprawdzeniem istnienia blokady a ewentualnym jej założeniem inny program mógłby stworzyć plik (a także go otworzyć), który informuje nas o blokadzie i zawrzeć w nim kod (bądź modyfikować go), który mógłby podstępnie ukraść nasze cenne informacje, które możemy do niego zapisać, a także też zapisać w nim kod, który potem nieuważnie moglibyśmy uruchomić.

Można pozbyć się tego błędu korzystając z flagi **O_EXCL**, która wraz z użyciem flagi **O_CREAT** sprawi, że w przypadku, gdy plik istnieje wywołanie open zakończy się niepowodzeniem i zwróci -1.

```C=
#include "csapp.h"

bool f_lock(const char *path) 
{
    int status = Open(path, O_CREAT|O_WRONLY|O_EXCL, 0700);
    
    if(status < 0)
        return false;
    
    return true;
}

void f_unlock(const char *path) 
{
    Unlink(path);
}
```

## Zadanie 4-6

Dowiązanie symboliczne to specjalny typ pliku, który odwoluję się do ścieżki wskazującej lokalizację innego pliku. Dowiązanie symboliczne zawiera napis tekstowy, który jest automatycznie interpretowany, jako ścieżka do innego pliku lub katalogu.


innocent.c
```c=
int main(void) {
  long max_fd = sysconf(_SC_OPEN_MAX);
  int out = Open("/tmp/hacker", O_CREAT | O_APPEND | O_WRONLY, 0666);
  /* TODO: Something is missing here! */ 
  char buf[256];
  char bufname[256];
  char bufresult[1024]; 
  //przeszukanie otwartych deskryptorów plików
  for(int i = 4; i <= max_fd; i++) {
    //zwraca (jako wynik funkcji) flagi deskryptora pliku
    if (fcntl(i, F_GETFD) != -1) {      
        int s = sprintf(buf, "/proc/self/fd/%d",i);
        //odczytuje wartość dowiązania symbolicznego
        int n = readlink(buf, bufname, 256);  
        if (n != -1) {   
           bufname[n] = '\0'; 
           s = sprintf(bufresult, "File descriptor %d is %s\n", i, bufname);
           bufresult[s] = '\0';
           Write(out,bufresult,s);
        
           lseek(i, 0, SEEK_SET);
           char contentbuff[256];
           int readn;           
           while ((readn = read(i,contentbuff,256)) > 0) {            
             contentbuff[readn] = '\0';
             Write(out,contentbuff,readn);
           }
        }       
    }
  }
  Close(out);
  printf("I'm just a normal executable you use on daily basis!\n");
  return 0;
}
```
leaky.c
```
fcntl (fd_2, F_SETFD, FD_CLOEXEC);
```

## Zadanie 4-7

Uzupełniona funkcja *filter_chain(pipe_t in)*:

```=c
static noreturn void filter_chain(pipe_t in) {
  long prime;

  int children_spawned = 0;
  while ( ReadNum( in, &prime ) ) {   // czekamy na kolejną liczbę pierwszą

    printf("%ld\n", prime);
    pipe_t last_pipe = MakePipe();   //tworzymy nowe połączenie którym połączymy
                                     //się z nowym ogniwem łańcucha filtrów
    if (Fork()) { /* parent */
      CloseReadEnd  ( in         );  //zamykamy połączenie z poprzednim ogniwem
      CloseWriteEnd ( last_pipe  );  
      in = last_pipe;                //ustawiamy naszą rurę wchodzącą na nowo
    } else      { /* child  */       //utworzoną
      CloseReadEnd  ( last_pipe  );
      filter(in, last_pipe, prime);  //rura in zostala odziedziczona po ojcu

      CloseReadEnd  ( in         );
      CloseWriteEnd ( last_pipe  );  //sprzatamy po sobie 
      exit ( EXIT_SUCCESS );         //kończymy pracę
    }
    children_spawned++;              //zwiekszamy licznik dzieci
  }

  CloseReadEnd( in );                
  for ( int i = 0; i < children_spawned; i++ )
    Wait( NULL );                    //żniwa 

  exit( EXIT_SUCCESS );
}
```

Działanie programu zobrazowałem przy użyciu diagramów:

Na początku Filter chain jest połączony rurą bezpośrednio z generatorem:

![](https://i.imgur.com/LVXFCKq.png)

Jeżeli jakaś liczba trafi do «filter_chain» to oznacza, że jest liczbą pierwszą. Wtedy wypisujemy ją i tworzymy dla niej nowe ogniwo w łańcuchu filtrowania:

![](https://i.imgur.com/Acdkpzy.png)

stare połączenie (w rodzicu) usuwamy i zastępujemy je nowym połączeniem którym łączymy się z nowym ogniwem łańcucha.

Po paru (n) iteracjach połączenia w programie wyglądają mniej więcej w ten sposób:

![](https://i.imgur.com/ZH00dZs.png)

W momencie w którym generator zakończy swoją pracę, to wszystkie ogniwa wyjdą z funkcji *filter* i zakończą swoją pracę.

Filter chain cały czas śledzi ilość stworzonych dzieci, dzięki czemu może na koniec dokonać żniwa, czekąjąc na koniec pracy wszystkich stworzonych dzieci.

<details><summary>Alternatywne rozwiązanie</summary>
<p>

```c=
static noreturn void filter_chain(pipe_t in) {
  long prime;

  /* TODO: Something is missing here! */
  if (ReadNum(in, &prime)) {
    safe_printf("%ld ", prime);

    pipe_t out = MakePipe();
    filter(in, out, prime);
    CloseReadEnd(in);
    CloseWriteEnd(out);
  
    if (Fork()) { /* parent */
	 CloseReadEnd(out);
	 Wait(NULL);
    }
    else /* child */
	 filter_chain(out);
  }
  else { /* last process */
    CloseReadEnd(in);
    safe_printf("\n");
  }

  exit(EXIT_SUCCESS);
}
```

</p>
</details>

:::spoiler Właściwa liczba podprocesów (Michał Górniak)
```
static noreturn void filter_chain(pipe_t in) {
  long prime;

  /* TODO: Something is missing here! */
  if (!ReadNum(in, &prime)) {
    exit(EXIT_SUCCESS);
  }
  printf("process (%d): %ld\n", getpid(), prime);
  fflush(stdout);

  pipe_t out = MakePipe();
  if (Fork()) {
    CloseReadEnd(out);
    filter(in, out, prime);
    CloseReadEnd(in);
    CloseWriteEnd(out);
    Wait(NULL);
  } else {
    CloseWriteEnd(out);
    filter_chain(out);
  }

  exit(EXIT_SUCCESS);
}
```
:::
