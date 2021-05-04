#include "module/tablica.h"

int main()
{
    array *t = initialize_array();
    printf("IDX(-10) = %d\n", idx(t,-10));

    t = add(t, 10, 4);
    t = add(t, 10, 0);
    t = add(t, 1, -8);
    t = add(t, 3, 2);

    print_array(t);
    printf("IDX(4) = %d\n", idx(t,4));

    free_array(t);
    return 0;
}