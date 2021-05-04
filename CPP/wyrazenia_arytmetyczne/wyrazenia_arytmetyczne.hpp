//Wiktoria Kuna 316418
#ifndef WYRAZENIA_ARYTMETYCZNE
#define WYRAZENIA_ARYTMETYCZNE

#include <iostream>
#include <string>
#include <vector>
#include <functional>
#include <cmath>
#include <algorithm>
#include <stdexcept>

//-----------------------------------------------------------------------
class Wyrazenie
{
public:
    virtual int getPrio() = 0;
    virtual double oblicz() = 0;
    virtual std::string opis() = 0;
};
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
std::string prettify(Wyrazenie *w, int priorytet);

//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
class Zmienna : public virtual Wyrazenie
{
protected:
    const int priorytet = -1;
    std::string nazwa;
    static std::vector<std::pair<std::string, double>> zmienne;

public:
    static void przypisz_wartosc(std::string nazwa, double wartosc);

    Zmienna(std::string nazwa);

    int getPrio() override;
    double oblicz() override;
    std::string opis() override;
};
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
class Stala : public virtual Wyrazenie
{
protected:
    const int priorytet = -1;
    const std::string nazwa;
    const double wartosc;

public:
    Stala(std::string nazwa, double wartosc);

    int getPrio() override;
    double oblicz() override;
    std::string opis() override;
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
class Liczba : public virtual Wyrazenie
{
protected:
    const int priorytet = -1;
    const double wartosc;

public:
    Liczba(const double wartosc);

    int getPrio() override;
    double oblicz() override;
    std::string opis() override;
};
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
class Operator1arg : public virtual Wyrazenie
{
private:
    std::function<double(double)> fun;

protected:
    const int priorytet = 0;
    std::string op;
    Wyrazenie *w1;

public:
    Operator1arg(Wyrazenie *w1);
    Operator1arg(Wyrazenie *w1, std::function<double(double)> fun);

    int getPrio() override;
    double oblicz() override;
    std::string opis() override { return ""; };
};
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
class Sin : public Operator1arg
{
protected:
    const int priorytet = -1;

public:
    int getPrio() override;
    Sin(Wyrazenie *x);
    std::string opis() override;
};
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
class Cos : public Operator1arg
{
protected:
    const int priorytet = -1;

public:
    int getPrio() override;
    Cos(Wyrazenie *x);
    std::string opis() override;
};
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
class Bezwgl : public Operator1arg
{
protected:
    const int priorytet = -1;

public:
    int getPrio() override;
    Bezwgl(Wyrazenie *x);
    std::string opis() override;
};
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
class Przeciw : public Operator1arg
{
protected:
    std::string op = "-";
    const int priorytet = 5;

public:
    int getPrio() override;
    Przeciw(Wyrazenie *x);
    std::string opis() override;
};
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
class Exp : public Operator1arg
{
protected:
    std::string op = "e^";
    const int priorytet = 15;

public:
    int getPrio() override;
    Exp(Wyrazenie *x);
    std::string opis() override;
};
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
class Odwrot : public Operator1arg
{
protected:
    std::string op = "1/";
    const int priorytet = 10;

public:
    int getPrio() override;
    Odwrot(Wyrazenie *x);
    std::string opis() override;
};
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
class Ln : public Operator1arg
{
protected:
    std::string op = "ln";
    const int priorytet = 15;

public:
    int getPrio() override;
    Ln(Wyrazenie *x);
    std::string opis() override;
};
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
class Operator2arg : public Operator1arg
{
private:
    std::function<double(double, double)> fun;

protected:
    std::string op;
    Wyrazenie *w2;

public:
    Operator2arg(Wyrazenie *w1, Wyrazenie *w2);
    Operator2arg(Wyrazenie *w1, Wyrazenie *w2, std::function<double(double, double)> fun);

    int getPrio() override;
    double oblicz() override;
    std::string opis() override { return ""; };
};
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
class Dodaj : public Operator2arg
{
protected:
    std::string op = "+";
    const int priorytet = 5;

public:
    int getPrio() override;
    Dodaj(Wyrazenie *w1, Wyrazenie *w2);
    std::string opis() override;
};
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
class Logarytm : public Operator2arg
{
protected:
    const int priorytet = 15;
    std::string op = "log";

public:
    int getPrio() override;
    Logarytm(Wyrazenie *w1, Wyrazenie *w2);
    std::string opis() override;
};
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
class Odejmij : public Operator2arg
{
protected:
    std::string op = "-";
    const int priorytet = 5;

public:
    int getPrio() override;
    Odejmij(Wyrazenie *w1, Wyrazenie *w2);
    std::string opis() override;
};
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
class Modulo : public Operator2arg
{
protected:
    std::string op = "%";
    const int priorytet = 10;

public:
    int getPrio() override;
    Modulo(Wyrazenie *w1, Wyrazenie *w2);
    std::string opis() override;
};
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
class Mnoz : public Operator2arg
{
public:
    std::string op = "*";
    const int priorytet = 10;

public:
    int getPrio() override;
    Mnoz(Wyrazenie *w1, Wyrazenie *w2);
    std::string opis() override;
};
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
class Potega : public Operator2arg
{
protected:
    std::string op = "^";
    const int priorytet = 15;

public:
    int getPrio() override;
    Potega(Wyrazenie *w1, Wyrazenie *w2);
    std::string opis() override;
};
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
class Dziel : public Operator2arg
{
protected:
    std::string op = "/";
    const int priorytet = 10;

public:
    int getPrio() override;
    Dziel(Wyrazenie *w1, Wyrazenie *w2);
    std::string opis() override;
};
//-----------------------------------------------------------------------

#endif