#include "csapp.h"

static __unused void outc(char c) {
  Write(STDOUT_FILENO, &c, 1);
}

#define N 100
#define M 100

static struct {
  /* TODO: Put semaphores and shared variables here. */
  int portions;
  sem_t PotAccess;
  sem_t EmptyPot;
  sem_t FullPot;
} *shared = NULL;


static void savage(void) {
  for (;;) {
    /* TODO Take a meal or wait for it to be prepared. */
    Sem_wait(&shared->PotAccess);
    
    if(!shared->portions){
      Sem_post(&shared->EmptyPot);
      Sem_wait(&shared->FullPot);
    }

    printf("EAT!\n");

    shared->portions--;
    Sem_post(&shared->PotAccess);

    /* Sleep and digest. */
    usleep(rand() % 1000 + 1000);
  }

  exit(EXIT_SUCCESS);
}

static void cook(void) {
  for (;;) {
    /* TODO Cook is asleep as long as there are meals.
     * If woken up they cook exactly M meals. */

    Sem_wait(&shared->EmptyPot);
    printf("COOK!\n");
    
    shared->portions = M;

    printf("COOK SLEEP!\n");
    Sem_post(&shared->FullPot);
  }

}

/* Do not bother cleaning up after this process. Let's assume that controlling
 * terminal sends SIGINT to the process group on CTRL+C. */
int main(void) {
  shared = Mmap(NULL, getpagesize(), PROT_READ|PROT_WRITE, MAP_ANON|MAP_SHARED,
                -1, 0);

  /* TODO: Initialize semaphores and other shared state. */
  shared->portions = M;
  Sem_init(&shared->PotAccess,1,1);
  Sem_init(&shared->EmptyPot,1,0);
  Sem_init(&shared->FullPot,1,0);

  for (int i = 0; i < N; i++)
    if (Fork() == 0)
      savage();

  cook();

  return EXIT_SUCCESS;
}
