## Zadanie 5-1

Punkt montażowy (mount point) - katalog w aktualnym systemie plików z którego dostępny jest korzeń innego systemu plików (katalog z którego zaczynają się ścieżki bezwzględne).
Fragment wyniku polecenia ```mount```:
```
sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
udev on /dev type devtmpfs (rw,nosuid,relatime,size=6072108k,nr_inodes=1518027,mode=755)
devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000)
tmpfs on /run type tmpfs (rw,nosuid,noexec,relatime,size=1218948k,mode=755)
/dev/sda6 on / type ext4 (rw,relatime,errors=remount-ro,data=ordered)
securityfs on /sys/kernel/security type securityfs (rw,nosuid,nodev,noexec,relatime)
tmpfs on /dev/shm type tmpfs (rw,nosuid,nodev)
tmpfs on /run/lock type tmpfs (rw,nosuid,nodev,noexec,relatime,size=5120k)
tmpfs on /sys/fs/cgroup type tmpfs (rw,mode=755)
cgroup on /sys/fs/cgroup/systemd type cgroup (rw,nosuid,nodev,noexec,relatime,xattr,release_agent=/lib/systemd/systemd-cgroups-agent,name=systemd)
pstore on /sys/fs/pstore type pstore (rw,nosuid,nodev,noexec,relatime)
efivarfs on /sys/firmware/efi/efivars type efivarfs (rw,nosuid,nodev,noexec,relatime)
```
W pamięci stałej przechowywany jest typ ext.
 * `noatime` - nie zaznaczaj czasu ostatniego dostępu do pliku (access time)
 * `noexec` - nie pozwalaj na uruchomienie plików
 * `sync` - synchronizuj operacje I/O 

Może być przydatne jeśli chcemy skopiować zawartość dysku USB. Dzięki noatime nie tracimy czasu na zapisywanie. Nie chcemy wykonywać plików, bo niekoniecznie są z zaufanego źródła. Opcja sync sprawia, że przy nagłym przerwaniu (np. wyjęciu dysku) wszystkie zmiany do tego momentu będą zapisane.

## Zadanie 5-2

Rysunek z ksiązki

![](https://i.imgur.com/DSyDpto.png)

Cały plik katalogu składa się z ułożonych w niekoniecznie posortowanej kolejności rekordów katalogu. Każdy z nich składa się z następujących części:

* numeru i-węzła (i-node)
* długość w bajtach tego rekordu (ale być może wraz z nieużytkami)
* typ, np. F (file -- plik), D (directory -- katalog), itd.
* prawdziwa długość nazwy w bajtach
* sama nazwa

Gdy usuwamy plik, to jedyne co zmieniamy, to długość poprzedniego rekordu katologu, zwiększamy ją o długość usuwanego rekordu. W ten sposób przechodząc po kolei po rekordach, skacząć dzięki długościom rekordów pominiemy usunięty plik. Tak generują się **nieużytki**.

Gdy za usuwanym rekordem jest usunięty wcześniej rekod, to wszystko działa, bo w jego długość jest już wliczony ten nieużytek. W przypadku gdy wcześniej jest nieużytek również działa, bo żeby znaleźć poprzdni rekord i tak musimy przezukać liniowo od początku, bo nie mamy żadnych "strzałek" wstecz.

Gdy dodajemy to szukamy odpowiednio długiego nieużytku na wstawienie nowego rekordu katalogu. Gdy takiego nie znajdziemy, bo luki są krótkie, to **kompaktujemy**, czyli przepisujemy całą listę rekordów, ale bez nieużytków, teraz możemy na końcu tej listy dopisać nasze informacje (jeśli jest tam miejsce). Mówimy, że dzieje się to leniwie, bo robimy to gdy naprawdę nie mamy już wyboru.

## Zadanie 5-3

**ścieżka bezwględna** pliku to ścieżka, która zaczyna się od folderu głównego i jednoznacznie wskazuje na dany plik.

**i-węzeł** to struktura, która przechowuje informacje o pliku. Dużą część z tej struktury możemy wyświetlić przy pomocy polecenia *stat*

Trawersacja do */usr/share/man/man1/ls.1*
Inody są pierwszą kolumną
![](https://i.imgur.com/TuMseJr.png)

W przypadku ścieżek bezwzględnych trawersacja zaczyna się od inode o id 2, ponieważ jest to standardowe id dla katalogu głównego.

![](https://i.imgur.com/IFp6cbo.png)

Sterownik uniksowego systemu plików wie, gdzie znajduje się dany bajt pliku dzięki drzewiastej strukturze przechowującej informacje o blokach pliku, tzw. bloki pośrednie. Znając rozmiar bloku i rozmiar pliku jesteśmy w stanie określić jakie obszary pliku są obejmowane przez nasze drzewo bloków pośrednich.

Nie możemy utworzyć dowiązania do */proc/version*, ponieważ jest to inny, wirtualny, system plików. Brak takiej możliwości wynika z tego, że każdy system plików numeruje inody w swoim obrębie, przez co mogą one się duplikować dla dwóch różnych FS.


## Zadanie 5-4

```c=
void tty_curpos(int fd, int *x, int *y) {
  struct termios ts, ots;

  tcgetattr(fd, &ts);                  \\ pobranie atrybutów terminala do ts
  memcpy(&ots, &ts, sizeof(struct termios));
  ts.c_lflag &= ~(ECHO | ICANON | CREAD);
  tcsetattr(fd, TCSADRAIN, &ts);        \\ usuwa flagi ECHO, ICANON, CREAD z
                                        \\ atrybutów terminala

  /* How many characters in the input queue. */
  int m = 0;
  /* TODO: Need to figure out some other way to do it on MacOS / FreeBSD. */
#ifdef LINUX
  ioctl(fd, TIOCINQ, &m);               \\ sprawdza ilości bajtów w buforze
                                        \\terminala
#endif

  /* Read them all. */
  char discarded[m];
  m = Read(fd, discarded, m);           \\ robi kopię zapasową kolejki

  Write(fd, CPR(), sizeof(CPR()));      \\ wypisuje pozycję kursora 
                                        \\na terminal
  char buf[20];
  int n = Read(fd, buf, 19);            \\ zapisuje pozycję kursora do buf
  buf[n] = '\0';

  ts.c_lflag |= ICANON;
  tcsetattr(fd, TCSADRAIN, &ts);       \\ustawia flagę ICANON
  for (int i = 0; i < m; i++)
    ioctl(fd, TIOCSTI, discarded + i); \\ przywraca kolejkę

  tcsetattr(fd, TCSADRAIN, &ots);      \\ przywraca poprzedną konfirugrację
                                       \\ terminala
  sscanf(buf, "\033[%d;%dR", x, y);    \\ zapisuje pozycję kursora w x,y
}

```
CPR (Cursor position report) - podaje położenie kursora

![](https://i.imgur.com/J7kkesO.png)


tty_ioctl:
- **TCGETS** struct termios **\*_argp_**

```tcgetattr(fd, argp)``` jest równoznaczny z wywołaniem ```ioctl(tty_fd, TCGETS, argp)```. Zwraca atrybuty terminala.


- **TCSETSW**   const struct termios **\*_argp_**

```tcsetattr(fd, argp)``` odpowiada ```ioctl(tty_fd, TCSETW, argp)``` i ustawia on dane atrubyty treminala.


- **TIOCINQ**   int **\*_argp_**

Zwraca liczbę bajtów w wejściowym buforze.


- **TIOCSTI**   const char **\*_argp_**

Wypisuje dany bajt do kolejki terminala

Sterownik terminala zapewnia interfejs przez, który użytkownik może wchodzić w interakcje z procesami robiącymi dostępy do terminala.

*termios*:
- ECHO

Znaki kolejki wejściowej kierowane są do kolejki wyjściowej.

- ICANON

Zajmuje się rozpoznawaniem znaków specjalnych. Gdy jest ustawiona jesteśmy w trybie kanonicznym, w którym wejście jest przetwarzane linia po linii, które zakończone są znakiem końca linii. Jeśli nie jest ustawiona read nie jest usatysfakcjonowany dopóki nie otrzyma MIN liczby bajtów lub nie upłynie TIME dziesiątek sekund między bajtami.

- CREAD

Umożliwia otrzymywanie przez terminal znaków. Jeśli flaga nie jest ustawiona, żaden znak nie zostanie odebrany.

## Zadanie 5-5

* **metadane pliku** - dodatkowe informacje o pliku, trzymane przez system operacyjny (poza nazwą i danymi), np. wielkość pliku, data i czas jego utworzenia
 
Uruchamiamy program `mkholes`:
```
0000 ................................................................
0064 ................................................................
0128 ...O......O.....................................................
0192 ................................................................
.
.
.
7680 ..............................O..........................O......
7744 ........................O.......................................
7808 ................................................................
7872 .............................................................O..
7936 ............O.................O.........O.......................
8000 ................................................................
8064 ........................O.......................................
8128 ..............................................................O.
Non-zero blocks: 138
```
Wydruk polecenia `stat holes.bin` jest następujący:
```
  File: holes.bin
  Size: 33550336        Blocks: 1104       IO Block: 4096   regular file
Device: 803h/2051d      Inode: 1455679     Links: 1
Access: (0644/-rw-r--r--)  Uid: ( 1000/  hubert)   Gid: (  985/   users)
Access: 2020-11-12 10:21:02.529852762 +0100
Modify: 2020-11-12 10:21:02.563186094 +0100
Change: 2020-11-12 10:21:02.563186094 +0100
 Birth: 2020-11-12 10:21:02.529852762 +0100
```

Widzimy, że `st_blocks` = 1104 (pole Blocks w wydruku). Jednocześnie pole `st_blocks` oznacza liczbę bloków o wielkości $512B$ zaalokowanych na potrzeby pliku. Zatem faktyczna objętość  pliku wynosi $512\;*$ `st_blocks` = $565248$ < $33550336$ = `st_size`. Tak duże `st_size` wynika z faktu, że plik `holes_bin` ma dziury, które nie są zaalokowane przez system, ale są uwzględniane przy obliczaniu `st_size`.

Jednocześnie liczba bloków zgłaszanych przez `mkholes` wynosi $138$, co wynika z tego, że `mkholes` liczy bloki jako segmenty pamięci o wielkości $4096B$. Zauważmy, że $138 * 4096/512 = 1104$, czyli liczba bloków się zgadza.

## Zadanie 5-6
```c=
#include "csapp.h"

#define DIRBUFSZ 256

static void print_mode(mode_t m)
{
  char t;

  if (S_ISDIR(m))
    t = 'd';
  else if (S_ISCHR(m))
    t = 'c';
  else if (S_ISBLK(m))
    t = 'b';
  else if (S_ISREG(m))
    t = '-';
  else if (S_ISFIFO(m))
    t = 'f';
  else if (S_ISLNK(m))
    t = 'l';
  else if (S_ISSOCK(m))
    t = 's';
  else
    t = '?';

  char ur = (m & S_IRUSR) ? 'r' : '-';
  char uw = (m & S_IWUSR) ? 'w' : '-';
  char ux = (m & S_IXUSR) ? 'x' : '-';
  char gr = (m & S_IRGRP) ? 'r' : '-';
  char gw = (m & S_IWGRP) ? 'w' : '-';
  char gx = (m & S_IXGRP) ? 'x' : '-';
  char or = (m & S_IROTH) ? 'r' : '-';
  char ow = (m & S_IWOTH) ? 'w' : '-';
  char ox = (m & S_IXOTH) ? 'x' : '-';

  /* TODO: Fix code to report set-uid/set-gid/sticky bit as 'ls' does. */
  if (ux == 'x')
    ux = (m & S_ISUID) ? 's' : 'x'; //The set-group-ID bit is on, and the corresponding group execution bit is also on
  else
    ux = (m & S_ISUID) ? 'S' : '-'; //the set-user-ID bit is on and the user execution bit is off
  if (gx == 'x')
    gx = (m & S_ISGID) ? 's' : 'x'; //The set-group-ID bit is on, and the corresponding group execution bit is also on
  else
    gx = (m & S_ISGID) ? 'S' : '-'; //the set-group-ID bit is on and the group execution bit is off
  if (ox == 'x')
    ox = (m & S_ISVTX) ? 't' : 'x'; //sticky bit is on and execution is on
  else
    ox = (m & S_ISVTX) ? 'T' : '-'; //sticky bit is on and execution is off

  printf("%c%c%c%c%c%c%c%c%c%c", t, ur, uw, ux, gr, gw, gx, or, ow, ox);
}

static void print_uid(uid_t uid)
{
  struct passwd *pw = getpwuid(uid);
  if (pw)
    printf(" %10s", pw->pw_name);
  else
    printf(" %10d", uid);
}

static void print_gid(gid_t gid)
{
  struct group *gr = getgrgid(gid);
  if (gr)
    printf(" %10s", gr->gr_name);
  else
    printf(" %10d", gid);
}

static void file_info(int dirfd, const char *name)
{
  struct stat sb[1];

  /* TODO: Read file metadata. */
  fstatat(dirfd, name, sb, AT_SYMLINK_NOFOLLOW); //if pathname is a symbolic link, do not dereference it

  print_mode(sb->st_mode);
  printf("%4ld", sb->st_nlink);
  print_uid(sb->st_uid);
  print_gid(sb->st_gid);

  /* TODO: For devices: print major/minor pair; for other files: size. */
  if (S_ISCHR(sb->st_mode) | S_ISBLK(sb->st_mode)) //check that the file is a character or block device
  {
    printf("%6d,", major(sb->st_rdev)); //print major
    printf("%6d", minor(sb->st_rdev));  //print minor
  }
  else
  {
    printf("%13ld", sb->st_size); //print size
  }

  char *now = ctime(&sb->st_mtime);
  now[strlen(now) - 1] = '\0';
  printf("%26s", now);

  printf("  %s", name);

  if (S_ISLNK(sb->st_mode))
  {
    /* TODO: Read where symlink points to and print '-> destination' string. */
    char buf[DIRBUFSZ];
    int size = readlinkat(dirfd, name, buf, DIRBUFSZ);
    if(size != -1){
        buf[size - 1] = '\0'; //add end of string char
        printf(" -> %s", buf);
        }
  }

  putchar('\n');
}

int main(int argc, char *argv[])
{
  if (!argv[1])
    argv[1] = ".";

  int dirfd = Open(argv[1], O_RDONLY | O_DIRECTORY, 0);
  char buf[DIRBUFSZ];
  int n;

  while ((n = Getdents(dirfd, (void *)buf, DIRBUFSZ)))
  {
    struct linux_dirent *d;
    /* TODO: Iterate over directory entries and call file_info on them. */
    for (long buffer_position = 0; buffer_position < n;)
    {
      d = (struct linux_dirent *)(buf + buffer_position);
      file_info(dirfd, d->d_name);
      buffer_position += d->d_reclen; //d_reclen -> size of this dirent
    }
  }

  Close(dirfd);
  return EXIT_SUCCESS;
}
```
**Numer urządzenia** -- składa się z dwóch części: głównego identyfikatora, identyfikującego klasę urządzenia i drugiego ID, który identyfikuje wystąpienie urządzenia w tej klasie. Pierwszy ID pobieramy przez `major`, a drugi przez `minor`.

Dodane linie:
* 37-48 --w tych liniach obsługujemy bity `set-uid/set-gid/sticky`
* 76 -- czytamy matadane pliku
* 83-92 -- sprawdzamy, czy plik jest urządzeniem znakowym/blokowym, jeśli tak, wypisujemy `mojor ID` i `minor ID`, jeśli nie, wypisujemy rozmiar
* 103-108 -- obsługa dowiązania symbolicznego
* 127-132 -- iterowanie się po zawartości katalogu

> [name=Michał Myczkowski] Czy w linijkach 110-113 kodu to zawsze bedzie działało? bo strlen() zdaje sie, szuka pierwszego \0 w ciagu wiec moze to byc w losowym miejscu (w praktyce pewnie na samym poczatku). Lepiej chyba ustawic \0 na pozycji zwróconej przez readlinkat (chyba, ze zwroci -1)

## Zadanie 5-7

Nieużywane gniazda zamykam tak szybko jak to możliwe, aby zapobiec sytuacji oczekiwania na dane, które się już nie pojawią. Przed wykonaniem funkcji `Sort`, zamykane są wszystkie pliki, poza tym, który jest używany do komunikacji z rodzicem.
Proces wysyła dzieciom po połowie liczb, kiedy liczba jest nieparzysta, prawy dostaje o jedną więcej. Następnie proces czyta wysłane przez dzieci dane i przesyła je scalone rodzicowi przy użyciu funkcji `Merge`.
Funkcja działa w stałej pamięci, gdyż od razu po przeczytaniu danych, wysyła je dalej.
```sequence
Rodzic->Proces: Nieposortowane dane
Proces->Lewe dziecko: Pierwsza połowa nieposortowanych danych
Proces->Prawe dziecko: Druga połowa nieposortowanych danych
Lewe dziecko-->Proces: Pierwsza połowa posortowanych danych
Prawe dziecko-->Proces: Druga połowa posortowanych danych
Proces-->Rodzic: Posortowane dane
```

```sequence
Rodzic->Proces: parent_fd
Proces->Lewe dziecko: left.parent_fd
Proces->Prawe dziecko: right.parent_fd
Lewe dziecko-->Proces: left.parent_fd
Prawe dziecko-->Proces: right.parent_fd
Proces-->Rodzic: parent_fd
```
```c=
static void Sort(int parent_fd) {
  int nelem = ReadNum(parent_fd);

  if (nelem < 2) {
    WriteNum(parent_fd, ReadNum(parent_fd));
    Close(parent_fd);
    return;
  }

  sockpair_t left = MakeSocketPair();

  /* TODO: Spawn left child. */
  pid_t c1 = Fork();
  if (!c1)
  {
    // otwartych plików: 3
    Close(parent_fd);
    Close(left.parent_fd);
    Sort(left.child_fd); // left.child_fd zostanie zamknięte w funkcji Sort
    exit(0);
  }
  Close(left.child_fd); // od razu po powrocie z Fork, zamykamy plik przeznaczony dla dziecka
  sockpair_t right = MakeSocketPair();
  // otwartych plików: 4
  /* TODO: Spawn right child. */
  pid_t c2=Fork();
  if (!c2)
  {
      Close(parent_fd);
      Close(right.parent_fd);
      Close(left.parent_fd);
      Sort(right.child_fd);
      exit(0);
  }
  Close(right.child_fd);
  // otwartych plików: 3
  /* TODO: Send elements to children and merge returned values afterwards. */
  SendElem(parent_fd, left.parent_fd, nelem / 2);
  SendElem(parent_fd, right.parent_fd, nelem / 2 + nelem % 2);
  Merge(left.parent_fd, right.parent_fd, parent_fd);
  Close(left.parent_fd);
  Close(right.parent_fd);
  Close(parent_fd);
  /* Wait for both children. */
  Wait(NULL);
  Wait(NULL);
}
```
