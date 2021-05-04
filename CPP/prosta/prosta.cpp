#include "prosta.hpp"

wektor::wektor(double x, double y) : dx(x), dy(y)
{
}

wektor wektor::dodajWektory(const wektor &a,const wektor &b)
{
    return wektor(a.dx + b.dx, a.dy + b.dy);
}

punkt::punkt(double x, double y) : x(x), y(y) {}

punkt::punkt(const punkt &p,const wektor &vec) : x(p.x + vec.dx), y(p.y + vec.dy) {}

double prosta::getA()const { return a; }
double prosta::getB()const { return b; }
double prosta::getC()const { return c; }
double prosta::getMiq()const { return miq; }

double mi(double A, double B, double C)
{
    double mi = 1 / sqrt(A * A + B * B);

    if (C > 0)
        return -1 * mi;
    else
        return mi;
}

void prosta::normalise()
{
    miq = mi(a, b, c);

    a *= miq;
    b *= miq;
    c *= miq;
}

prosta::prosta(const punkt &A,const punkt &B)
{
    if (abs(A.x - B.x) < numeric_limits<double>::epsilon() && abs(A.y - B.y) < numeric_limits<double>::epsilon())
        throw invalid_argument("Nie można jednoznacznie utworzyć prostej");

    a = A.y - B.y;
    b = -A.x + B.x;
    c = A.y * (A.x - B.x) - (A.y - B.y) * A.x;

    if (abs(a + b) < numeric_limits<double>::epsilon())
        throw invalid_argument("Nie można jednoznacznie utworzyć prostej");
    this->normalise();
}

prosta::prosta(const wektor &vec)
{
    a = vec.dx;
    b = vec.dy;
    c = -vec.dx * vec.dx - vec.dy * vec.dy;

    if (fabs(a + b) < numeric_limits<double>::epsilon())
        throw invalid_argument("Nie można jednoznacznie utworzyć prostej");
    this->normalise();
}

prosta::prosta(double A, double B, double C)
{
    if (fabs(A + B) < numeric_limits<double>::epsilon())
        throw invalid_argument("Nie można jednoznacznie utworzyć prostej");
    c = C;
    a = A;
    b = B;
    this->normalise();
}

prosta::prosta(const prosta &a,const wektor &vec) : prosta(a.a / a.miq, a.b / a.miq, (a.c - vec.dy * a.miq - a.a * a.miq * vec.dx / a.b) / a.miq)
{
}

bool prosta::czyProst(const wektor &vec)
{
    return abs(this->a - vec.dx * this->miq) < numeric_limits<double>::epsilon() and
           abs(this->b - vec.dy * this->miq) < numeric_limits<double>::epsilon();
}

//const wektor&
bool prosta::czyRown(const wektor &vec)
{
    return abs(vec.dx - 1) < numeric_limits<double>::epsilon() and
           abs(vec.dy / this->miq + this->a * this->b) < numeric_limits<double>::epsilon();
}

double prosta::dystans(const punkt &p)
{
    double a = this->a / miq;
    double b = this->b / miq;
    double c = this->c / miq;

    return (abs(a * p.x + b + p.y + c)) / sqrt(a * a + b * b);
}

bool czyRownolegle(const prosta &a,const prosta &b)
{
    return abs(a.getA() / a.getB() - b.getA() / b.getB()) < numeric_limits<double>::epsilon();
}

bool czyProstopadle(const prosta &a,const prosta &b)
{
    return abs(a.getA() / a.getB() * b.getB() / b.getA() + 1) < numeric_limits<double>::epsilon();
}

punkt przeciecia(const prosta &a,const prosta &b)
{
    double W = a.getA() / a.getMiq() * b.getB() / b.getMiq() - b.getA() / b.getMiq() * a.getB() / a.getMiq();

    if (W < numeric_limits<double>::epsilon())
        throw invalid_argument("Proste się nie przecinają");

    double Wx = -a.getC() / a.getMiq() * b.getB() / b.getMiq() + b.getC() / b.getMiq() * a.getB() / a.getMiq();
    double Wy = -a.getA() / a.getMiq() * b.getC() / b.getMiq() + b.getA() / b.getMiq() * a.getC() / a.getMiq();

    return punkt(Wx / W, Wy / W);
}

void punkt::wypisz()
{
    cout << "(" << this->x << ", " << this->y << ")" << endl;
}

void wektor::wypisz()
{
    cout << "[" << this->dx << "," << this->dy << "]" << endl;
}

void prosta::wypisz()
{
    cout << this->getA() << "x " << this->getB() << "y " << this->getC() << endl;
}