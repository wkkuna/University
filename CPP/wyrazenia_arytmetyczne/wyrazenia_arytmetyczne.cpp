//Wiktoria Kuna 316418
#include "wyrazenia_arytmetyczne.hpp"


//-----------------------------------------------------------------------
std::string prettify(Wyrazenie *w, int priorytet)
{
    if(w->getPrio() == -1 || priorytet == -1 || w->getPrio() >= priorytet)
        return w->opis();
    else
        return "(" + w->opis() + ")";
}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
std::vector<std::pair<std::string, double>> Zmienna::zmienne;

void Zmienna::przypisz_wartosc(std::string nazwa, double wartosc)
{

    auto wyszukana = find_if(zmienne.begin(), zmienne.end(),
                             [&nazwa](auto x) {
                                 return x.first == nazwa;
                             });

    if (wyszukana == zmienne.end())
        zmienne.emplace_back(nazwa, wartosc);
    else
        wyszukana->second = wartosc;
}

Zmienna::Zmienna(std::string nazwa) : nazwa(nazwa){}

double Zmienna::oblicz()
{
    auto wyszukana = find_if(zmienne.begin(), zmienne.end(),
                             [this](auto x) {
                                 return x.first == this->nazwa;
                             });

    if (wyszukana != zmienne.end())
        return wyszukana->second;
    else
        throw std::invalid_argument("Nie zainicjalizowana zmienna");
}

std::string Zmienna::opis(){return nazwa;}

int Zmienna::getPrio(){return priorytet;}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
Stala::Stala(std::string nazwa, double wartosc) : nazwa(nazwa), wartosc(wartosc) {}

double Stala::oblicz()  {return wartosc;}

std::string Stala::opis()   {return nazwa;}

int Stala::getPrio()    {return priorytet;}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------

Pi::Pi() : Stala("pi", M_PI) {}
E::E() : Stala("e", M_E) {}
Fi::Fi() : Stala("fi", 1.6180339887498948482) {}

//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
std::string Liczba::opis()  {return std::to_string(this->wartosc);}

double Liczba::oblicz()     {return wartosc;}

Liczba::Liczba(const double wartosc) : wartosc(wartosc) {}

int Liczba::getPrio()   {return priorytet;}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
Operator1arg::Operator1arg(Wyrazenie *w1) : w1(w1) {}
Operator1arg::Operator1arg(Wyrazenie *w1, std::function<double(double)> func) : fun(move(func)), w1(w1) {}

int Operator1arg::getPrio() { return priorytet;}

double Operator1arg::oblicz() {    return fun(w1->oblicz());}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
Sin::Sin(Wyrazenie *x) : Operator1arg(x, sin) {}

std::string Sin::opis() {return ("sin(" + w1->opis() + ")");}

int Sin::getPrio()    {return priorytet;}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
Cos::Cos(Wyrazenie *x) : Operator1arg(x, cos) {}

std::string Cos::opis() {return ("cos(" + w1->opis() + ")");}

int Cos::getPrio()    {return priorytet;}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
Ln::Ln(Wyrazenie *x) : Operator1arg(x,
                                    [](double y) {
                                            if(y<=0)
                                                throw std::invalid_argument("Logarytm nieobliczalny");
                                            return log(y); }) {}

std::string Ln::opis()  {return ("ln(" + w1->opis() + ")");}

int Ln::getPrio()    {return priorytet;}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
Bezwgl::Bezwgl(Wyrazenie *x) : Operator1arg(x, abs) {}

std::string Bezwgl::opis()  {return ("|" + w1->opis() + "|");}

int Bezwgl::getPrio()    {return priorytet;}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------

Przeciw::Przeciw(Wyrazenie *x) : Operator1arg(x, std::negate<double>()) {}

std::string Przeciw::opis() {return op + prettify(w1,priorytet+1);}

int Przeciw::getPrio()    {return priorytet;}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------

Exp::Exp(Wyrazenie *x) : Operator1arg(x, exp) {}

std::string Exp::opis()
{
    return op + prettify(w1,priorytet);
}
int Exp::getPrio()    {return priorytet;}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
Odwrot::Odwrot(Wyrazenie *x) : Operator1arg(x,
                                            [](double x) {
                                                if(x==0)
                                                    throw std::invalid_argument("Dzielenie przez zero");
                                                return 1/x; }) {}

std::string Odwrot::opis()
{
    return op + prettify(w1,priorytet-1);
}
int Odwrot::getPrio()    {return priorytet;}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
Operator2arg::Operator2arg(Wyrazenie *w1, Wyrazenie *w2) : Operator1arg(w1), w2(w2) {}

Operator2arg::Operator2arg(Wyrazenie *w1, Wyrazenie *w2, std::function<double(double, double)> fun)
    : Operator1arg(w1), fun(std::move(fun)), w2(w2) {}

double Operator2arg::oblicz()
{
    return fun(w1->oblicz(), w2->oblicz());
}
int Operator2arg::getPrio()    {return priorytet;}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
Logarytm::Logarytm(Wyrazenie *w1, Wyrazenie *w2) : Operator2arg(w1, w2,
                                                                [](double x, double y) {
                                                                    if (x <= 0 || y <= 0)
                                                                        throw std::invalid_argument("Logarytm nieobliczalny");
                                                                    return log(y) / log(x);
                                                                }) {}

std::string Logarytm::opis()
{
    return (op + "_" + "(" + w1->opis() + ")" + prettify(w2, -1));
}
int Logarytm::getPrio()    {return priorytet;}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
Dodaj::Dodaj(Wyrazenie *w1, Wyrazenie *w2) : Operator2arg(w1, w2, std::plus<double>()) {}

std::string Dodaj::opis()
{
    return prettify(w1,priorytet) + op + prettify(w2,priorytet);
}
int Dodaj::getPrio()    {return priorytet;}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
Odejmij::Odejmij(Wyrazenie *w1, Wyrazenie *w2) : Operator2arg(w1, w2, std::minus<double>()) {}

std::string Odejmij::opis()
{
    return prettify(w1,priorytet) + op + prettify(w2,priorytet+1);
}
int Odejmij::getPrio()    {return priorytet;}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
Modulo::Modulo(Wyrazenie *w1, Wyrazenie *w2) : Operator2arg(w1, w2, fmod) {}

std::string Modulo::opis()
{
    return prettify(w1,priorytet) + op + prettify(w2,priorytet);
}
int Modulo::getPrio()    {return priorytet;}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
Mnoz::Mnoz(Wyrazenie *w1, Wyrazenie *w2) : Operator2arg(w1, w2, std::multiplies<double>()) {}

std::string Mnoz::opis()
{
    return prettify(w1,priorytet) + op + prettify(w2,priorytet);
}
int Mnoz::getPrio()    {return priorytet;}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
Potega::Potega(Wyrazenie *w1, Wyrazenie *w2) : Operator2arg(w1, w2, pow) {}

std::string Potega::opis()
{
    return prettify(w1,priorytet+1) + op + prettify(w2,priorytet);
}
int Potega::getPrio()    {return priorytet;}
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
Dziel::Dziel(Wyrazenie *w1, Wyrazenie *w2) : Operator2arg(w1, w2, std::divides<double>()) {}

std::string Dziel::opis()
{
    return prettify(w1,priorytet) + op + prettify(w2,priorytet+1);
}
int Dziel::getPrio()    {return priorytet;}
//-----------------------------------------------------------------------
