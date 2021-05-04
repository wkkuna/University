#ifndef DRIVER
#define DRIVER
#endif

#include "memlib.h"
#include "mm.h"

int main(void) {

  // a 0 4092
  // a 1 16
  // r 0 4097
  // a 2 16
  // f 1
  // r 0 4102
  // a 3 16
  // f 2
  // r 0 4107
  // a 4 16
  // f 3
  // r 0 4112
  // a 5 16
  // f 4
  // r 0 4117
  // a 6 16
  // f 5

  // r 0 4122
  // a 7 16
  // f 6

  // r 0 4127
  // a 8 16
  // f 7

  // r 0 4132
  // a 9 16
  // f 8

  // r 0 4137
  // a 10 16
  // f 9

  // r 0 4142
  // a 11 16
  // f 10

  // r 0 4147
  // a 12 16
  // f 11

  // r 0 4152
  // a 13 16
  // f 12

  // r 0 4157
  // a 14 16
  // f 13

  // r 0 4162
  // a 15 16
  // f 14

  // r 0 4167
  // a 16 16

  mem_init();
  mm_init();

  void *a0 = mm_malloc(4092);
  void *a1 = mm_malloc(15);
  a0 = mm_realloc(a0, 4097);
  void *a2 = mm_malloc(16);
  mm_free(a1);

  a0 = mm_realloc(a0, 4102);
  void *a3 = mm_malloc(16);
  mm_free(a2);

  a0 = mm_realloc(a0, 4107);
  void *a4 = mm_malloc(16);
  mm_free(a3);

  a0 = mm_realloc(a0, 4112);
  void *a5 = mm_malloc(16);
  mm_free(a4);

  a0 = mm_realloc(a0, 4117);
  void *a6 = mm_malloc(16);
  mm_free(a5);

  a0 = mm_realloc(a0, 4122);
  void *a7 = mm_malloc(16);
  mm_free(a6);

  a0 = mm_realloc(a0, 4127);
  void *a8 = mm_malloc(16);
  mm_free(a7);

  a0 = mm_realloc(a0, 4132);
  void *a9 = mm_malloc(16);
  mm_free(a8);

  a0 = mm_realloc(a0, 4137);
  void *a10 = mm_malloc(16);
  mm_free(a9);

  a0 = mm_realloc(a0, 4142);
  void *a11 = mm_malloc(16);
  mm_free(a10);
  mm_free(a11);

  return 0;
}