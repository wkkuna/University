
## Zadanie 3-1

- Fork już nie jest taki prosty w swoim działaniu jak się wydaje: specyfikacja POSIX wymienia teraz 25 przypadków specjalnych w jaki sposób stan rodzica jest kopiowany do dziecka: 
  *  blokady plików (Blokowanie plików to mechanizm ograniczający dostęp do pliku między wieloma procesami.
  *   Pozwala tylko jednemu procesowi na dostęp do pliku w określonym czasie,
  *    unikając w ten sposób problemu z aktualizacją pośredniczącą.) ,
  *  czasomierze, 
  *  asynchroniczne operacje I/O, 
  *  śledzenie (strace) itp. Ponadto wiele flag wywołań systemowych kontroluje zachowanie 
  *  forka w odniesieniu do mapowań pamięci, deskryptorów plików i wątków.
- Fork słabo pasuje do zaimplementowanych dla użytkownika abstrakcji systemu operacyjnego, 
    np konieczność korzystania z fflush(), dla opróżnienia buforów wyjściowych przed forkiem.
- Fork jest nietrwały w wielowątkowości. Fork tworzy kopię tylko wątka-rodzica (ale nie procesu),
    to może dać niespójność odziedziczonych danych. Też może wystąpić problem z blokowaniem wspólnej pamięci
    z różnych wątków (deadlock problem). Podręczniki z programowania odradzają używanie forka w procesie wielowątkowym 
    lub polecają wywoływanie exec natychmiast po forku.
- Fork jest niebiezpieczny (względem ochrony danych). Domyślnie utworzone dziecko dziedziczy wszystko po swoim rodzicu, 
    a programista jest odpowiedzialny za usunięcie stanów, których dziecko nie potrzebuje: 
        zamykanie deskryptorów plików/ustawienie flagi close-on-exec, 
        czyszczenie sekretów z pamięci, 
        izolowanie przestrzeni nazw przy użyciu unshare() (umożliwia procesowi (lub wątkowi) oddzielenie części 
        jego kontekstu wykonania, który jest obecnie udostępniany innym procesom (lub wątkom)), 
        itd.
- Fork jest powolny. Wcześniej programy i pamięć były bardzo mniejsze, dostęp do pamięci był szybki w stosunku do wykonywania instrukcji i zapewniał przekonującą abstrakcję. Później jedynie technika kopiowania przy zapisie dawała forku nadwagę, ale teraz i to nie ratuje szybkość wykonania programów.
- Fork źle skaluje się. Operacje zarządzania pamięcią potrzebne do skonfigurowania mapowania kopiowania przy zapisie,
    szkodzą skalowalności, a też sama specyfikacja API fork nie sprawia możliwości przełączania się 
    z innymi operacjami w tym procesie.
- Fork nadużywa pamięć. Konieczność mapowania stron kopiowania przy zapisie dla dużych procesów potrzebuje dużo pamięci,przy tym jeśli dziecko zawoła exec, wszystkie te referencje nie będą wykorzystane. Dla optymizacji w Linuxie jest stosowana technika overcommit virtual memory, co znaczy że odpowiednie mapowanie jest do pamięci wirtualnej. Czyli fork jest wykonywany nawet gdy nie ma za bardzo pamięci. Takie podejście może sprawiać, że kolejny błąd strony (np. zapis do strony rodzica) może nie przydzielić wymaganej pamięci, wywołując „zabójcę braku pamięci” w celu zakończenia procesów i zwolnienia pamięci.

![](https://i.imgur.com/KHJZ34n.png)

- posix_spawn jest dobrą zamianą kombinacji fork+exec. Polega to na tym, że najczęściej nie chcemy kopiować wszystko, z procesa rodzica (np tablicę deskryptorów plików). Funkcja posix_spawn() w nowszych wersjach zaczyna się od wywołania clone () z flagami CLONE_VM i CLONE_VFORK (proces wywołujący i proces potomny działają w tej samej przestrzeni pamięci - nie ma kopiowania. Wykonywanie wywołującego procesu jest zawieszane do momentu zwolnienia przez dziecko zasobów pamięci wirtualnej poprzez wywołanie funkcji exec - nie ma konkurencji wątków za zasoby) i wykonaniu pewnych przygotowań (maski sygnału, domyślne handlery sygnałów, grupa procesów, identyfikatory użytkowników i grup są zmieniane zgodnie z atrybutami attrp) przestrzeni adresowej i wywołania exec.


## Zadanie 3-2

Proces jest **osierocony**, jeśli jego proces-rodzic został zakończony.
**Zadanie drugoplanowe** -- grupa procesów wykonująca się w tle(background). Aby uruchomić proces w tle, należy na koniec polecenia dodać `&`. Aby przenieść proces z  background-u do foreground-u, używamy polecenia `fg`, oraz polecenia `bg`, aby przenieść proces w drugą stronę.
```
ireneusz@irek-laptop:~$ bash
ireneusz@irek-laptop:~$ sleep 1000 &
[1] 4703
ireneusz@irek-laptop:~$ ps -o pid,ppid,cmd
  PID  PPID CMD
 3218  3213 /bin/bash
 4701  3218 bash
 4703  4701 sleep 1000
 4718  4701 ps -o pid,ppid,cmd
```
Rodzicem procesu `sleep` jest uruchomiona przez nas kopia powłoki `bash`.

```
ireneusz@irek-laptop:~$ kill -9 4701
Killed
ireneusz@irek-laptop:~$ ps -o pid,ppid,cmd
  PID  PPID CMD
 3218  3213 /bin/bash
 4703     1 sleep 1000
 4724  3218 ps -o pid,ppid,cmd
```
Po wysłaniu sygnału `SIGKILL` do uruchomionej przez nas powłoki, rodzicem procesu `sleep` został proces `init`, co możemy stwierdzić po `PPID=1`.

```
ireneusz@irek-laptop:~$ ps -o pid,ppid,cmd
  PID  PPID CMD
 3218  3213 /bin/bash
 4867  3218 bash
 4870  4867 sleep 1000
 4872  4867 ps -o pid,ppid,cmd
ireneusz@irek-laptop:~$ kill -SIGHUP 4867
Hangup
ireneusz@irek-laptop:~$ ps -o pid,ppid,cmd
  PID  PPID CMD
 3218  3213 /bin/bash
 4876  3218 ps -o pid,ppid,cmd
```
Sygnał `SIGHUP` wysłany do lidera grupy zabija go i wszystkie procesy z jego grupy, a następnie jest propagowany do wszystkich liderów grup procesów, którzy zostali przez niego utworzeni. Ponieważ `sleep 1000` został utworzony przez basha, `SIGHUP` jest do niego wysyłany.

## Zadanie 3-3

**terminal** - konsola systemy Linux, która zapewnia sposób, w jaki jądro i inne procesy mogą wysyłać dane tekstowe do użytkownika i odbierać dane tekstowe od użytkownika
**zadanie pierwszoplanowe** - jest na bieżąco nadzorowane przez użytkownika, który wykonuje polecenia za pośrednictwem interfejsu grafinczego lub tekstowego.
**wstrzymanie zadania** - wysłanie odpowiedniego sygnału do grupy procesów, w celu zatrzymania ich wykonywania, ale nie zakończenia

```bash=
$ stty -a
speed 38400 baud; rows 55; columns 105; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = <undef>; eol2 = <undef>; swtch = <undef>;
start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V; discard = ^O; min = 1; time = 0;
-parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc -ixany -imaxbel
iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho
-extproc
```

**Znaki, które sterownik terminala zamienia na sygnały z zarządzaniem zadaniami**

- `intr = ^C` - wysyła sygnał przerwania
- `quit = ^\` - wysyła sygnał wyjścia
- `susp = ^Z` - wysyła sygnał stop
- `start = ^Q` - wnowienie wyświetlania
- `stop = ^S` - zatrzymanie wyświetlania

**Znaki, które służą do edycji wiersza**
- `erase = ^?` - kasuje ostatnio wprowadzony znak
- `kill = ^U` - kasuje bieżącą linię
- `werase = ^W` - kasuje ostatnio wprowadzone słowo
- `eof = ^D` - wysyła znak końca linii

**Następnie uruchom «find /» i obserwuj zachowanie programu po naciśnięciu kombinacji klawiszy «CTRL+S» i «CTRL+Q» – jakie sygnały wysyła sterownik terminala do zadania pierwszoplanowego?**

- `start = ^Q` - wnowienie wyświetlania
- `stop = ^S` - zatrzymanie wyświetlania

Wciśnięcie `CTRL+S` powoduje, że proces lub urządzenie wysyłające dane dostają informację od innego procesu/udządzenia, żeby zwiesić transmisję danych. Sygnał `SIGSTOP`.
Wciśnięcie `CTRL+Q` powoduje, wznowienie transmisji między procesami/urządzeniami. Sygnał `SIGCONT`.

**Następnie wstrzymaj zadanie pierwszoplanowe «sleep 1000» i przy pomocy wbudowanego polecenia powłoki «bg» przenieś to zadanie do wykonania w tle.
Jaki sygnał został użyty do wstrzymania zadania?**

W przypadku wstrzymania zadania wciśnięciem `ctrl+z` do procesu zostaje wysłany sygnał `SIGTSTP`. Po przeniesieniu zadania do wykonywania w tle zostaje wysłany sygnał `SIGCONT`.

**Na przykładzie programu «vi» wskaż kiedy program może
być zainteresowany obsługą tego sygnału oraz «SIGCONT».**

> podręcznik strona 379

Będzie to wykorzystywane w przypadku, gdy użytkownik bedzie edytował plik kodu w tym edytorze. Kiedy go zapisze, to będzie chiał go skompilować i uruchomić. Więc zatrzyma działanie `vi` poprzez wciśniecie `CTRL+Z` (wysłanie sygnału `SIGTSTP`). 

`vi` jest programem, który po zatrzymaniu (sygnałem `SIGTSTP`) musi odtworzyć stan terminala (odtworzyć to, co wpisaliśmy do edytora przed zatrzymaniem), przenosząc proces `vi` do pierwszego planu (przez sygnał `SIGCONT`).

```bash=
$ strace -e trace=signal vi
...
kill(0, SIGTSTP
[1]+  Zatrzymano              strace -e trace=signal vi
```

Kiedy bedzie chciał do niego wrócić to może go przywrócić poleceniem `fg`.

```bash=
$ fg
strace -e trace=signal vi text.txt
)                        = 0
--- SIGCONT {si_signo=SIGCONT, si_code=SI_USER, si_pid=16014, si_uid=1000} ---

```

## Zadanie 3-4

**Wbudowane polecenie powłoki** - funkcje, które nie wymagają od powłoki uruchamiania osobnych programów.

```
~$ strace -e trace=signal cat - &
[1] 26894
~$ --- SIGTTIN {si_signo=SIGTTIN, si_code=SI_KERNEL} ---
--- stopped by SIGTTIN ---
```

Polecenie ```cat -``` wypisuje wczytane znaki z terminala. Ponieważ proces nie może przeczytać nic z terminala, gdy działa w tle, to zostaje do niego wysłany sygnał **SIGTTIN**, którego domyślną akcją jest zatrzymanie procesu.

Przed:
:::spoiler
```
~$ cat /etc/shells &
[1] 27241
~$ # /etc/shells: valid login shells
/bin/sh
/bin/bash
/usr/bin/bash
/bin/rbash
/usr/bin/rbash
/bin/dash
/usr/bin/dash
/usr/bin/tmux

```
:::
Po:
:::spoiler 
```
~$ stty tostop
~$ cat /etc/shells &
[1] 27321
~$ 
```
:::

Po włączeniu flagi ***tostop***, do powyższego procesu wysyłany zostaje sygnał ***SIGTTOU***, który działa podobnie do SIGTTIN z tą różnicą, że domyślnie zatrzymuje procesy działające w tle próbujące wypisać coś na terminal. 

SIGCHLD wysyłany jest do procesu-rodzica w przypadku zakończenia bądź zatrzymania procesu.

Aby rozróżnić wstrzymanie/kontynuowanie od zakończenia procesu potomnego w waitpid() wystarczy wywołać ją z opcją:
- **WEXITED**(jeśli chcemy dowiedzieć się czy dziecko zakończyło działanie - ustawiona jest domyślnie), 
- **WSTOPPED** (dla rozpoznania zatrzymania)
- **WCONTINUED** (gdy proces został wznowiony sygnałem SIGCONT).

Funkcja biblioteki standardowej do wybrania grupy pierwszoplanowej: [*tcsetpgrp()*](https://linux.die.net/man/3/tcsetpgrp).


## Zadanie 3-5

Procedury `setjmp`, `longjmp` implementują funkcjonalność tzw. **nielokalnych skoków**. `setjmp` w momencie pierwszego wywołania zapisuje kontekst działania programu (niektóre rejestry), które następnie podane do procedury `longjmp` zostają przywracane powodując zmianę kontroli przepływu na miejsce, w którym `setjmp` zostało oryginalnie wywołane.

Definicja struktury `jmpbuf` służącej do zapisywania kontekstu:
```c=
typedef struct {
  long rbx;
  long rbp;
  long r12;
  long r13;
  long r14;
  long r15;
  void *rsp;
  void *rip;
} Jmpbuf[1];

int Setjmp(Jmpbuf env);
noreturn void Longjmp(Jmpbuf env, int val);
```
Zmienne używane przez `setjmp` i `longjmp`, a tak naprawdę offsety do kolejnych pól w strukturze `jmpbuf`:
```assembler=
_JB_RBX = 0
_JB_RBP = 1
_JB_R12 = 2
_JB_R13 = 3
_JB_R14 = 4
_JB_R15 = 5
_JB_RSP = 6
_JB_RIP = 7
```
Procedura `setjmp`:
```assembler=
        .text

        .globl Setjmp
        .type Setjmp,@function
Setjmp:
	movq    (%rsp),%r11  ; zapisanie adresu powrotu (najpierw do %r11)
	movq    %rbx,(_JB_RBX * 8)(%rdi)
	movq    %rbp,(_JB_RBP * 8)(%rdi)
	movq    %r12,(_JB_R12 * 8)(%rdi)
	movq    %r13,(_JB_R13 * 8)(%rdi)
	movq    %r14,(_JB_R14 * 8)(%rdi)
	movq    %r15,(_JB_R15 * 8)(%rdi)
	movq    %rsp,(_JB_RSP * 8)(%rdi)
	movq    %r11,(_JB_RIP * 8)(%rdi)
	xorl	%eax,%eax
	ret
        .size Setjmp, . - Setjmp
```
Widzimy, że procedura `setjmp` zapisuje kolejne rejestry do odpowiednich pól struktury. Jedyną wątpliwość może budzić instrucja `movq    (%rsp),%r11` z linii 6 - przypomnijmy, że w momencie wejścia do funkcji wywołaniem `call` (co zrobiliśmy wchodząc do `setjmp`), na stos zostaje odłożony adres, do którego mamy wrócić.

Jednocześnie `setjmp` nie zapisuje wszystkich rejestrów procesora, ponieważ nie musi - zapisuje tylko te `callee-saved`, ponieważ reszta - `caller-saved` będą zapisane w momencie wywołania procedury `setjmp` i przywrócone po wyjściu z niej.

Procedura `longjmp`:
```assembler=
        .globl Longjmp
        .type Longjmp,@function
Longjmp:
	movq    (_JB_RBX * 8)(%rdi),%rbx
	movq    (_JB_RBP * 8)(%rdi),%rbp
	movq    (_JB_R12 * 8)(%rdi),%r12
	movq    (_JB_R13 * 8)(%rdi),%r13
	movq    (_JB_R14 * 8)(%rdi),%r14
	movq    (_JB_R15 * 8)(%rdi),%r15
	movq    (_JB_RSP * 8)(%rdi),%rsp
	movq    (_JB_RIP * 8)(%rdi),%r11
	movl	%esi,%eax
	testl	%eax,%eax
	jnz	1f
	incl	%eax
1:	movq	%r11,(%rsp)
	ret
        .size Longjmp, . - Longjmp

```
Operacja `movq    (_JB_RIP * 8)(%rdi),%r11` przywraca zapisany wcześniej *instruction pointer* najpierw do rejestru `%r11` - dlaczego nie do `%rip`? Ponieważ została nam do wykonania jeszcze część ciała procedury `longjmp`, a po zmianie rejestru `%rip`, od razu skoczymy do zapisanego wcześniej miejsca.

## Zadanie 3-6

**Nielokale skoki** zapewniają wykonanie tego, co w efekcie jest przejściem od jednej funkcji do drugiej. Nie można tego zrobić za pomocą goto i etykiety, ponieważ etykiety mają tylko zakres funkcji. 
Jednak setjmp i funkcja longjmp zapewniają alternatywę, znaną jako nielokalne goto lub nielokalny skok.

Jedyną różnicą między sigsetjmp i siglongjmp funkcjami a funkcjami setjmp i longjmp jest to, że sigsetjmp ma dodatkowy argument. Jeśli savemask ma wartość niezerową, sigsetjmp zapisuje również bieżącą maskę sygnału procesu w env. Po wywołaniu siglongjmp, jeśli argument env został zachowany przez wywołanie sigsetjmp z niezerową maską zapisu, to siglongjmp przywraca zapisaną maskę sygnału.

```c=

static void signal_handler(int signo) {
  siglongjmp(env, signo);
}


static int readnum(int *num_p) {
  char line[MAXLINE];
  int n;

  alarm(1);
  if ((n = sigsetjmp(env,1)) == 0) {
    int l = Read(STDIN_FILENO, line, MAXLINE);
    line[l] = 0;
    *num_p = atoi(line);
    return 0;
  } 
  return n;
}
```


> [name=Michał Myczkowski] Moje rozwiązanie unikające błędu z obsługiwaniem sygnału alarmowego w wypadku, gdy wpiszemy rozwiazanie w odpowiednim czasie
> fragment man ALARM(2)
>" If seconds is zero, any pending alarm is canceled."
:::spoiler
```c=
/* alternatywna wersja */
static int readnum(int *num_p) {
  char line[MAXLINE];
  int sig = sigsetjmp(env, 1);
  if(sig)
    return sig;
  alarm(1);
  int n = Read(STDIN_FILENO, line, MAXLINE);
  line[n] = 0;
  alarm(0);
  *num_p = atoi(line);
  return sig;
}
```

:::


## Zadanie 3-7

**zmiana kontekstu** --- ([mimuw](http://smurf.mimuw.edu.pl/node/879)) polega na zachowaniu stanu przetwarzania procesu oddającego procesor (zachowaniu kontekstu) i załadowaniu stanu przetwarzania innego procesu (odtworzenie kontekstu).
**wielozadaniowość kooperacyjna** (ang. *cooperative multitasking*) --- wielozadaniowość, w której system operacyjny nie wymusza na procesach zmian kontekstu. Zamiast tego procesy dobrowolnie oddają procesor, kiedy np. są bezczynne lub zablokowane w oczekiwaniu na sygnał.

###### Uzupełniony fragment programu
```c=
/*
 * Switch between subsequent coroutines.
 *
 * Dead coroutines, i.e. ones that returned EOF, get removed from the run queue.
 * Feed next coroutine (value returned from coro_yield) with the result from
 * previous one (parameter passed to coro_yield).
 * Return to dispatcher if there're no more coroutines to run.
 */
static noreturn void coro_switch(int v) {
  coro_t *curr = running;
  /* TODO: Use description above to implement the body. */
  if (v == NOTHING) //  we start from the first coroutine
  {
    running = TAILQ_FIRST(&runqueue);
    Longjmp(running->co_ctx, v);
  }
  running = TAILQ_NEXT(curr, co_link); // next coroutine
  if (v == EOF) // EOF means we're ending program
  {
    TAILQ_REMOVE(&runqueue, curr, co_link);
    if (TAILQ_EMPTY(&runqueue)) // last coroutine returned
      Longjmp(dispatcher, v);
  }
  Longjmp(running->co_ctx, v); // start executing next coroutine
}
```
