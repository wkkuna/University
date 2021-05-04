// Wiktoria Kuna 316418
#include "wymierna.hpp"


int main()
{
    /****** Konstrukcja i upraszczanie ******/
    //---------------------------------------/
    try
    {
        cout << "1/0 = ";
        Obliczenia::Wymierna w(1, 0);
        cout << w << endl;
    }
    catch (const exception &e)
    {
        cerr << e.what() << '\n';
    }

    cout <<endl;

    try
    {
        cout << "6/-18 = ";
        Obliczenia::Wymierna w(6, -18);
        cout << w.getLicznik() << '/' << w.getMianownik() << " = "
             << w << endl;
    }
    catch (const exception &e)
    {
        cerr << e.what() << '\n';
    }
    cout <<endl;

    /********** Dodawanie i błędy ***********/
    //---------------------------------------/
    try
    {
        cout << "3/6 + 1/5 = ";
        Obliczenia::Wymierna w(3, 6);
        Obliczenia::Wymierna x(1, 5);

        auto y = w + x;
        cout << w.getLicznik() << '/' << w.getMianownik() << " + "
             << x.getLicznik() << '/' << x.getMianownik()
             << " = " << y << endl;
    }
    catch (const exception &e)
    {
        cerr << e.what() << '\n';
    }
    cout <<endl;

    try
    {
        cout << "INT32_MIN/1 + -5/1 = ";
        Obliczenia::Wymierna w(INT32_MIN, 1);
        Obliczenia::Wymierna x(-5, 1);

        auto y = w + x;
        cout << w.getLicznik() << '/' << w.getMianownik() << " + "
             << x.getLicznik() << '/' << x.getMianownik()
             << " = " << y << endl;
    }
    catch (const exception &e)
    {
        cerr << e.what() << '\n';
    }
    cout <<endl;

    try
    {
        cout << "INT32_MAX/1 + 9/1 = ";
        Obliczenia::Wymierna w(INT32_MAX, 1);
        Obliczenia::Wymierna x(9, 1);

        auto y = w + x;
        cout << w.getLicznik() << '/' << w.getMianownik() << " + "
             << x.getLicznik() << '/' << x.getMianownik()
             << " = " << y << endl;
    }
    catch (const exception &e)
    {
        cerr << e.what() << '\n';
    }
    cout <<endl;

    /********** Odejmowanie i błędy ***********/
    //-----------------------------------------/
    try
    {
        cout << "173/7 - 655/9 = ";
        Obliczenia::Wymierna w(173, 7);
        Obliczenia::Wymierna x(655, 9);

        auto y = w - x;
        cout << w.getLicznik() << '/' << w.getMianownik() << " - "
             << x.getLicznik() << '/' << x.getMianownik()
             << " = " << y << endl;
    }
    catch (const exception &e)
    {
        cerr << e.what() << '\n';
    }
    cout <<endl;

    try
    {
        cout << "INT32_MIN/1 - 65/3 = ";
        Obliczenia::Wymierna w(INT32_MIN, 1);
        Obliczenia::Wymierna x(65, 3);

        auto y = w - x;
        cout << w.getLicznik() << '/' << w.getMianownik() << " - "
             << x.getLicznik() << '/' << x.getMianownik()
             << " = " << y << endl;
    }
    catch (const exception &e)
    {
        cerr << e.what() << '\n';
    }

    try
    {
        cout << "-(-18/4) = ";
        Obliczenia::Wymierna w(-18, 4);

        auto y = -w;
        cout << abs(y.getLicznik()) << '/' << y.getMianownik()  << " = "
             << y << endl;
    }
    catch (const exception &e)
    {
        cerr << e.what() << '\n';
    }

    cout <<endl;

    /********** Mnożenie i błędy ***********/
    //--------------------------------------/

    try
    {
        cout << "878/9 * 122/90 = ";
        Obliczenia::Wymierna w(878, 9);
        Obliczenia::Wymierna x(122, 90);

        auto y = w * x;
        cout << w.getLicznik() << '/' << w.getMianownik() << " * "
             << x.getLicznik() << '/' << x.getMianownik()
             << " = " << y << endl;
    }
    catch (const exception &e)
    {
        cerr << e.what() << '\n';
    }
    cout <<endl;

    try
    {
        cout << "878432343/1 * 1129223122/1 = ";
        Obliczenia::Wymierna w(878432343, 1);
        Obliczenia::Wymierna x(1129223122, 1);

        auto y = w * x;
        cout << w.getLicznik() << '/' << w.getMianownik() << " * "
             << x.getLicznik() << '/' << x.getMianownik()
             << " = " << y << endl;
    }
    catch (const exception &e)
    {
        cerr << e.what() << '\n';
    }
    cout <<endl;

    /********** Dzielnie i błędy ***********/
    //--------------------------------------/

    try
    {
        cout << "312/13 / 923/17 = ";
        Obliczenia::Wymierna w(312, 13);
        Obliczenia::Wymierna x(923, 17);

        auto y = w / x;
        cout << w.getLicznik() << '/' << w.getMianownik() << " / "
             << x.getLicznik() << '/' << x.getMianownik()
             << " = " << y << endl;
    }
    catch (const exception &e)
    {
        cerr << e.what() << '\n';
    }
    cout <<endl;

    try
    {
        cout << "31212/7 / 0/17 = ";
        Obliczenia::Wymierna w(31212, 7);
        Obliczenia::Wymierna x(0, 17);

        auto y = w / x;
        cout << w.getLicznik() << '/' << w.getMianownik() << " / "
             << x.getLicznik() << '/' << x.getMianownik()
             << " = " << y << endl;
    }
    catch (const exception &e)
    {
        cerr << e.what() << '\n';
    }
    cout <<endl;

    try
    {
        cout << "-12/13 / 23/INT32_MAX = ";
        Obliczenia::Wymierna w(-12, 13);
        Obliczenia::Wymierna x(23, INT32_MAX);

        auto y = w / x;
        cout << w.getLicznik() << '/' << w.getMianownik() << " / "
             << x.getLicznik() << '/' << x.getMianownik()
             << " = " << y << endl;
    }
    catch (const exception &e)
    {
        cerr << e.what() << '\n';
    }
    cout <<endl;


    try
    {
        cout << "!-812/17 = ";
        Obliczenia::Wymierna w(-812, 17);

        auto y = !w;
        cout << y.getLicznik() << '/' << y.getMianownik()  << " = "
             << y << endl;
    }
    catch (const exception &e)
    {
        cerr << e.what() << '\n';
    }
    cout <<endl;

    /************** Konwersje **************/
    //--------------------------------------/

    try
    {
        cout << "static_cast<double>(-138/17) = ";
        Obliczenia::Wymierna w(-138, 19);

        auto y = static_cast<double>(w);
        cout << w.getLicznik() << '/' << w.getMianownik() << " = "
             << y << endl;
    }
    catch (const exception &e)
    {
        cerr << e.what() << '\n';
    }
    cout <<endl;

    try
    {
        cout << "static_cast<int>(-9812/17) = ";
        Obliczenia::Wymierna w(-9812, 17);

        auto y = static_cast<int>(w);
        cout << w.getLicznik() << '/' << w.getMianownik() << " = "
             << y << endl;
    }
    catch (const exception &e)
    {
        cerr << e.what() << '\n';
    }
    cout <<endl;


}
