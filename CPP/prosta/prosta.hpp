#ifndef PROSTA
#define PROSTA

#include <iostream>
#include <cmath>
#include <limits>

using namespace std;

class wektor
{
private:
public:
    const double dx;
    const double dy;

    static wektor dodajWektory(const wektor &a,const wektor &b);

    wektor() = default;
    wektor(double dx, double dy);
    wektor(const wektor &vec) = delete;
    ~wektor() = default;

    void wypisz();

    wektor &operator=(const wektor&) = delete;
};

class punkt
{
private:
public:
    const double x;
    const double y;
    punkt();
    punkt(double x, double y);
    punkt(const punkt &p,const wektor &vec);
    punkt(const punkt &p) = delete;
    ~punkt() = default;
    punkt &operator=(const punkt&) = delete;

    void wypisz();

};

class prosta
{
private:
    double a;
    double b;
    double c;
    void normalise();
    double miq;

public:
    double getA()const;
    double getB()const;
    double getC()const;
    double getMiq()const;

    bool czyProst(const wektor &vec);
    bool czyRown(const wektor &vec);
    double dystans(const punkt &p);

    void wypisz();

    prosta(const prosta &a) = delete;
    prosta() = default;
    prosta(const punkt &A,const punkt &B);
    prosta(const wektor &vec);
    prosta(double A, double B, double C);
    prosta(const prosta &a,const wektor &vec);
    ~prosta() = default;

    prosta &operator=(const prosta&) = delete;
};

bool czyRownolegle(const prosta &a,const prosta &b);
bool czyProstopadle(const prosta &a,const prosta &b);
punkt przeciecia(const prosta &a,const prosta &b);

#endif // !PROSTA
