// Wiktoria Kuna 316418
#ifndef Q
#define Q

#include<iostream>
#include<cmath>
#include<map>

using namespace std;


namespace Obliczenia
{
    class Wymierna
    {
        private:
            int mianownik;
            int licznik;

        public:
            int getMianownik() noexcept;
            int getLicznik() noexcept;
            
            Wymierna(int licznik, int mianownik);
            Wymierna(int liczba) noexcept;
            Wymierna(const Wymierna&) = default;
            Wymierna(Wymierna&&) = default;

            void normalizuj() noexcept;
            static string rozwiniecie(int l, int m) noexcept;

            Wymierna operator+(Wymierna);
            Wymierna operator-();
            Wymierna operator-(Wymierna);
            Wymierna operator*(Wymierna);
            Wymierna operator/(Wymierna);
            Wymierna operator!();

            friend ostream &operator<<(ostream &wyj, const Wymierna &w) noexcept; 

            operator double() noexcept;
            operator int() noexcept;
    };

    class WyjatekWymierna : public exception
    {
        protected:
            const char* message;
        public:
            WyjatekWymierna();
            WyjatekWymierna(const WyjatekWymierna&);
            WyjatekWymierna(const char*);
            virtual ~WyjatekWymierna() = default;
        
            WyjatekWymierna operator=(WyjatekWymierna&);

            const char* what() const noexcept override;
    };


    class DzieleniePrzezZero : public WyjatekWymierna
    {
        private:
            const char* message;
        public:
        DzieleniePrzezZero();
        DzieleniePrzezZero(const DzieleniePrzezZero&);
        DzieleniePrzezZero(const char* msg);

        DzieleniePrzezZero operator=(DzieleniePrzezZero&);

        const char* what() const noexcept override;
    };

    class PrzekroczenieZakresu : public WyjatekWymierna
    {
        private:
            const char* message;
        public:
        PrzekroczenieZakresu();
        PrzekroczenieZakresu(const PrzekroczenieZakresu&);
        PrzekroczenieZakresu(const char* msg);

        PrzekroczenieZakresu operator=(PrzekroczenieZakresu&);

        const char* what() const noexcept override;
    };

    static int GCD(int n, int m);
};

#endif