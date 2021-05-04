# Ćwiczenia 2, grupa KBa, 15 października 2020

## Zadanie 2-1

### Definicje

***relacja rodzic-dziecko ---*** 
:::spoiler 
podczas użycia $fork()$ tworzona zostaje kopia procesu, która jest nazywana dzieckiem danego procesu, a ten jest jej rodzicem. Proces wywołuje wywołanie systemowe $fork ()$, które system operacyjny udostępnia jako sposób tworzenia nowego procesu. 
Tworzony proces jest (prawie) dokładną kopią procesu wywołującego. Oznacza to, że dla systemu operacyjnego wygląda teraz na to, że są uruchomione dwie kopie programu `p1` i obie mają powrócić z wywołania systemowego $fork ()$. Nowo utworzony proces (nazywany dzieckiem, w przeciwieństwie do rodzica tworzącego) nie zaczyna działać w `main()`.
:::

***identyfikator procesu ---*** *pid* --- 
:::spoiler
PID jest używany do *identyfikacji procesu* np. aby zamknąć proces podajemy jego PID, a nie nazwę, ponieważ te mogą się powtarzać (menager zadań nieraz wskazuje np. kilka procesów `chrome`)
:::

***identyfikator grupy procesów ---*** *pgid* --- 
:::spoiler
"Process Group ID"; identyfikator grupy procesów, do której ten proces należy; na początku proces potomny należy do tej samej grupy co proces macierzysty (może jednak założyć własną grupę procesów i stać się jej przywódcą, czyli może mieć PID=PGID). 
przykład zastosowania grup procesów: 
- można wysyłać sygnały do całych grup procesów a nie tylko do pojedynczych procesów. 

([strona](https://mhanckow.students.wmi.amu.edu.pl/sop121/sop121b.htm))
:::

***identyfikator rodzica procesu ---*** *ppid* ---  
:::spoiler
"Parent Process ID"; identyfikator "rodzica" procesu; w Unix-ie proces może się "rozdwoić", nowy proces nazywamy procesem potomnym, a stary proces nazywamy procesem macierzystym; proces potomny jest początkowo dokładną kopią procesu macierzystego; proces potomny może zacząć wykonywać inny program niż ten wykonywany przez proces macierzysty; jeśli z pewnej powłoki uruchamiamy program to program ten wykonuje się w procesie potomnym a powłoka jest jego procesem macierzystym; ([strona](https://mhanckow.students.wmi.amu.edu.pl/sop121/sop121b.htm))
:::

***właściciel procesu ---*** *user* --- 
:::spoiler
użytkownik, który uruchomił proces i nim zarządza 
:::

***wątki jądra ---*** *kernel threads* --- 
:::spoiler
działają asynchronicznie w przestrzeni jądra (podobnie jak zwykłe wątki w przestrzeni użytkownika), niezwiązane z żadnym procesem użytkownika. Ich nazwy przedstawione są na liście procesów w nawiasach kwadratowych. Rodzicem wszystkich wątków jądra jest **kthreadd** - PID = 2 ([strona](https://students.mimuw.edu.pl/ZSO/Wyklady/00_stud/watki_jadra.pdf))
:::

***hierarchia procesów ---*** procesy tworzą hierarchię:
:::spoiler
- *init* jest procesem głównym
- proces tworzący inne procesy staje się dla nich rodzicem
- procesy wykonują się w separacji od siebie i mogą kończyć się w dowolnej kolejności
- procesy sieroty (ang. orphan) - procesy, których proces macierzysty się zakończył
    - ich procesem macierzystym staje się init
- procesy zombie - proces się zakończył, ale nie został oczyszczony (widnieje w tablicy )
    - nie zajmuje procesora ani innych zasobów (w zasadzie tylko miejsce na deskryptor procesu(ang. process descriptor) --- rekord w którym system operacyjny utrzymuje wszystkie informacje niezbędne do zarządzania procesem. )
    - występuje w tablicy procesów do momentu wywołania *wait()*
:::

### Polecenie

```
ps -eo user,pid,ppid,pgid,tid,pri,stat,wchan,cmd
```

#### man ps:
:::spoiler
```
       -e     Select all processes.  Identical to -A.

       -o format
              User-defined format.  format is a single argument in the form
              of a blank-separated or comma-separated list, which offers a
              way to specify individual output columns.  The recognized
              keywords are described in the STANDARD FORMAT SPECIFIERS
              section below.  Headers may be renamed (ps -o pid,
              ruser=RealUser -o comm=Command) as desired.  If all column
              headers are empty (ps -o pid= -o comm=) then the header line
              will not be output.  ...
			  
```
```
       user        USER         see euser.  (alias euser, uname).
	   

       euser       EUSER        effective user name.  This will be the textual
                                user ID, if it can be obtained and the field
                                width permits, or a decimal representation
                                otherwise.  The n option can be used to force
                                the decimal representation.  (alias uname,
                                user).
							    
       pid         PID       	a number representing the process ID (alias
								tgid).

       ppid        PPID      	parent process ID.
							 
 
       pgid        PGID      	process group ID or, equivalently, the process
                               ID of the process group leader.  (alias pgrp).
							 
	   

       tid         TID       	the unique number representing a dispatchable
                               entity (alias lwp, spid).  This value may also
                               appear as: a process ID (pid); a process group
                               ID (pgrp); a session ID for the session leader
                               (sid); a thread group ID for the thread group
                               leader (tgid); and a tty process group ID for
                               the process group leader (tpgid).
										
										
       pri         PRI       	priority of the process.  Higher number means
                               lower priority.
							 

       stat        STAT      	multi-character process state.  See section
                                PROCESS STATE CODES for the different values
                                meaning.  See also s and state if you just want
                                the first character displayed.
							 

       wchan       WCHAN           name of the kernel function in which the
                                    process is sleeping, a "-" if the process is
                                    running, or a "*" if the process is
                                    multi-threaded and ps is not displaying
                                    threads.
							 

       cmd         CMD           see args.  (alias args, command).
	   

       args        COMMAND       command with all its arguments as a string.
                                 Modifications to the arguments may be shown.
                                 The output in this column may contain spaces.
                                 A process marked <defunct> is partly dead,
                                 waiting to be fully destroyed by its parent.
                                 Sometimes the process args will be unavailable;
                                 when this happens, ps will instead print the
                             executable name in brackets.  (alias cmd,
                             command).  See also the comm format keyword,
                             the -f option, and the c option.
                             When specified last, this column will extend to
                             the edge of the display.  If ps can not
                             determine display width, as when output is
                             redirected (piped) into a file or another
                             command, the output width is undefined (it may
                             be 80, unlimited, determined by the TERM
                             variable, and so on).  The COLUMNS environment
                             variable or --cols option may be used to
                             exactly determine the width in this case.  The
                             w or -w option may be also be used to adjust
                             width.
```
:::

### Kto jest rodzicem procesu init?

Rodzicem procesu init jest $kernel$, z $PID = 0$ (tutaj PPID, ponieważ to PID rodzica procesu init).
```
USER         PID    PPID    PGID     TID PRI STAT WCHAN  CMD
root           1       0       1       1  19 Ss   -      /sbin/init splash
```

### Wskaż, które z wyświetlonych zadań są wątkami jądra

Wątki jądra *(kernel threads)* są dziećmi procesu $PID=2$:
```
USER         PID    PPID    PGID     TID PRI STAT WCHAN  CMD
root           2       0       0       2  19 S    -      [kthreadd]
```

a także:

>Jeśli nie można znaleźć argumentów (zwykle dlatego, że nie zostały one ustawione, jak ma to miejsce w przypadku procesów systemowych i / lub **wątków jądra**), nazwa polecenia jest drukowana w nawiasach kwadratowych.
><cite>~ FreeBSD ps(1) man</cite>

> Czasami argumenty procesu będą niedostępne; gdy tak się stanie, ps zamiast tego wypisze nazwę pliku wykonywalnego w nawiasach.
> <cite>~ linux ps(1) man</cite>

Zatem bardzo prawdopodobne, że wątki procesora oznaczone są z $PPID=2$ i z nazwami w nawiasach kwadratowych.

### Jakie jest znaczenie poszczególnych znaków w kolumnie STAT?

:::spoiler
```
PROCESS STATE CODES         

   D    uninterruptible sleep (usually IO)
   I    Idle kernel thread 
   R    running or runnable (on run queue)
   S    interruptible sleep (waiting for an event to complete)
   T    stopped by job control signal
   t    stopped by debugger during the tracing
   W    paging (not valid since the 2.6.xx kernel)
   X    dead (should never be seen)
   Z    defunct ("zombie") process, terminated but not reaped by
        its parent


   <    high-priority (not nice to other users)
   N    low-priority (nice to other users)
   L    has pages locked into memory (for real-time and custom
        IO)
   s    is a session leader
   l    is multi-threaded (using CLONE_THREAD, like NPTL
        pthreads do)
   +    is in the foreground process group
```
:::

### Polecenie

```
pstree
```

### Które z zadań są wątkami?

#### man pstree:

:::spoiler
```
       pstree spokazuje uruchomione procesy jako drzewo. 
       Drzewo jest zakorzenione pid lub init, jeśli pominięto pid. 
       Jeśli określono nazwę użytkownika, 
       wyświetlane są wszystkie drzewa procesów 
       zakorzenione w procesach należących do tego użytkownika.

       pstree wizualnie łączy identyczne gałęzie, 
       umieszczając je w kwadratowe nawiasy 
       i poprzedzając je liczbą powtórzeń, np.

           init-+-getty
                |-getty
                |-getty
                `-getty

       staje się

           init---4*[getty]

       Wątki potomne procesu znajdują się pod procesem nadrzędnym 
       i są pokazane z nazwą procesu w nawiasach klamrowych, np.

           icecast2---13*[{icecast2}]
```

:::

## Zadanie 2-2

$$ - pid powłoki na której jesteśmy
UID - id użytkownika, mówi o tym jakie przywileje wobec pliku ma user (r w x)
GID - identyfikator grupy w sensie przywilejów (co może robić proces)
/proc - to katalog będący tekstowym mapowaniem danych o procesach działających w systemie na system plików. Dzięki temu możemy odczytywać informacje o procesie (np. lista otwartych plików, parametry startowe) jak i je     modyfikować (np. env). Zastosowanie systemu plików zwalnia nas z potrzeby implementowania syscalli za to odpowiedzialnych.
Oprócz informacji o poszczególnych procesach /proc udostępnia również pliki zawierające przydatne informacje o systemie. Na przykład:
* /proc/cpuinfo - informacje o procesorze
* /proc/uptime - czas od uruchomienia systemu
* /proc/modules - lista załadowanych modułów jądra

/proc/status
* Uid, Gid: Real, effective, saved set, and filesystem UIDs (GIDs).
* Groups - dodatkowe grupy przypisane do procesu
* VmPeak - największe zużycie pamięci wirtualnej
* VmSize - rozmiar pamięci wirtualnej
* VmRSS - rozmiar obecnie używanej pamięci fizycznej
* Threads - ilość wątków należących do procesu
* voluntary_ctxt_switches, nonvoluntary_ctxt_switches - przymusowe i nieprzymusowe przełączenia kontekstu ([What exactly are “Voluntary context switches”?](https://unix.stackexchange.com/a/442991))

nieprzymusowe - zdarzają się, kiedy proces nie potrzebuje w danym momencie zasobów procesora, np. czekanie na zdarzenie, io
przymusowe - zachodzą gdy system uznaje, że w danym przedziale czasowym proces wykorzystał wystarczająco dużo zasobów procesora i oddaje możliwość działania innemu procesowi

## Zadanie 2-3

![](https://i.imgur.com/9uW6hVq.png)

**Segmenty programu:** 
* segment tekstu (ELF)
* segment danych (zainicjowane zmienne statyczne)
* bss segment (zmienne statyczne które nie został przypisany)

**Pamięć anonimowa**
Pamięć anonimowa to mapowanie pamięci bez żadnego pliku ani urządzenia, na którym jest utworzona. W ten sposób programy przydzielają pamięć z systemu operacyjnego do wykorzystania przez takie rzeczy, jak stos i sterta.

**Pliki odwzorowane w pamięć** to segmenty pamięci, do których przypisano pewną część pliku lub zasobu podobnego do pliku. Ten zasób to zazwyczaj plik fizycznie obecny na dysku, ale może to być również urządzenie, obiekt pamięci współużytkowanej lub inny zasób, do którego system operacyjny może się odwoływać za pośrednictwem deskryptora pliku.

<details>
  <summary>pmap</summary>
  

```bash=
17189:   xterm
000055962eef8000    604K r-x-- xterm
000055962f18f000     28K r---- xterm
000055962f196000     32K rw--- xterm
000055962f19e000     40K rw---   [ anon ]
000055962f788000   3504K rw---   [ anon ]
00007f0cf0f8a000     44K r-x-- libnss_files-2.27.so
00007f0cf0f95000   2044K ----- libnss_files-2.27.so
00007f0cf1194000      4K r---- libnss_files-2.27.so
00007f0cf1195000      4K rw--- libnss_files-2.27.so
00007f0cf119c000     92K r-x-- libnsl-2.27.so
00007f0cf587b000      4K rw---   [ anon ]
00007f0cf587c000     96K r-x-- libXmu.so.6.2.0
00007f0cf5894000   2044K ----- libXmu.so.6.2.0
00007f0cf5cfd000      4K r---- libXaw7.so.7.0.0
00007f0cf5cfe000     40K rw--- libXaw7.so.7.0.0
00007f0cf5d08000      4K rw---   [ anon ]
00007f0cf5d09000    248K r-x-- libfontconfig.so.1.10.1
00007f0cf5d47000   2048K ----- libfontconfig.so.1.10.1
00007f0cf5f47000      8K r---- libfontconfig.so.1.10.1
00007f0cf5f49000     20K rw--- libfontconfig.so.1.10.1
00007f0cf6169000   2044K ----- libgtk3-nocsd.so.0
00007f0cf6368000      4K r---- libgtk3-nocsd.so.0
00007f0cf6369000      4K rw--- libgtk3-nocsd.so.0
00007f0cf636a000    156K r-x-- ld-2.27.so
00007f0cf6562000     56K rw---   [ anon ]
00007f0cf6591000      4K r---- ld-2.27.so
00007f0cf6592000      4K rw--- ld-2.27.so
00007f0cf6593000      4K rw---   [ anon ]
00007ffe6760e000    132K rw---   [ stack ]
00007ffe6765c000     12K r----   [ anon ]
00007ffe6765f000      8K r-x--   [ anon ]
ffffffffff600000      4K r-x--   [ anon ]
 total            90476K

```
</details>

## Zadanie 2-4

```
COMMAND   PID USER   FD      TYPE             DEVICE  SIZE/OFF     NODE NAME
firefox 11785 ania  cwd       DIR                8,6     12288 12454324 /home/ania
firefox 11785 ania  rtd       DIR                8,6      4096        2 /
firefox 11785 ania  txt       REG                8,6    227648  9967169 /usr/lib/firefox/firefox
firefox 11785 ania  DEL       REG               0,22                 80 /dev/shm/org.mozilla.ipc.11840.101
firefox 11785 ania  DEL       REG               0,22                 59 /dev/shm/org.mozilla.ipc.11840.95
```

Kolumny:
NODE - numer Inode

Typ zasobu można rozpoznać po TYPE:
REG - zwykły plik
DIR - katalog
FIFO - potok
sock/unix/IPv4 - gniazdo

Urządzenie można zidentyfikować po nazwie zaczynającej się od /dev.
Wyjście `diff -u before after | grep TCP`:
:::spoiler

```
-firefox 11785 ania   99u     IPv4             141068       0t0      TCP asus:45362->104.26.0.94:https (ESTABLISHED)
+firefox 11785 ania   99u     IPv4             141068       0t0      TCP 192.168.42.130:45362->104.26.0.94:https (ESTABLISHED)
-firefox 11785 ania  112u     IPv4             141604       0t0      TCP asus:54266->server-13-224-102-41.zrh50.r.cloudfront.net:https (ESTABLISHED)
-firefox 11785 ania  113u     IPv4             141605       0t0      TCP asus:38182->151.101.112.193:https (ESTABLISHED)
-firefox 11785 ania  114u     IPv4             144514       0t0      TCP asus:44450->ss64.com:https (ESTABLISHED)
+firefox 11785 ania  112u     IPv4             141604       0t0      TCP 192.168.42.130:54266->server-13-224-102-41.zrh50.r.cloudfront.net:https (ESTABLISHED)
+firefox 11785 ania  113u     IPv4             141605       0t0      TCP 192.168.42.130:38182->151.101.112.193:https (ESTABLISHED)
+firefox 11785 ania  114u     IPv4             144514       0t0      TCP 192.168.42.130:44450->ss64.com:https (ESTABLISHED)
+firefox 11785 ania  118u     IPv4             149169       0t0      TCP 192.168.42.130:41590->edge-star-mini-shv-01-waw1.facebook.com:https (ESTABLISHED)
-firefox 11785 ania  125u     IPv4             137895       0t0      TCP asus:41800->text-lb.esams.wikimedia.org:https (ESTABLISHED)
-firefox 11785 ania  127u     IPv4             136637       0t0      TCP asus:48436->ec2-52-193-206-70.ap-northeast-1.compute.amazonaws.com:https (ESTABLISHED)
+firefox 11785 ania  125u     IPv4             149236       0t0      TCP 192.168.42.130:49998->waw02s08-in-f10.1e100.net:https (ESTABLISHED)
+firefox 11785 ania  127u     IPv4             136637       0t0      TCP 192.168.42.130:48436->ec2-52-193-206-70.ap-northeast-1.compute.amazonaws.com:https (ESTABLISHED)
-firefox 11785 ania  145u     IPv4             136608       0t0      TCP asus:33312->ec2-34-213-90-136.us-west-2.compute.amazonaws.com:https (ESTABLISHED)
+firefox 11785 ania  145u     IPv4             136608       0t0      TCP 192.168.42.130:33312->ec2-34-213-90-136.us-west-2.compute.amazonaws.com:https (ESTABLISHED)
+firefox 11785 ania  155u     IPv4             150005       0t0      TCP 192.168.42.130:46206->waw02s18-in-f3.1e100.net:http (ESTABLISHED)
-firefox 11785 ania  168u     IPv4             140555       0t0      TCP asus:41368->ec2-18-179-225-220.ap-northeast-1.compute.amazonaws.com:https (ESTABLISHED)
+firefox 11785 ania  165u     IPv4             149248       0t0      TCP 192.168.42.130:44234->fna-fbcdn-shv-01-fktw4.fbcdn.net:https (ESTABLISHED)
+firefox 11785 ania  167u     IPv4             149251       0t0      TCP 192.168.42.130:38324->93.184.220.29:http (ESTABLISHED)
+firefox 11785 ania  168u     IPv4             140555       0t0      TCP 192.168.42.130:41368->ec2-18-179-225-220.ap-northeast-1.compute.amazonaws.com:https (ESTABLISHED)
+firefox 11785 ania  169u     IPv4             145107       0t0      TCP 192.168.42.130:42462->edge-star-shv-01-waw1.facebook.com:https (ESTABLISHED)
+firefox 11785 ania  177u     IPv4             149252       0t0      TCP 192.168.42.130:38326->93.184.220.29:http (ESTABLISHED)
+firefox 11785 ania  181u     IPv4             145105       0t0      TCP 192.168.42.130:39696->fna-fbcdn-shv-01-fktw1.fbcdn.net:https (ESTABLISHED)
+firefox 11785 ania  183u     IPv4             149253       0t0      TCP 192.168.42.130:38328->93.184.220.29:http (ESTABLISHED)
+firefox 11785 ania  185u     IPv4             145108       0t0      TCP 192.168.42.130:42464->edge-star-shv-01-waw1.facebook.com:https (ESTABLISHED)
+firefox 11785 ania  203u     IPv4             149231       0t0      TCP 192.168.42.130:52224->xx-fbcdn-shv-01-waw1.fbcdn.net:https (ESTABLISHED)

```
:::

## Zadanie 2-5

:::warning
Autor: Radosław Zazulczak
:::

**czas wykonania** - czas spędzony przez procesor na wykonanie danego programu

**ograniczenie na czas wykonania** - limit czasu dany programowi na działanie.

```text=
$ time

real	0m0,000s
user	0m0,000s
sys	0m0,000s
```

a) Czemu suma czasów `user` i `sys` nie jest równa `real`?

**Real** - czas od początku do końca wykonywania. Czas, kiedy proces jest wykonywany oraz kiedy jest zablokowany.

**User** - czas jaki spędza procesor w trybie użytkownika w procesie. Gdy proces jest zablokowany, czas nie jest wliczany do niego.

**Sys** - czas jaki spędza procesor w trybie jądra, czyli wywołując wywołania systemowe. Nie jest wliczany czas spędzany w trybie użytkownika oraz podczas innych procesów

Ogólnie dlatego, że w `real` liczy sie czas spędzany w innych procesach.

b) Czemu  suma  czasów `user` i `sys` może być większa od `real`?

Taka sytuacja jest możliwa wtedy, gdy proces jest wykonywany przez kilka procesorów (rdzeni) współbieżnie. Wtedy czasy poszczególnych rdzeni są sumowane, przez co jest on większy od rzeczywistego.

Zmieniam limit `cpu time` na 1 sekundę:

```text=
$ ulimit -a
core file size          (blocks, -c) 0
data seg size           (kbytes, -d) unlimited
scheduling priority             (-e) 0
file size               (blocks, -f) unlimited
pending signals                 (-i) 30814
max locked memory       (kbytes, -l) 16384
max memory size         (kbytes, -m) unlimited
open files                      (-n) 1024
pipe size            (512 bytes, -p) 8
POSIX message queues     (bytes, -q) 819200
real-time priority              (-r) 0
stack size              (kbytes, -s) 8192
cpu time               (seconds, -t) unlimited
max user processes              (-u) 30814
virtual memory          (kbytes, -v) unlimited
file locks                      (-x) unlimited
```

```text=
$ ulimit -t 1
$ ulimit -a
core file size          (blocks, -c) 0
data seg size           (kbytes, -d) unlimited
scheduling priority             (-e) 0
file size               (blocks, -f) unlimited
pending signals                 (-i) 30814
max locked memory       (kbytes, -l) 16384
max memory size         (kbytes, -m) unlimited
open files                      (-n) 1024
pipe size            (512 bytes, -p) 8
POSIX message queues     (bytes, -q) 819200
real-time priority              (-r) 0
stack size              (kbytes, -s) 8192
cpu time               (seconds, -t) 1
max user processes              (-u) 30814
virtual memory          (kbytes, -v) unlimited
file locks                      (-x) unlimited

```

Jaki sygnał wysłano do procesu (wykonanie `find /usr`)?

SIGKILL (Unicestwienie)


## Zadanie 2-6

**kopiowanie przez referencję** -- w chwili wywołania _forka_, jądro nie kopiuje całej zawartości rodzica, tylko obszary pamięci są współdzielone, jądro zastrzega, że są one tylko do odczytu. Dopiero w chwili, gdy któryś z procesów próbuje zmodyfikować obszar pamięci, odpowiednia strona jest kopiowana.

**pozycja kursora** -- wskaźnik, wskazujący na obecną pozycję na której jesteśmy w pliku (np. gdzie zakończyliśmy wczytywanie do tej pory)

:::spoiler Kod rozwiązania
```
#include "csapp.h"

static char buf[256];

#define LINE1 49
#define LINE2 33
#define LINE3 78

static void do_read(int fd) {
  /* TODO: Spawn a child. Read from the file descriptor in both parent and
   * child. Check how file cursor value has changed in both processes. */
  
  int id = fork();
  if(id == 0){
    //child
    if(read(fd, buf, 5) == -1)	
      printf("Child with pid = %d, read error\n", getpid());
    else
	  printf("Child with pid = %d, cursor = %ld reads %s\n", getpid(), lseek(fd, 0, SEEK_CUR), buf);
  }
  else{
  	//parent
    if(read(fd, buf, 5) == -1) {
      printf("Parent with pid = %d, read error\n", getpid());
    }
    else {
      printf("Parent with pid = %d, cursor = %ld reads %s\n", getpid(), lseek(fd, 0, SEEK_CUR), buf);  	
    }
  }
  
  exit(0);
}

static void do_close(int fd) {
  /* TODO: In the child close file descriptor, in the parent wait for child to
   * die and check if the file descriptor is still accessible. */
  
  int id = fork();
  if(id == 0){
  	//child
  	if(close(fd) == -1) {
  	  printf("Child with pid = %d, close error\n", getpid());
  	}
  	else {
  	  printf("Child with pid = %d, close successful\n", getpid());
  	}
  }
  else{
  	//parent
  	wait(NULL);
    if(read(fd, buf, 5) == -1) {
      printf("Parent with pid = %d, read error\n", getpid());
    }
    else {
      printf("Parent with pid = %d, cursor = %ld reads %s\n", getpid(), lseek(fd, 0, SEEK_CUR), buf); 
    }
  }
  
  exit(0);
}

int main(int argc, char **argv) {
  if (argc != 2)
    app_error("Usage: %s [read|close]", argv[0]);

  int fd = Open("test.txt", O_RDONLY, 0);
  
  if (!strcmp(argv[1], "read"))
    do_read(fd);
  if (!strcmp(argv[1], "close"))
    do_close(fd);
  app_error("Unknown variant '%s'", argv[1]);
}
```
:::

:::spoiler Wyjście dla _read_
```
Parent with pid = 12681, cursor = 5 reads Write
Child with pid = 12682, cursor = 10 reads  prog
```
:::

:::spoiler Wyjście dla _close_
```
Child with pid = 12842, close successful
Parent with pid = 12841, cursor = 5 reads Write
```
:::

Z powyższego wyjścia można zauważyć, że przy wczytaniu do dziecka, kursor przesuwa się też w rodzicu, co dowodzi, że oba procesy współdzielą plik między sobą przez referencję. Tak samo, można zauważyć, że wywołanie funkcji $\texttt{close}$ w dziecku, $\textbf{nie}$ zamyka danego pliku w rodzicu.

## Zadanie 2-7

**fork bomba** - sytuacja, w której proces nieustannie się replikuje, co powoduje wyczerpanie zasobów

Przykład dla `n=3` (w każdym momencie `main` może zakończyć działanie, gdy znajdzie konflikt ustawienia hetmanów, ale nie zostało zaznaczone to na diagramie dla większej czytelności):
![](https://i.imgur.com/WLYPcLN.png)

 
