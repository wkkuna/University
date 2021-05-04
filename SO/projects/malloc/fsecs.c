/****************************
 * High-level timing wrappers
 ****************************/
#include <stdio.h>
#include "fsecs.h"
#include "fcyc.h"
#include "clock.h"
#include "ftimer.h"
#include "config.h"

#if USE_FCYC
static double Mhz; /* estimated CPU clock frequency */
#endif

extern int verbose; /* -v option in mdriver.c */

/*
 * init_fsecs - initialize the timing package
 */
void init_fsecs(void) {
#if USE_FCYC
  if (verbose)
    printf("Measuring performance with a cycle counter.\n");

  /* set key parameters for the fcyc package */
  set_fcyc_k(10);
  set_fcyc_maxsamples(100);
  set_fcyc_epsilon(0.01);
  set_fcyc_compensate(0);
  set_fcyc_clear_cache(1);
  set_fcyc_cache_size(1 << 19);
  set_fcyc_cache_block(64);
  Mhz = mhz(verbose > 0);
#elif USE_ITIMER
  if (verbose)
    printf("Measuring performance with the interval timer.\n");
#elif USE_GETTOD
  if (verbose)
    printf("Measuring performance with gettimeofday().\n");
#endif
}

/*
 * fsecs - Return the running time of a function f (in seconds)
 */
double fsecs(fsecs_test_funct f, void *argp) {
#if USE_FCYC
  double cycles = fcyc(f, argp);
  return cycles / (Mhz * 1e6);
#elif USE_ITIMER
  return ftimer_itimer(f, argp, 10);
#elif USE_GETTOD
  return ftimer_gettod(f, argp, 10);
#endif
}
