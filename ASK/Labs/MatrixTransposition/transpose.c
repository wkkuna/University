/*
 * Matrix transposition with and without blocking.
 *
 * Intel® Core™ i5-6600 CPU @ 3.30GHz
 *
 * $ ./transpose -n 32768 -v 0
 * Time elapsed: 21.528841 seconds.
 * $ ./transpose -n 32768 -v 1
 * Time elapsed: 5.251710 seconds.
 */
#include "transpose.h"

void transpose0(T *dst, T *src, int n)
{
  for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
      dst[j * n + i] = src[i * n + j];
}

void transpose1(T *dst, T *src, int n)
{
  // i,j idicates the begining of the 
  // block to be transposed 
  for (int i = 0; i < n; i += BLOCK)
    for (int j = 0; j < n; j += BLOCK)
    // i1, j1 are element idx within the block
    // that is currently transposed
      for (int i1 = i; i1 < i + BLOCK; i1++)
        for (int j1 = j; j1 < j + BLOCK; j1++)
          dst[j1 * n + i1] = src[i1 * n + j1];
}


// Quick comparison
/*
transpose0 shows the most basic approach to
matrix transposition.

It places each row of src matrix in corresponding
spot in dst matrix. As we may notice, vertically 
iterating through dst matrix makes us load new lines
to L1 cache in order to place just one element, most 
possibly evicting it when another one is necessary and
bringing it back when another cell is to be updated.

transpose1 is more cache-optymalised approach, where
we transpose matrix block by block. This reduces unnecessary 
line loading/evicting by updating more data at once 
in a certain block.

*/
