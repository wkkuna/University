//Wiktoria Kuna 316418
#ifndef TABBIT

#define TABBIT
#include <cmath>
#include <iostream>
using namespace std;

class tab_bit
{
    typedef uint64_t slowo;                            // komorka w tablicy
    static const int rozmiarSlowa = sizeof(slowo) * 8; // rozmiar slowa w bitach
    friend istream &operator>>(istream &we, tab_bit &tb);
    friend ostream &operator<<(ostream &wy, const tab_bit &tb);

public:
    class ref
    {
    public:
        slowo *s;
        int idx;
        bool val;

    public:
        ref(tab_bit *w, int i);
        ref() = delete;
        ~ref() = default;

        operator bool();
        ref &operator=(const ref x);
        ref &operator=(bool val);
    }; // ✓ klasa pomocnicza do adresowania bitów

protected:
    int dl;     // liczba bitów
    slowo *tab; // tablica bitów
public:
    explicit tab_bit(int rozm); //  wyzerowana tablica bitow [0...rozm]
    explicit tab_bit(slowo tb); //  tablica bitów [0...rozmiarSlowa]// zainicjalizowana wzorcem
    tab_bit(initializer_list<bool>);
    tab_bit(const tab_bit &tb);            //  konstruktor kopiujący
    tab_bit(tab_bit &&tb);                 //  konstruktor przenoszący
    tab_bit &operator=(const tab_bit &tb); //  przypisanie kopiujące
    tab_bit &operator=(tab_bit &&tb);      //  przypisanie przenoszące
    ~tab_bit();                            //  destruktor
public:
    bool operator[](int i) const; // indeksowanie dla stałych tablic bitowych
    ref operator[](int i);        // indeksowanie dla zwykłych tablic bitowych
    inline int rozmiar() const;   // rozmiar tablicy w bitach

    tab_bit operator|(const tab_bit &T);
    tab_bit operator|=(const tab_bit &T);

    tab_bit operator&(const tab_bit &T);
    tab_bit operator&=(const tab_bit &T);

    tab_bit operator^(const tab_bit &T);
    tab_bit operator^=(const tab_bit &T);

    bool operator!();
};

#endif