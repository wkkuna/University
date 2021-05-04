#ifndef ULAMKI
#define ULAMKI

#include <stdio.h>
#include <stdlib.h>

typedef struct ulamki
{
    int licznik;
    int mianownik;
} ulamki;

int NWD(int a, int b);
int NWW(int a, int b);
ulamki *stworz_ulamek(int L, int M);
ulamki *dod_ul(ulamki *u1, ulamki *u2);
void dod_ul1(ulamki *u1, ulamki *u2);
ulamki *odj_ul(ulamki *u1, ulamki *u2);
void odj_ul1(ulamki *u1, ulamki *u2);
ulamki *mno_ul(ulamki *u1, ulamki *u2);
void mno_ul1(ulamki *u1, ulamki *u2);
ulamki *dz_ul(ulamki *u1, ulamki *u2);
void dz_ul1(ulamki *u1, ulamki *u2);

#endif