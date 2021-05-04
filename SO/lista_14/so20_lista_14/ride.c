#include "csapp.h"

static __thread unsigned seed;

static void rand_usleep(int min, int max) {
  usleep(rand_r(&seed) % (max - min + 1) + min);
}

#define DEBUG
#ifdef DEBUG
static __unused void outc(char c) {
  Write(STDOUT_FILENO, &c, 1);
}

/* XXX Please use following function to simulate malicious scheduler.
 * Just insert a call to rand_yield between instructions in your solution. */
static __unused void rand_yield(void) {
  /* Once every 100 calls to this function (on average)
   * it yields and lets kernel choose another thread. */
  if (rand_r(&seed) % 100 == 42)
    sched_yield();
}
#else
#define outc(c)
#define rand_yield()
#endif

typedef struct ride {
  /* TODO: Put internal state & mutexes & condvars here. */
} ride_t;

static void ride_init(ride_t *r, unsigned seats) {
}

static void ride_destroy(ride_t *r) {
  /* TODO: Destroy all synchronization primitives. */
}

static void cart_load(ride_t *r) {
  /* TODO: Wait for all seats to be taken and depart. */
}

static void cart_unload(ride_t *r) {
  /* TODO: Wait for all passangers to leave and be ready for next ride. */
}

static void passenger_board(ride_t *r) { 
  /* TODO: Wait for the cart, enter it and wait for the ride to begin. */
}

static void passenger_unboard(ride_t *r) {
  /* TODO: Wait for the ride to end and leave the cart. */
}

static void *cart(void *data) {
  ride_t *r = data;

  seed = (unsigned)pthread_self();

  while (true) {
    outc('L');
    cart_load(r);

    rand_usleep(1000, 2000);

    outc('U');
    cart_unload(r);
  }

  return NULL;
}

static void *passenger(void *data) {
  ride_t *r = data;

  seed = (unsigned)pthread_self();

  while(true) {   
    outc('-');
    passenger_board(r);

    rand_usleep(500, 1000);

    outc('!');
    passenger_unboard(r);

    outc('+');
    rand_usleep(2000, 4000);
  }

  return NULL;
}

#define PASSENGERS 50
#define SEATS 10

int main(void) {
  ride_t r;
  ride_init(&r, SEATS);

  pthread_t cartThread;
  pthread_t passengerThread[PASSENGERS];

  pthread_create(&cartThread, NULL, cart, &r);
  for (int i = 0; i < 50; i++)
    pthread_create(&passengerThread[i], NULL, passenger, &r);

  pthread_join(cartThread, NULL);
  for (int i = 0; i < 50; i++)
    pthread_join(passengerThread[i], NULL);

  ride_destroy(&r);
  return 0;
}
