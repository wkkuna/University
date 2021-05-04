//Wiktoria Kuna 316418
#ifndef KALKULATOR
#define KALKULATOR

#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <functional>
#include <map>
#include <cmath>
#include <algorithm>
#include <stack>

namespace kalkulator
{
    /****************************** INNE ******************************/
    /******************************************************************/
    bool isLegal(std::string name);
    bool isConst(std::string name);
    bool isNum(std::string nazwa);

    //-----------------------------------------------------------------------

    class Wyrazenie
    {
    public:
        virtual double oblicz(std::stack<double> *env) = 0;
    };

    class ONP
    {
    private:
        std::vector<Wyrazenie *> Wyr;

    public:
        ONP(std::vector<std::string>);
        double oblicz();
    };
    //-----------------------------------------------------------------------

    //-----------------------------------------------------------------------

    /**************************** OPERANDY ****************************/
    /******************************************************************/
    //-----------------------------------------------------------------------
    class Operand : public virtual Wyrazenie
    {
    public:
        virtual double oblicz(std::stack<double> *env) = 0;
    };

    //-----------------------------------------------------------------------
    class Symbol : public virtual Operand
    {
    public:
        virtual double oblicz(std::stack<double> *env) = 0;
    };
    //-----------------------------------------------------------------------
    class Zmienna : public virtual Symbol
    {
    protected:
        std::string nazwa;
        static std::map<std::string, double> zmienne;

    public:
        Zmienna() = default;
        Zmienna(std::string nazwa);
        Zmienna(std::string nazwa, double wartosc);
        void przypisz(std::string, double wartosc);
        void wyczysc();
        double oblicz(std::stack<double> *env) override;
        double oblicz();
    };
    //-----------------------------------------------------------------------

    //-----------------------------------------------------------------------
    class Stala : public virtual Symbol
    {
    protected:
        const std::string nazwa;
        const double wartosc;

    public:
        Stala(std::string nazwa, double wartosc);

        double oblicz(std::stack<double> *env) override;
        double oblicz();
    };
    //-----------------------------------------------------------------------

    //-----------------------------------------------------------------------
    class Pi : public Stala
    {
    public:
        Pi();
    };
    //-----------------------------------------------------------------------

    //-----------------------------------------------------------------------
    class E : public Stala
    {
    public:
        E();
    };
    //-----------------------------------------------------------------------

    //-----------------------------------------------------------------------
    class Fi : public Stala
    {
    public:
        Fi();
    };
    //-----------------------------------------------------------------------

    //-----------------------------------------------------------------------
    class Liczba : public virtual Operand
    {
    protected:
        const double wartosc;

    public:
        Liczba(const double wartosc);

        double oblicz(std::stack<double> *env) override;
        double oblicz();
    };
    //-----------------------------------------------------------------------

    /**************************** FUNKCJE *****************************/
    /******************************************************************/
    //-----------------------------------------------------------------------
    class Funkcja : public Wyrazenie
    {
    public:
        virtual double oblicz(std::stack<double> *env) = 0;
    };

    class Operator1arg : public virtual Funkcja
    {
    private:
        std::function<double(double)> fun;
        static std::map<std::string, std::function<double(double)>> funkcje;

    public:
        Operator1arg(std::function<double(double)> fun);

        double oblicz(std::stack<double> *env) override;
    };
    //-----------------------------------------------------------------------

    //-----------------------------------------------------------------------
    class Operator2arg : public Funkcja
    {
    private:
        std::function<double(double, double)> fun;

    public:
        Operator2arg(std::function<double(double, double)> fun);

        double oblicz(std::stack<double> *env) override;
    };
    //-----------------------------------------------------------------------

    /***************************** 1ARG ******************************/
    //-----------------------------------------------------------------------
    class Sin : public Operator1arg
    {
    public:
        Sin();
    };
    //-----------------------------------------------------------------------

    //-----------------------------------------------------------------------
    class Cos : public Operator1arg
    {
    public:
        Cos();
    };
    //-----------------------------------------------------------------------

    //-----------------------------------------------------------------------
    class Bezwgl : public Operator1arg
    {
    public:
        Bezwgl();
    };
    //-----------------------------------------------------------------------

    //-----------------------------------------------------------------------
    class Exp : public Operator1arg
    {
    public:
        Exp();
    };
    //-----------------------------------------------------------------------

    //-----------------------------------------------------------------------
    class Ln : public Operator1arg
    {
    public:
        Ln();
    };

    class Sgn : public Operator1arg
    {
    public:
        Sgn();
    };

    class Floor : public Operator1arg
    {
    public:
        Floor();
    };

    class Ceil : public Operator1arg
    {
    public:
        Ceil();
    };

    class Frac : public Operator1arg
    {
    public:
        Frac();
    };

    class Atan : public Operator1arg
    {
    public:
        Atan();
    };

    class Acot : public Operator1arg
    {
    public:
        Acot();
    };
    //-----------------------------------------------------------------------

    /***************************** 2ARG ******************************/
    //-----------------------------------------------------------------------
    //-----------------------------------------------------------------------
    class Min : public Operator2arg
    {
    public:
        Min();
    };
    //-----------------------------------------------------------------------

    //-----------------------------------------------------------------------
    class Max : public Operator2arg
    {
    public:
        Max();
    };
    //-----------------------------------------------------------------------
    class Dodaj : public Operator2arg
    {
    public:
        Dodaj();
    };
    //-----------------------------------------------------------------------

    //-----------------------------------------------------------------------
    class Logarytm : public Operator2arg
    {
    public:
        Logarytm();
    };
    //-----------------------------------------------------------------------

    //-----------------------------------------------------------------------
    class Odejmij : public Operator2arg
    {
    public:
        Odejmij();
    };
    //-----------------------------------------------------------------------

    //-----------------------------------------------------------------------
    class Modulo : public Operator2arg
    {
    public:
        Modulo();
    };
    //-----------------------------------------------------------------------

    //-----------------------------------------------------------------------
    class Mnoz : public Operator2arg
    {
    public:
        Mnoz();
    };
    //-----------------------------------------------------------------------

    //-----------------------------------------------------------------------
    class Potega : public Operator2arg
    {
    public:
        Potega();
    };
    //-----------------------------------------------------------------------

    //-----------------------------------------------------------------------
    class Dziel : public Operator2arg
    {
    public:
        Dziel();
    };
    //-----------------------------------------------------------------------

}; // namespace kalkulator

#endif