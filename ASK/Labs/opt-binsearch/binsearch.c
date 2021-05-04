/*
 * Binary search with linearly placed tree levels.
 *
 * Intel® Core™ i5-6600 CPU @ 3.30GHz
 *
 * $ ./binsearch -S 0x5bab3de5da7882ff -n 23 -t 24 -v 0
 * Time elapsed: 7.616777 seconds.
 * $ ./binsearch -S 0x5bab3de5da7882ff -n 23 -t 24 -v 1
 * Time elapsed: 2.884369 seconds.
 */
#include "binsearch.h"

bool binsearch0(T *arr, long size, T x)
{
  do
  {
    size >>= 1;
    T y = arr[size];
    if (y == x)
      return true;
    if (y < x)
      arr += size + 1;
  } while (size > 0);
  return false;
}

void linearize(T *dst, T *src, long size)
{
  T tmp = size;

  long i = 0;
  while(i < size)
  {
    // The distance between left child
    // and right child (also right child to
    // the next left child)
    T diff = tmp + 1;
    
    // Node most to the left on a certain level (depth)
    tmp >>= 1;

    // couter - indicates next node 
    long counter = tmp;

    // assign correct nodes to correspondig indexes in the dst array
    while (counter < size)
    {
      dst[i] = src[counter];
      i++;
      counter += diff;
    }
  }
}

bool binsearch1(T *arr, long size, T x)
{
  long i = 0;
  
  while(i < size)
  {
    T y = arr[i];
    
    if (x==y)
      return true;

    i <<= 1;
    i += (x > y) + 1;
  }

  return false;
}