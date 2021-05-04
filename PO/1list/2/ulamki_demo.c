#include "module/ulamki.h"

int main()
{
    ulamki *u1 = stworz_ulamek(1, 4);
    ulamki *u2 = stworz_ulamek(1, 3);
    ulamki *u; 

    u = dod_ul(u1, u2);
    printf("%d/%d + %d/%d = %d/%d\n", u1->licznik, u1->mianownik, u2->licznik, u2->mianownik, u->licznik, u->mianownik);

    free(u);

    u = odj_ul(u1, u2);
    printf("%d/%d - %d/%d = %d/%d\n", u1->licznik, u1->mianownik, u2->licznik, u2->mianownik, u->licznik, u->mianownik);

    free(u);

    u = mno_ul(u1, u2);
    printf("%d/%d * %d/%d = %d/%d\n", u1->licznik, u1->mianownik, u2->licznik, u2->mianownik, u->licznik, u->mianownik);

    free(u);

    u = dz_ul(u1, u2);
    printf("%d/%d / %d/%d = %d/%d\n", u1->licznik, u1->mianownik, u2->licznik, u2->mianownik, u->licznik, u->mianownik);

    free(u1);
    free(u2);
    free(u);

    return 0;
}