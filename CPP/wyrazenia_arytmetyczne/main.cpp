//Wiktoria Kuna 316418
#include "wyrazenia_arytmetyczne.hpp"

int main()
{
    Zmienna::przypisz_wartosc("x", 1.);
    Zmienna::przypisz_wartosc("y", 1.);

    Wyrazenie *w = new Odejmij(new Pi(), new Dodaj(new Liczba(2.), new Mnoz(new Zmienna("x"), new Liczba(7.))));
    auto fst = new Dziel(
        new Mnoz(
            new Odejmij(
                new Zmienna("x"),
                new Liczba(1.)),
            new Zmienna("x")),
        new Liczba(2.));

    auto snd = new Dziel(
        new Dodaj(
            new Liczba(3.),
            new Liczba(5.)),
        new Dodaj(
            new Liczba(2.),
            new Mnoz(
                new Zmienna("x"),
                new Liczba(7.))));

    auto trd = new Odejmij(
        new Dodaj(
            new Liczba(2.),
            new Mnoz(
                new Zmienna("x"),
                new Liczba(7.))),
        new Dodaj(
            new Mnoz(
                new Zmienna("y"),
                new Liczba(3.)),
            new Liczba(5.)));

    auto frth = new Dziel(
        new Cos(
            new Mnoz(
                new Dodaj(
                    new Zmienna("x"),
                    new Liczba(1.)),
                new Zmienna("x"))),
        new Exp(
            new Potega(
                new Zmienna("x"),
                new Liczba(2.))));

    auto test = new Odejmij(
        new Odejmij(
            new Liczba(2),
            new Liczba(4)),
        new Odejmij(
            new Liczba(3),
            new Liczba(5)));

    auto test2 = new Dodaj( 
        new Liczba (1),
        new Dodaj(new Liczba(4), 
                  new Dodaj (new Liczba(1), 
                             new Dodaj(new Liczba(0), 
                                       new Liczba(2)))));

    std::cout << w->oblicz() << std::endl;

    std::cout << fst->oblicz() << " " << fst->opis() << std::endl;
    std::cout << snd->oblicz() << " " << snd->opis() << std::endl;
    std::cout << trd->oblicz() << " " << trd->opis() << std::endl;
    std::cout << frth->oblicz() << " " << frth->opis() << std::endl;
    std::cout << test->oblicz() << " " << test->opis() << std::endl;
    std::cout << test2->oblicz() << " " << test2->opis() << std::endl;

    return 0;
}