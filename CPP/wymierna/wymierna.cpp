// Wiktoria Kuna 316418
#include "wymierna.hpp"

namespace Obliczenia
{
    /*----------------------WYMIERNA------------------------------*/

    //------------------------INNE---------------------------------
    //-------------------------------------------------------------
    string Wymierna::rozwiniecie(int l, int m) noexcept
    {
        string okres;

        map<int, int> mp;
        mp.clear();

        int reszta = l % m;

        while ((reszta != 0) && (mp.find(reszta) == mp.end()))
        {
            mp[reszta] = okres.length();

            reszta = reszta * 10;

            int res_part = reszta / m;
            okres += to_string(res_part);

            reszta = reszta % m;
        }

        if (reszta != 0)
        {
            okres = okres.substr(mp[reszta]);

            double wynik = static_cast<double>(l) / static_cast<double>(m) - l / m;

            string w = to_string(wynik);

            int s = okres.size();
            int ws = w.size();
            int i = 0;

            while (i < ws - s && w.substr(i, s).compare(okres) != 0)
            {
                i++;
            }

            return w.substr(2, i - 2) + '(' + okres + ')';
        }

        return "";
    }

    void Wymierna::normalizuj() noexcept
    {
        int m = this->mianownik;
        int l = this->licznik;
        int gcd = GCD(l, m);
        bool sgn = signbit(l) ^ signbit(m);

        this->licznik = abs(l / gcd);
        this->mianownik = abs(m / gcd);

        if (sgn)
            this->licznik = -this->licznik;
    }

    static int GCD(int n, int m)
    {
        if (m == 0)
            return n;
        return GCD(m, n % m);
    }

    //----------------------GETTERY--------------------------------
    //-------------------------------------------------------------
    int Wymierna::getMianownik() noexcept
    {
        return mianownik;
    }
    int Wymierna::getLicznik() noexcept
    {
        return licznik;
    }

    //--------------------KONSTRUKTORY-----------------------------
    //-------------------------------------------------------------
    Wymierna::Wymierna(int licznik, int mianownik)
    {
        if (mianownik == 0)
            throw DzieleniePrzezZero();

        this->licznik = licznik;
        this->mianownik = mianownik;
        this->normalizuj();
    }

    Wymierna::Wymierna(int liczba) noexcept
        : Wymierna::Wymierna(liczba, 1) {}

    //----------------------OPERATORY------------------------------
    //-------------------------------------------------------------

    Wymierna Wymierna::operator+(Wymierna x)
    {
        int gcd = GCD(this->mianownik, x.mianownik);
        int lcm = this->mianownik * x.mianownik / gcd;

        bool sgn1 = signbit(this->licznik);
        bool sgn2 = signbit(x.licznik);

        if (lcm < 0)
            throw PrzekroczenieZakresu();

        int l1 = this->licznik * (lcm / this->mianownik);
        int l2 = x.licznik * (lcm / x.mianownik);
        int l = l1 + l2;
        bool sgn3 = signbit(l);

        if (signbit(l1) ^ sgn1 || signbit(l2) ^ sgn2 || !(sgn1 ^ sgn2) & (sgn1 ^ sgn3))
            throw PrzekroczenieZakresu();

        Wymierna w(l, lcm);
        w.normalizuj();
        return w;
    }

    Wymierna Wymierna::operator-(Wymierna x)
    {
        return -x + *this;
    }

    Wymierna Wymierna::operator*(Wymierna x)
    {
        int sgn = signbit(this->licznik) ^ signbit(x.licznik);
        auto gcd1 = GCD(this->licznik, x.mianownik);
        auto gcd2 = GCD(this->mianownik, x.licznik);

        int l = this->licznik / gcd1 * x.licznik / gcd2;
        int m = this->mianownik / gcd2 * x.mianownik / gcd1;

        if (sgn ^ (signbit(l)) || signbit(m) ^ 0)
            throw PrzekroczenieZakresu();

        Wymierna w(l, m);
        w.normalizuj();
        return w;
    }

    Wymierna Wymierna::operator/(Wymierna x)
    {
        return !x * *this;
    }

    Wymierna Wymierna::operator-()
    {
        if (this->licznik == INT32_MIN)
            throw PrzekroczenieZakresu();

        Wymierna w(-this->licznik, this->mianownik);

        return w;
    }

    Wymierna Wymierna::operator!()
    {
        if (this->licznik == 0)
            throw DzieleniePrzezZero();

        int sgn = 0;
        if (this->licznik < 0)
            sgn = 1;

        if (this->licznik == INT32_MIN)
            throw PrzekroczenieZakresu();

        int l;
        if (sgn)
            l = -this->mianownik;
        else
            l = this->mianownik;

        Wymierna w(l,abs(this->licznik));
        return w;
    }

    ostream &operator<<(ostream &wyj, const Wymierna &w) noexcept
    {
        auto roz = Wymierna::rozwiniecie(abs(w.licznik), w.mianownik);

        if (roz.compare("") != 0)
        {
            if(signbit(w.licznik) && w.licznik == 0)
                wyj << '-';

            int cal = w.licznik / w.mianownik;
            wyj << to_string(cal) + '.' + roz;
        }
        else
        {
            auto x = w;
            wyj << static_cast<double>(x);
        }

        return wyj;
    }

    Wymierna::operator double() noexcept
    {
        return (double)this->licznik / this->mianownik;
    }

    Wymierna::operator int() noexcept
    {
        return round(this->licznik / this->mianownik);
    }

    /*-------------------WYJĄTEK WYMIERNA-------------------------*/
    //-------------------------------------------------------------

    WyjatekWymierna::WyjatekWymierna() : message("Wyjątek dla liczby wymiernej") {}

    WyjatekWymierna WyjatekWymierna::operator=(WyjatekWymierna &w)
    {
        this->message = w.message;
        return *this;
    }

    WyjatekWymierna::WyjatekWymierna(const char *msg)
    {
        this->message = msg;
    }

    WyjatekWymierna::WyjatekWymierna(const WyjatekWymierna &x)
    {
        WyjatekWymierna w(x.message);
    }

    const char *WyjatekWymierna::what() const noexcept
    {
        return this->message;
    }

    /*-----------------DZIELENIE PRZEZ ZERO-----------------------*/
    //-------------------------------------------------------------

    DzieleniePrzezZero::DzieleniePrzezZero() : message("Dzielenie przez zero!") {}

    DzieleniePrzezZero::DzieleniePrzezZero(const DzieleniePrzezZero &x)
    {
        DzieleniePrzezZero w(x.message);
    }

    DzieleniePrzezZero::DzieleniePrzezZero(const char *msg)
    {
        this->message = msg;
    }

    DzieleniePrzezZero DzieleniePrzezZero::operator=(DzieleniePrzezZero &w)
    {
        this->message = w.message;
        return *this;
    }

    const char *DzieleniePrzezZero::what() const noexcept
    {
        return this->message;
    }

    /*-----------------PRZEKROCZENIE ZAKRESU----------------------*/
    //-------------------------------------------------------------

    PrzekroczenieZakresu::PrzekroczenieZakresu() : message("Przekroczenie zakresu!") {}

    PrzekroczenieZakresu::PrzekroczenieZakresu(const char *msg)
    {
        this->message = msg;
    }

    PrzekroczenieZakresu::PrzekroczenieZakresu(const PrzekroczenieZakresu &x)
    {
        PrzekroczenieZakresu w(x.message);
    }

    PrzekroczenieZakresu PrzekroczenieZakresu::operator=(PrzekroczenieZakresu &w)
    {
        return *this;
    }

    const char *PrzekroczenieZakresu::what() const noexcept
    {
        return message;
    }
} // namespace Obliczenia