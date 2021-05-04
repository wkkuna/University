//Wiktoria Kuna 316418
#include "tabbit.hpp"
#include <sstream>

void wytyczne_zadania()
{
    cout << "**WTYCZNE ZADANIA**" << endl;
    tab_bit t(46); // tablica 46-bitowa (zainicjalizowana zerami)
    cout << "t: " << t << endl;
    tab_bit u(45UL); // tablica 64-bitowa (sizeof(uint64_t)*8)
    cout << "u: " << u << endl;
    tab_bit v(t); // tablica 46-bitowa (skopiowana z t)
    cout << "v: " << v << endl;
    tab_bit w(tab_bit{1, 0, 1, 1, 0, 0, 0, 1}); // tablica 8-bitowa (przeniesiona)
    cout << "w: " << w << endl;
    v[0] = 1; // ustawienie bitu 0-go bitu na 1
    cout << "v: " << v << endl;
    t[45] = true; // ustawienie bitu 45-go bitu na 1
    cout << "t: " << t << endl;
    bool b = v[1];         // odczytanie bitu 1-go
    u[45] = u[46] = u[63]; // przepisanie bitu 63-go do bitow 45-go i 46-go
    cout << "u: " << u << endl;
    cout << "b: " << b << endl;
    cout << t << endl; // wysietlenie zawartości tablicy bitów na ekranie
    cout << endl
         << endl;
}

void konstruktory()
{
    cout << "**KONSTRUKTORY**" << endl;
    tab_bit x(5);
    cout << "x: " << x << endl
         << "(od rozmiaru = 5)" << endl;
    tab_bit y((uint64_t)4343234234234);
    cout << "y: " << y << endl
         << " (od  (uint64_t)4343234234234)" << endl;
    tab_bit z{1, 1, 1, 1, 0, 0, 0, 0, 1};
    cout << "z: " << z << endl
         << " (od listy {1,1,1,1,0,0,0,0,1})" << endl;
    tab_bit a(x);
    cout << "a: " << a << endl
         << " (kopia x)" << endl;
    tab_bit b(move(y));
    cout << "b: " << b << endl
         << " (przeniesiony y)" << endl;
    cout << endl
         << endl;
}

void przypisania()
{
    cout << "**PRZYPISANIA**" << endl;
    tab_bit x(100);
    cout << x << endl;
    x[70] = 1;
    cout << "Ustawienie 70-tego bitu na 1: " << endl
         << x << endl;

    tab_bit y(120);
    y = x;
    cout << "Skopiowanie tablicy: " << endl
         << y << endl;

    tab_bit z(120);
    z = move(y);
    cout << "Przeniesienie tablicy: " << endl
         << z << endl;

    tab_bit ss(10);
    string str = "10011101";
    istringstream stream(str);
    stream >> ss;
    cout << "Wczytanie do obiektu \"10011101\" : " << endl
         << ss << endl;
    cout << endl
         << endl;
}

void operacje_bitowe()
{
    cout << "**OPERACJE BITOWE**" << endl;
    tab_bit y((uint64_t)4343234234234);
    tab_bit x((uint64_t)121212123323);

    cout << "x: " << endl
         << x << endl;
    cout << "y: " << endl
         << y << endl;

    cout << "x ^ y : " << endl
         << (x ^ y) << endl;
    cout << "x ^= y : " << endl
         << (x ^= y) << endl;

    cout << "y | x : " << endl
         << (y | x) << endl;
    cout << "y |= x : " << endl
         << (y |= x) << endl;

    cout << "x & y : " << endl
         << (x & y) << endl;
    cout << "x &= tab_bit((uint64_t)0) : " << endl
         << (x &= tab_bit((uint64_t)0)) << endl;

    cout << "!x : " << endl
         << !x << endl;
    cout << "!y : " << endl
         << !y << endl;
    cout << endl
         << endl;
}
int main()
{
    wytyczne_zadania();
    konstruktory();
    przypisania();
    operacje_bitowe();
}