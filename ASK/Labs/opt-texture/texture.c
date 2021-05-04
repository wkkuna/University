/*
 * row-major vs. tiled texture queries
 *
 * Intel® Core™ i5-6600 CPU @ 3.30GHz
 *
 * $ ./texture -S 0xdeadc0de -t 65536 -v 0
 * Time elapsed: 1.707234 seconds.
 * $ ./texture -S 0xdeadc0de -t 65536 -v 1
 * Time elapsed: 1.031514 seconds.
 * $ ./texture -S 0xdeadc0de -t 65536 -v 2
 * Time elapsed: 0.935953 seconds.
 */
#include "texture.h"

static inline long index_0(long x, long y) {
  return y * N + x;
}

#define VARIANT 0
#include "texture_impl.h"

static inline long index_1(long x, long y) {
  int BLOCK = 5; // size of block is 2^BLOCK 

  long mask = (1 << BLOCK) - 1;

  // extract BLOCK x's lower bits
  long addr = x & mask;

  // put BLOCK y's lower bits on the upper
  // part of the addr 
  addr |= (y & mask) << BLOCK;

  // take N times x's upper bits
  // perform logic or with y's upper bits
  // place the result on the upper part of a addr 
  addr |= ((y >> BLOCK) | ((x >> BLOCK) * N >> BLOCK)) << (BLOCK << 1);
  return addr;

}
#define VARIANT 1
#include "texture_impl.h"
