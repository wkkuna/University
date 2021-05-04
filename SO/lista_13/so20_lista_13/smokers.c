#include "csapp.h"

static __unused void outc(char c) { Write(STDOUT_FILENO, &c, 1); }

static __thread unsigned seed;

static sem_t tobacco;
static sem_t matches;
static sem_t paper;
static sem_t doneSmoking;

/* TODO: If you need any extra global variables, then define them here. */
static sem_t pusherSem;
static sem_t tobaccoSem;
static sem_t paperSem;
static sem_t matchSem;
static bool isTobacco;
static bool isPaper;
static bool isMatch;

static void *agent(void *arg) {
  seed = pthread_self();

  while (true) {
    Sem_wait(&doneSmoking);

    int choice = rand_r(&seed) % 3;
    if (choice == 0) {
      Sem_post(&tobacco);
      Sem_post(&paper);
    } else if (choice == 1) {
      Sem_post(&tobacco);
      Sem_post(&matches);
    } else {
      Sem_post(&paper);
      Sem_post(&matches);
    }
  }

  return NULL;
}

/* TODO: If you need extra threads, then define their main procedures here. */

static void *tobacco_pusher(void *arg) {

  while (true) {
    /* code */

    Sem_wait(&tobacco);
    Sem_wait(&pusherSem);

    if (isPaper) {
      Sem_post(&matchSem);
      isPaper = false;
    } else if (isMatch) {
      isMatch = false;
      Sem_post(&paperSem);
    } else {
      isTobacco = true;
    }

    Sem_post(&pusherSem);
  }
  return NULL;
}

static void *paper_pusher(void *arg) {

  while (true) {
    /* code */

    Sem_wait(&paper);
    Sem_wait(&pusherSem);

    if (isMatch) {
      Sem_post(&tobaccoSem);
      isMatch = false;
    } else if (isTobacco) {
      isTobacco = false;
      Sem_post(&matchSem);
    } else {
      isPaper = true;
    }

    Sem_post(&pusherSem);
  }

  return NULL;
}

static void *matches_pusher(void *arg) {

  while (true) {

    Sem_wait(&matches);
    Sem_wait(&pusherSem);

    if (isPaper) {
      Sem_post(&tobaccoSem);
      isPaper = false;
    } else if (isTobacco) {
      isTobacco = false;
      Sem_post(&paperSem);
    } else {
      isMatch = true;
    }

    Sem_post(&pusherSem);
  }
  return NULL;
}

static void randsleep(void) { usleep(rand_r(&seed) % 1000 + 1000); }

static void make_and_smoke(char smoker) {
  randsleep();
  Sem_post(&doneSmoking);
  outc(smoker);
  randsleep();
}

static void *smokerWithMatches(void *arg) {
  seed = pthread_self();

  while (true) {

    /* TODO: wait for paper and tobacco */
    Sem_wait(&matchSem);
    printf("Smoker with matches\n");
    make_and_smoke('M');
  }

  return NULL;
}

static void *smokerWithTobacco(void *arg) {
  seed = pthread_self();

  while (true) {
    /* TODO: wait for paper and matches */
    Sem_wait(&tobaccoSem);
    printf("Smoker with tobacco\n");
    make_and_smoke('T');
  }

  return NULL;
}

static void *smokerWithPaper(void *arg) {
  seed = pthread_self();

  while (true) {
    /* TODO: wait for tobacco and matches */
    Sem_wait(&paperSem);
    printf("Smoker with paper\n");
    make_and_smoke('P');
  }

  return NULL;
}

int main(void) {
  Sem_init(&tobacco, 0, 0);
  Sem_init(&matches, 0, 0);
  Sem_init(&paper, 0, 0);
  Sem_init(&doneSmoking, 0, 1);

  /* TODO: Initialize your global variables here. */
  isPaper = isMatch = isTobacco = false;
  Sem_init(&tobaccoSem, 0, 0);
  Sem_init(&matchSem, 0, 0);
  Sem_init(&paperSem, 0, 0);

  Sem_init(&pusherSem, 0, 1);

  pthread_t paperPusherThread, tobaccoPusherThread, matchesPusherThread;
  Pthread_create(&paperPusherThread, NULL, paper_pusher, NULL);
  Pthread_create(&tobaccoPusherThread, NULL, tobacco_pusher, NULL);
  Pthread_create(&matchesPusherThread, NULL, matches_pusher, NULL);

  pthread_t agentThread;
  Pthread_create(&agentThread, NULL, agent, NULL);

  pthread_t smokerPaperThread, smokerMatchesThread, smokerTobaccoThread;
  Pthread_create(&smokerPaperThread, NULL, smokerWithPaper, NULL);
  Pthread_create(&smokerMatchesThread, NULL, smokerWithMatches, NULL);
  Pthread_create(&smokerTobaccoThread, NULL, smokerWithTobacco, NULL);

  Pthread_join(agentThread, NULL);
  Pthread_join(smokerPaperThread, NULL);
  Pthread_join(smokerMatchesThread, NULL);
  Pthread_join(smokerTobaccoThread, NULL);

  return 0;
}
