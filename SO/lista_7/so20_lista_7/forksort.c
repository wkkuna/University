#include "csapp.h"

static void InsertionSort(long table[], size_t left, size_t right)
{
  for (size_t pivot = left + 1; pivot <= right; pivot++)
  {
    size_t insert = left;

    while ((insert < pivot) && (table[insert] < table[pivot]))
      insert++;

    if (insert < pivot)
    {
      size_t n = pivot - insert;
      long tmp = table[pivot];
      memmove(&table[insert + 1], &table[insert], n * sizeof(long));
      table[insert] = tmp;
    }
  }
}

static void SwapElem(long table[], size_t i, size_t j)
{
  long tmp = table[i];
  table[i] = table[j];
  table[j] = tmp;
}

static size_t Partition(long table[], size_t begin, size_t end, long pivot)
{
  size_t left = begin;
  size_t right = end;

  while (left < right)
  {
    while ((left < right) && (table[left] < pivot))
      left++;

    while ((left < right) && (table[right] >= pivot))
      right--;

    if (left < right)
      SwapElem(table, left, right);
  }

  return left;
}

#define INSERTSORT_MAX 32
#define FORKSORT_MIN (1L << 18)

static int QuickSort(long table[], size_t left, size_t right)
{
  pid_t pid_left = -1, pid_right = -1, pid = -1;

  /* TODO: If there is more to sort than FORKSORT_MIN start a subprocess. */

  if (left < right)
  {
    if (right - left <= INSERTSORT_MAX)
    {
      InsertionSort(table, left, right);
    }
    else
    {
      size_t pivot = left + random() % (right - left + 1);
      size_t split = Partition(table, left, right, table[pivot]);

      // Create subprocess if there's more to sort than FORKSORT_MIN
      if (right - left >= FORKSORT_MIN)
      {
        pid = fork();

        /* parent */
        if (pid)
          return pid;

        // Let the subprocess sort
      }

      if (left == split)
      {
        SwapElem(table, left, pivot);
        split++;
      }
      else
      {
        pid_left = QuickSort(table, left, split - 1);
      }

      pid_right = QuickSort(table, split, right);

      /* TODO: Wait for possible children and exit if created a subprocess. */

      if (pid_right != -1)
        Waitpid(pid_right, NULL, 0);
      if (pid_left != -1)
        Waitpid(pid_left, NULL, 0);

      // Exit if created subprocess
      if (pid != -1)
        exit(0);
    }
  }

  return pid;
}

#define NELEMS (1L << 26)

int main(void)
{
  /* Table size in bytes must be divisible by page size. */
  size_t size = NELEMS * sizeof(long);
  assert((size & (getpagesize() - 1)) == 0);

  /* Initialize PRNG seed. */
  struct timeval tv;
  gettimeofday(&tv, NULL);
  srandom(tv.tv_usec);

  /* TODO: Allocate table... */

  // Alokujemy obszar z prawami do odczytu i zapisu
  // używamy odwzorowania dzielonego pamięci anonimowej (żeby tylko
  // dzielić ją z procesami potomnymi)
  long *table = Mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_SHARED, -1, 0);

  /* ... and fill it in with random elements. */
  for (size_t i = 0; i < NELEMS; i++)
    table[i] = random();

  /* Sort it using hybrid algorithm... */
  if (QuickSort(table, 0, NELEMS - 1) > 0)
    Wait(NULL);

  /* ... and verify if the table is actually sorted. */
  long prev = LONG_MIN;
  for (size_t i = 0; i < NELEMS; i++)
  {
    assert(prev <= table[i]);
    prev = table[i];
  }

  return 0;
}
