#ifndef __CONFIG_H_
#define __CONFIG_H_

/*
 * config.h - malloc lab configuration file
 *
 * Copyright (c) 2002, R. Bryant and D. O'Hallaron, All rights reserved.
 * May not be used, modified, or copied without permission.
 */

/*
 * This is the default path where the driver will look for the
 * default tracefiles. You can override it at runtime with the -t flag.
 */

#ifndef TRACEDIR
#define TRACEDIR "./traces/"
#endif

/*
 * This is the list of default tracefiles in TRACEDIR that the driver
 * will use for testing. Modify this if you want to add or delete
 * traces from the driver's test suite.
 */

#ifndef DEFAULT_TRACEFILES
/* clang-format off */
#define DEFAULT_TRACEFILES \
  "amptjp-bal.rep", \
  "amptjp.rep", \
  "binary-bal.rep", \
  "binary.rep", \
  "binary2-bal.rep", \
  "binary2.rep", \
  "cccp-bal.rep", \
  "cccp.rep", \
  "coalescing-bal.rep", \
  "coalescing.rep", \
  "cp-decl-bal.rep", \
  "cp-decl.rep", \
  "expr-bal.rep", \
  "expr.rep", \
  "random-bal.rep", \
  "random.rep", \
  "random2-bal.rep", \
  "random2.rep", \
  "realloc-bal.rep", \
  "realloc.rep", \
  "realloc2-bal.rep", \
  "realloc2.rep", \
  "short1-bal.rep", \
  "short1.rep", \
  "short2-bal.rep", \
  "short2.rep"
/* clang-format on */
#endif

/*
 * Students get 0 points for this point or below (ops / sec)
 */
#define MIN_SPEED 0E3

/*
 * Students can get more points for building faster allocators,
 * up to this point (in ops / sec)
 */
#define MAX_SPEED 40000E3

/*
 * Students get 0 points for this allocation fraction or below
 */
#define MIN_SPACE 0.6

/*
 * Students can get more points for building more efficient allocators,
 * up to this point (1 is perfect).
 */
#define MAX_SPACE 0.85

/*
 * This constant determines the contributions of space utilization (UTIL_WEIGHT)
 * and throughput (1 - UTIL_WEIGHT) to the performance index.
 */
#define UTIL_WEIGHT .6

/*****************************************************************************
 * Set exactly one of these USE_xxx constants to "1" to select a timing method
 *****************************************************************************/
#define USE_FCYC 1   /* cycle counter w/K-best scheme (x86 only) */
#define USE_ITIMER 0 /* interval timer (any Unix box) */
#define USE_GETTOD 0 /* gettimeofday (any Unix box) */

#endif /* __CONFIG_H */
