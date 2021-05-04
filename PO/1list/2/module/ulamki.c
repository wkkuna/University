//Wiktoria Kuna 316418
#include "ulamki.h"

int NWD(int a, int b)
{
    if (b != 0)
        return NWD(b, a % b);
    return a;
}

int NWW(int a, int b)
{
    return a / NWD(a, b) * b;
}

ulamki *skroc(ulamki *u)
{
    int dz = NWD(u->licznik, u->mianownik);
    u->licznik /= dz;
    u->mianownik /= dz;

    return u;
}

ulamki *ustal_znak(ulamki *u)
{

    int sgn = 1;

    if (u->licznik < 0)
        sgn *= -1;
    if (u->mianownik < 0)
        sgn *= -1;

    u->licznik = sgn * abs(u->licznik);
    u->mianownik = abs(u->mianownik);

    return u;
}

ulamki *stworz_ulamek(int L, int M)
{
    if (M == 0)
        return NULL;

    ulamki *ul = (ulamki *)malloc(sizeof(ulamki));

    ul->licznik = L;
    ul ->mianownik = M;
    
    ul = skroc(ul);
    ul = ustal_znak(ul);

    return ul;
}

ulamki *dod_ul(ulamki *u1, ulamki *u2)
{
    ulamki *u = stworz_ulamek(1, 1);

    int nw = NWW(u1->mianownik, u2->mianownik);
    u->licznik = u1->licznik * nw / u1->mianownik + u2->licznik * nw / u2->mianownik;
    u->mianownik = nw;

    u = skroc(u);
    u = ustal_znak(u);

    return u;
}

void dod_ul1(ulamki *u1, ulamki *u2)
{
    int nw = NWW(u1->mianownik, u2->mianownik);
    u2->licznik = u1->licznik * nw / u1->mianownik + u2->licznik * nw / u2->mianownik;
    u2->mianownik = nw;

    u2 = skroc(u2);
    u2 = ustal_znak(u2);
}

ulamki *odj_ul(ulamki *u1, ulamki *u2)
{
    ulamki *u = stworz_ulamek(1, 1);

    int nw = NWW(u1->mianownik, u2->mianownik);
    u->licznik = u1->licznik * nw / u1->mianownik - u2->licznik * nw / u2->mianownik;
    u->mianownik = nw;

    u = skroc(u);
    u = ustal_znak(u);

    return u;
}

void odj_ul1(ulamki *u1, ulamki *u2)
{
    int nw = NWW(u1->mianownik, u2->mianownik);

    u2->licznik = u1->licznik * nw / u1->mianownik - u2->licznik * nw / u2->mianownik;
    u2->mianownik = nw;

    u2 = skroc(u2);
    u2 = ustal_znak(u2);
}

ulamki *mno_ul(ulamki *u1, ulamki *u2)
{
    ulamki *u = stworz_ulamek(1, 1);

    u->licznik = u1->licznik * u2->licznik;
    u->mianownik = u1->mianownik * u2->mianownik;

    u = skroc(u);
    u = ustal_znak(u);

    return u;
}

void mno_ul1(ulamki *u1, ulamki *u2)
{
    u2->licznik = u1->licznik * u2->licznik;
    u2->mianownik = u1->mianownik * u2->mianownik;

    u2 = skroc(u2);
    u2 = ustal_znak(u2);
}

ulamki *dz_ul(ulamki *u1, ulamki *u2)
{
    if (u2->licznik == 0)
    {
        printf("DZIELENIE PRZEZ 0!");
        return NULL;
    }

    ulamki *u = stworz_ulamek(1, 1);

    u->licznik = u1->licznik * u2->mianownik;
    u->mianownik = u1->mianownik * u2->licznik;

    u = skroc(u);
    u = ustal_znak(u);

    return u;
}

void dz_ul1(ulamki *u1, ulamki *u2)
{
    if (u2->licznik == 0)
    {
        printf("DZIELENIE PRZEZ 0!");
        return;
    }

    int l = u2->licznik;
    u2->licznik = u1->licznik * u2->mianownik;
    u2->mianownik = u1->mianownik * l;

    u2 = skroc(u2);
    u2 = ustal_znak(u2);
}
