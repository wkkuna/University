#include "prosta.hpp"

int main()
{
    try
    {
        double a = 0.1, b = 0.6, c = 3.0, d = 4.0, e = 5.7, f = 6.9;

        punkt A(a, b), B(c, d);
        wektor vec(c, d);
        wektor v1(e, f);

        wektor v2 = wektor::dodajWektory(vec, v1);
        punkt C(A, vec);

        {
            cout << "Tworzenie punktów:" << endl;

            cout << endl;

            cout << "Punkt ze współrzędnych (" << a << "," << b << "):" << endl;
            A.wypisz();

            cout << endl;

            cout << "Punkt C z punktu ";
            A.wypisz();
            cout << "oraz wektora ";
            vec.wypisz();
            C.wypisz();

            cout << endl;
        }

        {
            cout << "Tworzenie wektorów:" << endl;

            cout << endl;

            cout << "Wektor vec ze współrzędnych [" << c << "," << d << "]" << endl;
            vec.wypisz();
            cout << endl;

            cout << "[" << c << "," << d << "] + [" << e << "," << f << "] = [" << v2.dx << "," << v2.dy << "]" << endl;
        }

        {
            prosta p(A, B);
            cout << "Prosta przechodząca przez punkty: "
                 << "(" << a << "," << b << ") i "
                 << "(" << c << "," << d << "):" << endl;
            p.wypisz();

            cout << endl;

            prosta g(v1);
            cout << "Prosta z wektora: ";
            v1.wypisz();
            g.wypisz();

            cout << endl;

            double G = 6.2, E = 99.7, F = 0.2137;

            prosta q(G, E, F);
            cout << "Prosta ze współczynników: "
                 << "A = " << G << " B = " << E << " C = " << F << ":" << endl;
            q.wypisz();

            cout << endl;

            prosta m(q, v2);
            cout << "Prosta z prostej ";
            q.wypisz();
            cout << " i wektora ";
            v2.wypisz();
            m.wypisz();

            cout << endl;

            prosta w(G, E, F + 2.0);

            cout << "Czy proste są równoległe?" << endl;
            q.wypisz();
            w.wypisz();
            if (czyRownolegle(q, w))
                cout << "TAK" << endl;
            else
                cout << "NIE" << endl;

            cout << endl;

            prosta v(-G, E, F + 2.0);

            cout << "Czy proste są prostopadłe?" << endl;
            q.wypisz();
            v.wypisz();
            if (czyProstopadle(q, v))
                cout << "TAK" << endl;
            else
                cout << "NIE" << endl;

            cout << endl;

            cout << "Punkt przecięcia prostych" << endl;
            q.wypisz();
            v.wypisz();
            punkt S = przeciecia(q, v);
            S.wypisz();
        }

        cout << endl;
        prosta(0 ,0 ,0);
    }
    catch (const std::exception &e)
    {
        std::cerr << e.what() << '\n';
    }

    return 0;
}