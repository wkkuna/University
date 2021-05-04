#include <stdio.h>
#include <stdlib.h>

typedef int Tval;
typedef int Tkey;

typedef struct arr
{
    Tval value;
    Tkey key;
    struct arr *next;
} array;

array *initialize_array();
Tval idx(array *t, Tkey key);
array *add(array *t, Tval value, Tkey key);
void print_array(array *t);
void free_array(array* head);