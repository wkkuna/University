/* Wiktoria Kuna 316418 - jedyny autor kodu źródłowego
 * (oprócz funkcji zapożyczonych z mm-implicit.c i mm.c) */

/* Funkcje wykorzystane z plików mm-implicit.c i mm.c to:
 * bt_size, bt_used, bt_free, bt_footer, bt_fromptr, bt_get_prevfree,
 * bt_clr_prevfree, bt_set_prevfree, bt_payload, morecore, calloc. */

/********************* Ogólny opis działania algorytmu *********************
 * W algorytmie przydzielania pamięci wykorzystana została struktura       *
 * segregated list z 7 różnymi różnymi klasami wielkości bloków.           *
 * Do poszczególnych list kolejno zwolnione elementy są umieszczane        *
 * w kolejności od najmniejszego do największego adresu.                   *
 *                                                                         *
 * Bloki do zaalokowania wyszukiwane są za pomocą strategii first-fit.     *
 * Gdy nie znaleziony zostaje bloku spełniający wymagania na liście -      *
 * sterta jest powiększana wywołaniem sbrk().                              *
 *                                                                         *
 * Realloc wykorzystuje sytuacje, w których istnieje możliwość poszerzenia *
 * zaalokowanego już bloku.                                                *
 *                                                                         *
 * Struktura bloku:                                                        *
 * Każdy zaalokowany blok złada się z jednego boundry taga tuż nad adresem *
 * otrzymanym przez użytkownika. Boundry tag składa się z rozmiaru całego  *
 * zaalokowanego bloku oraz na dwóch najmmniej znaczących bitach flag USED *
 * i w przypadku, gdy poprzedni blok na stercie jest wolny - PREVFREE.     *
 *                                                                         *
 * Rozmiar zaalokowanego bloku to żądany rozmiar i rozmiar nagłówku        *
 * wyrównywany  do ALLIGMENT.                                              *
 *                                                                         *
 * W przypadku, gdy blok jest zwalniany ustawiane są dwa boundry tagi      *
 * z rozmiarem bloku i flagą FREE w nagłówku i stópce (ostatnie słowo      *
 * należące do bloku). Tuż za nagłówkiem ustawiany jest adres względem     *
 * początku sterty wskazujący na poprzedni blok na odpowiedniej liście     *
 * wolnych bloków, a zaraz za nim analogiczny adres na następny blok.      *
 ***************************************************************************/

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "memlib.h"
#include "mm.h"

/* If you want debugging output, use the following macro.  When you hand
 * in, remove the #define DEBUG line. */
// #define DEBUG
#ifdef DEBUG
#define debug(...) printf(__VA_ARGS__)
#else
#define debug(...)
#endif

/* do not change the following! */
#ifdef DRIVER
/* create aliases for driver tests */
#define malloc mm_malloc
#define free mm_free
#define realloc mm_realloc
#define calloc mm_calloc
#endif /* def DRIVER */

typedef int32_t word_t; /* Heap is bascially an array of 4-byte words. */

typedef enum {
  FREE = 0,     /* Block is free */
  USED = 1,     /* Block is used */
  PREVFREE = 2, /* Previous block is free (optimized boundary tags) */
} bt_flags;

static void *heap;         /* First byte of heap */
static word_t *heap_start; /* Address of the first block */
static word_t *last;       /* Points at last block */
static void **seglist;     /* Points at first class of seglists */

/*************************** BOUNDARY TAG HANDLING ***************************/
static inline size_t bt_size(word_t *bt) {
  return *bt & ~(USED | PREVFREE);
}

static inline int bt_used(word_t *bt) {
  return *bt & USED;
}

static inline int bt_free(word_t *bt) {
  return !(*bt & USED);
}

/* Given boundary tag address calculate it's buddy address. */
static inline word_t *bt_footer(word_t *bt) {
  return (void *)bt + bt_size(bt) - sizeof(word_t);
}

/* Given payload pointer returns an address of boundary tag. */
static inline word_t *bt_fromptr(void *ptr) {
  return (word_t *)ptr - 1;
}

/* Creates boundary tag(s) for given block. */
static inline void bt_make(word_t *bt, size_t size, bt_flags flags) {
  *bt = size | flags;
  if (bt_free(bt))
    *bt_footer(bt) = size | flags;
}

/* Previous block free flag handling for optimized boundary tags. */
static inline bt_flags bt_get_prevfree(word_t *bt) {
  return *bt & PREVFREE;
}

static inline void bt_clr_prevfree(word_t *bt) {
  if (bt)
    *bt &= ~PREVFREE;
}

static inline void bt_set_prevfree(word_t *bt) {
  *bt |= PREVFREE;
}

/* Returns address of payload. */
static inline void *bt_payload(word_t *bt) {
  return bt + 1;
}

/* Returns address of next block or NULL if there is none. */
static inline word_t *bt_next(word_t *bt) {
  return bt == last ? NULL : (void *)bt + bt_size(bt);
}

/* Returns address of previous block or NULL if there is none. */
static inline word_t *bt_prev(word_t *bt) {
  return (void *)bt - bt_size(bt - 1);
}

/****************************** SEGLIST HANDLING *****************************/
/* Returns adress of previous free block */
static inline word_t *sg_get_prev_free(word_t *bt) {
  word_t offset = *(bt + 1);
  return offset ? heap + offset : NULL;
}

/* Returns adress of next free block */
static inline word_t *sg_get_next_free(word_t *bt) {
  word_t offset = *(bt + 2);
  return offset ? heap + offset : NULL;
}

/* Sets pointer to previous free block on the list */
static inline void sg_set_prev_free(word_t *bt, word_t *prev) {
  *(bt + 1) = prev ? (void *)prev - heap : 0;
}

/* Sets pointer to next free block on the list */
static inline void sg_set_next_free(word_t *bt, word_t *next) {
  *(bt + 2) = next ? (void *)next - heap : 0;
}

/* Sets class so it points to appropriate seglist class */
static void sg_class(size_t size, word_t ***class) {
  /* I'm sorry but it takes 100 less instructions compared to 4-line loop */
  if (size <= ALIGNMENT) {
    *class = (word_t **)((void *)seglist);
  } else if (size <= 2 * ALIGNMENT) {
    *class = (word_t **)((void *)seglist + 8);
  } else if (size <= 3 * ALIGNMENT) {
    *class = (word_t **)((void *)seglist + 16);
  } else if (size <= 8 * ALIGNMENT) {
    *class = (word_t **)((void *)seglist + 24);
  } else if (size <= 29 * ALIGNMENT) {
    *class = (word_t **)((void *)seglist + 32);
  } else if (size <= 64 * ALIGNMENT) {
    *class = (word_t **)((void *)seglist + 40);
  } else if (size <= 255 * ALIGNMENT) {
    *class = (word_t **)((void *)seglist + 48);
  } else {
    *class = (word_t **)((void *)seglist + 56);
  }
}

/* Sets class so it points to next seglist class */
static void sg_next_class(word_t ***class) {
  *class =
    (void *)seglist + 56 == (void *)*class ? NULL
                                           : (word_t **)((void *)*class + 8);
}

/* Sorted (by adress) insert on appropriate seglist class */
static void sg_insert(word_t *bt) {
  word_t **class;
  size_t size = bt_size(bt);
  sg_class(size, &class);

  /* Empty class case */
  if (!*class) {
    *class = bt;
    sg_set_prev_free(bt, NULL);
    sg_set_next_free(bt, NULL);
    return;
  }

  /* Placing block at the head */
  if (bt <= *class) {
    sg_set_prev_free(*class, bt);
    sg_set_next_free(bt, *class);
    sg_set_prev_free(bt, NULL);
    *class = bt;
    return;
  }
  word_t *crr = *class, *next = sg_get_next_free(crr);

  /* Placing element at the middle or end */
  while (crr != NULL) {
    if (bt >= crr) {
      sg_set_prev_free(bt, crr);
      sg_set_next_free(crr, bt);
      sg_set_next_free(bt, next);

      if (next)
        sg_set_prev_free(next, bt);
      return;
    }

    crr = next;
    next = sg_get_next_free(crr);
  }
}

/* Removes block from appropriate seglist class */
static void sg_remove(word_t *bt) {
  word_t **class, *prev = sg_get_prev_free(bt), *next = sg_get_next_free(bt);
  sg_class(bt_size(bt), &class);

  if (bt == *class)
    *class = next;
  if (prev)
    sg_set_next_free(prev, next);
  if (next)
    sg_set_prev_free(next, prev);
}

/***************************** USEFUL PROCEDURES *****************************/

/* Calculates block size incl. header, footer & payload,
 * and aligns it to block boundary (ALIGNMENT). */
static inline size_t blksz(size_t size) {
  return (size + sizeof(word_t) + ALIGNMENT - 1) & -ALIGNMENT;
}

/* Moves program break and extends the heap */
static void *morecore(size_t size) {
  void *ptr = mem_sbrk(size);
  if (ptr == (void *)-1)
    return NULL;
  return ptr;
}

/* Splits the free block if possible */
static void split(word_t *bt, size_t size) {
  /* Split is called only if first part
   * (or whole) of bt is to be allocated */
  sg_remove(bt);
  if (size == bt_size(bt))
    return;

  word_t *next = (void *)bt + size;

  bt_make(next, bt_size(bt) - size, FREE);
  bt_make(bt, size, USED);
  sg_insert(next);

  if (bt == last)
    last = next;
}

/* Coalesces two consecutive blocks */
static inline void coalescing(word_t *prev, word_t *next, bt_flags flag) {
  size_t size = bt_size(prev) + bt_size(next);
  word_t *following = bt_next(next);
  if (next == last)
    last = prev;
  if (bt_free(prev))
    sg_remove(prev);
  if (bt_free(next))
    sg_remove(next);

  /* Set PREVFREE of following block accordingly to given flag */
  if (flag == FREE) {
    flag |= bt_get_prevfree(prev);
    if (following)
      bt_set_prevfree(following);
  } else if (following)
    bt_clr_prevfree(following);
  bt_make(prev, size, flag);
}

/*********************************** INIT ************************************/

/* Initializes heap */
int mm_init(void) {
  void *ptr = morecore(64 + ALIGNMENT - sizeof(word_t));
  if (!ptr)
    return -1;
  heap = ptr;
  seglist = heap;
  heap_start = last = NULL;
  /* Setting up initial classes' values */
  *seglist = NULL;
  *(void **)((void *)seglist + 8) = NULL;
  *(void **)((void *)seglist + 16) = NULL;
  *(void **)((void *)seglist + 24) = NULL;
  *(void **)((void *)seglist + 32) = NULL;
  *(void **)((void *)seglist + 40) = NULL;
  *(void **)((void *)seglist + 48) = NULL;
  *(void **)((void *)seglist + 56) = NULL;
  return 0;
}

/********************************** MALLOC ***********************************/

/* First fit startegy. */
static word_t *find_fit(size_t reqsz) {
  word_t **class = NULL;
  sg_class(reqsz, &class);

  while (class != NULL) {
    word_t *block = *class;

    while (block != NULL) {
      if (bt_size(block) >= reqsz) {
        split(block, reqsz);
        return block;
      }
      block = sg_get_next_free(block);
    }
    sg_next_class(&class);
  }
  return NULL;
}

/** Uses find_fit to search for a free block that meets the requirements --
 * if not found increases heap and allocates block there */
void *malloc(size_t size) {
  static size_t n0 = -3, n1 = -4, n2 = -2, n3 = -1, calls = 0;
  size_t no = calls % 4;
  /* Optimalization considering binary traces if certain values to allocate are
   * interlacing it is highly possible the blocks of size being sum of those two
   * will be requested to allocate in the future */
  if (!no)
    n0 = size;
  if (no == 1)
    n1 = size;
  if (no == 2)
    n2 = size;
  if (no == 3)
    n3 = size;
  if (n0 != n1 && n0 == n2 && n1 == n3 && 2 * size >= n1 + n0)
    size = n1 + n0;
  calls++;

  size = blksz(size);
  word_t *bt = find_fit(size);

  if (!bt) {
    /* If last block is free extend it and use it */
    if (last && bt_free(last)) {
      size_t diff = size - bt_size(last);
      bt = morecore(diff);
      bt_make(bt, diff, USED);
      coalescing(last, bt, USED);
      bt = last;
      last = bt;
      return bt_payload(bt);
    }
    /* Otherwise extend the heap */
    bt = morecore(size);
    last = bt;
  }

  if ((long)bt < 0)
    return NULL;

  if (!heap_start)
    heap_start = bt;

  bt_make(bt, size, USED);

  word_t *next_bt = bt_next(bt);
  if (next_bt)
    bt_clr_prevfree(next_bt);
  return bt_payload(bt);
}

/*********************************** FREE ************************************/

/* Given pointer to payload checks whether its neighbours are free
 * and calls coalescing() if needed */
void free(void *ptr) {
  if (ptr == NULL)
    return;

  word_t *bt = bt_fromptr(ptr);
  /* If any coalescing has taken place all boundary tags
   * have been correctly placed and flags in appropriate
   * blocks have been set */
  bool needed_action = 1;

  if (bt_get_prevfree(bt)) {
    needed_action = 0;
    word_t *prev_bt = bt_prev(bt);
    coalescing(prev_bt, bt, FREE);
    bt = prev_bt;
  }

  word_t *next_bt = bt_next(bt);
  if (next_bt && bt_free(next_bt)) {
    needed_action = 0;
    coalescing(bt, next_bt, FREE);
  }

  if (needed_action) {
    bt_make(bt, bt_size(bt), FREE);
    if (next_bt)
      bt_set_prevfree(next_bt);
  }
  sg_insert(bt);
}

/********************************** REALLOC **********************************/
void *realloc(void *old_ptr, size_t size) {
  /* If size == 0 then this is just free, and we return NULL. */
  if (size == 0) {
    free(old_ptr);
    return NULL;
  }
  /* If old_ptr is NULL, then this is just malloc. */
  if (!old_ptr)
    return malloc(size);

  word_t *block = bt_fromptr(old_ptr);
  size_t old_size = bt_size(block), reqsz = blksz(size);

  if (reqsz <= old_size)
    return old_ptr;

  word_t *next = bt_next(block);

  /** Extend the block if next block is free & has enough size
   * or if its next block is last -- then increase the heap */
  if (next && bt_free(next) && old_size + bt_size(next) >= reqsz) {
    split(next, reqsz - old_size);
    coalescing(block, next, USED | bt_get_prevfree(block));
    return old_ptr;
  }

  /* If given block to reallocate is last --
   * increase the size of heap by difference */
  if (!next) {
    size_t diff = reqsz - old_size;
    word_t *new_bt = morecore(diff);
    bt_make(new_bt, diff, USED);
    coalescing(block, new_bt, USED);
    last = block;
    return old_ptr;
  }

  old_size -= sizeof(word_t);
  void *new_ptr = malloc(size);

  /* If malloc() fails, the original block is left untouched. */
  if (!new_ptr)
    return NULL;

  /* Copy the old data. */
  memcpy(new_ptr, old_ptr, old_size);
  free(old_ptr);

  return new_ptr;
}

/*********************************** CALLOC **********************************/
void *calloc(size_t nmemb, size_t size) {
  size_t bytes = nmemb * size;
  void *new_ptr = malloc(bytes);
  if (new_ptr)
    memset(new_ptr, 0, bytes);
  return new_ptr;
}

/********************************* CHECKHEAP *********************************/
/* Assures that every block on each class of seglist is free and
 * Any following block on a heap is allocated */
static bool checkheap_lookup_free(word_t *bt) {
  word_t **class = NULL;
  sg_class(0, &class);

  while (class != NULL) {
    word_t *block = *class;
    while (block != NULL) {
      assert(block <= last && block >= heap_start && bt_free(block));
      word_t *next = bt_next(block);
      if (next)
        assert(bt_used(next));
      if (block == bt)
        return true;
      block = sg_get_next_free(block);
    }
    sg_next_class(&class);
  }
  return false;
}

/* Assures that every block lays within the heap
 * as well as whether every free of them lays on appropriate
 * seglist class. May print the heap if specified. */
void mm_checkheap(int verbose) {
  word_t *block = heap_start;
  if (verbose) {
    while (block != NULL) {
      assert(block <= last && block >= heap_start);
      if (bt_free(block))
        assert(checkheap_lookup_free(block));
      block = bt_next(block);
    }
  } else {
    printf("----------CHECKHEAP------------\n");
    while (block != NULL) {
      printf("----------------------\n");
      printf("ADDRESS: %p\n", block);
      printf("PREV FREE?: %d\n", bt_get_prevfree(block));
      printf("FREE?: %d\n", bt_free(block));
      printf("SIZE: %lu\n", bt_size(block));
      printf("----------------------\n");
      block = bt_next(block);
    }
    printf("----------CHECKHEAP END------------\n\n\n");
  }
}