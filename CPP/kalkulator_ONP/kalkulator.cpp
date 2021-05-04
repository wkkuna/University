//Wiktoria Kuna 316418
#include "kalkulator.hpp"

namespace kalkulator
{
    /****************************** INNE ******************************/
    /******************************************************************/
    template <typename Base, typename T>
    inline bool instanceof (const T *)
    {
        return std::is_base_of<Base, T>::value;
    }

    static const std::vector<std::pair<int, std::string>> funAssoc = {{1, "abs"}, {2, "sgn"}, {3, "floor"}, {4, "ceil"}, {5, "frac"}, {6, "sin"}, {7, "cos"}, {8, "atan"}, {9, "acot"}, {10, "ln"}, {11, "exp"}, {12, "modulo"}, {13, "min"}, {14, "max"}, {15, "log"}, {16, "pow"}, {17, "+"}, {18, "-"}, {19, "/"}, {20, "*"}};

    bool isLegal(std::string name)
    {
        if (name.length() > 7)
            return false;
        std::vector<std::string> illegal = {"abs", "modulo", "min", "max", "log", "pow", "sgn", "floor", "ceil", "frac",
                                            "sin", "cos", "atan", "acot", "ln", "exp", "e", "pi", "fi", "+", "-",
                                            "*", "/", "%", "to", "print", "assign", "clear", "exit", "."};

        for (auto x : illegal)
            if (name == x)
                return false;

        return true;
    }
    bool isConst(std::string name)
    {
        std::vector<std::string> consts = {"pi", "e", "fi"};

        for (auto x : consts)
            if (name == x)
                return true;

        return false;
    }

    bool isNum(std::string nazwa)
    {
        int iter = 0, len = nazwa.length();

        if ((nazwa[0] == '-' || nazwa[0] == '.') && len == 1)
            return false;

        for (auto x : nazwa)
        {
            if (!((x <= '9' && x >= '0') || x == '.' && iter < len - 1 || x == '-' && iter == 0))
                return false;
            iter++;
        }
        return true;
    }

    int isFunction(std::string nazwa)
    {
        for (auto x : funAssoc)
            if (nazwa == x.second)
                return x.first;

        return 0;
    }

    /**************************** OPERANDY ****************************/
    /******************************************************************/
    std::map<std::string, double> Zmienna::zmienne;

    /************************** KONSTRUKTORY **************************/
    Zmienna::Zmienna(std::string nazwa, double wartosc) : nazwa(nazwa)
    {
        przypisz(nazwa, wartosc);
    }

    Zmienna::Zmienna(std::string nazwa) : nazwa(nazwa) {}

    Stala::Stala(std::string nazwa, double wartosc) : nazwa(nazwa), wartosc(wartosc) {}
    Pi::Pi() : Stala("pi", M_PI) {}
    E::E() : Stala("e", M_E) {}
    Fi::Fi() : Stala("fi", 1.6180339887498948482) {}
    Liczba::Liczba(const double wartosc) : wartosc(wartosc) {}

    /*************************** OBLICZANIE ***************************/
    double Zmienna::oblicz()
    {
        double return_val;
        try
        {
            return_val = zmienne.at(this->nazwa);
        }
        catch (const std::exception &e)
        {
            std::clog << "Niezainicjalizowana zmienna \n";
            return 0;
        }

        return return_val;
    }
    double Stala::oblicz() { return wartosc; }
    double Liczba::oblicz() { return wartosc; }
    double Zmienna::oblicz(std::stack<double> *env)
    {
        auto x = this->oblicz();
        env->push(x);
        return x;
    }

    double Stala::oblicz(std::stack<double> *env)
    {
        auto x = this->oblicz();
        env->push(x);
        return x;
    }

    double Liczba::oblicz(std::stack<double> *env)
    {
        auto x = this->oblicz();
        env->push(x);
        return x;
    }

    void Zmienna::przypisz(std::string nazwa, double wartosc)
    {
        auto wyszukana = find_if(zmienne.begin(), zmienne.end(),
                                 [&nazwa](auto x) {
                                     return x.first == nazwa;
                                 });

        if (wyszukana == zmienne.end())
            zmienne.insert(std::pair<std::string, double>(nazwa, wartosc));
        else
            wyszukana->second = wartosc;
    }

    void Zmienna::wyczysc()
    {
        zmienne.clear();
    }
    /**************************** FUNKCJE *****************************/
    /******************************************************************/

    /************************** KONSTRUKTORY **************************/

    Operator1arg::Operator1arg(std::function<double(double)> func) : fun(std::move(func)) {}
    Operator2arg::Operator2arg(std::function<double(double, double)> func) : fun(std::move(func)) {}

    Sin::Sin() : Operator1arg(sin) {}
    Cos::Cos() : Operator1arg(cos) {}
    Atan::Atan() : Operator1arg(atan) {}
    Acot::Acot() : Operator1arg([](double x) { return atan(1 / x); }) {}
    Bezwgl::Bezwgl() : Operator1arg(abs) {}
    Floor::Floor() : Operator1arg(floor) {}
    Ceil::Ceil() : Operator1arg(ceil) {}
    Sgn::Sgn() : Operator1arg([](double x) {
                     if (x < 0)
                         return -1;
                     else if (x > 0)
                         return 1;
                     else
                         return 0;
                 }) {}
    Exp::Exp() : Operator1arg(exp) {}
    Frac::Frac() : Operator1arg([](double x) { return 1 / x; }) {}
    Ln::Ln() : Operator1arg([](double y) {
                                if(y<=0)
                                    std::clog << "Logarytm nieobliczalny";
                                return log(y); }) {}

    Min::Min() : Operator2arg([](double x, double y) { return x < y ? x : y; }) {}

    Max::Max() : Operator2arg([](double x, double y) { return y < x ? x : y; }) {}

    Dodaj::Dodaj() : Operator2arg(std::plus<double>()) {}
    Logarytm::Logarytm() : Operator2arg([](double x, double y) {
                                            if (x <= 0 || y <= 0)
                                                std::clog << "Logarytm nieobliczalny";
                                            return log(y) / log(x); }) {}

    Odejmij::Odejmij() : Operator2arg(std::minus<double>()) {}
    Modulo::Modulo() : Operator2arg(fmod) {}
    Mnoz::Mnoz() : Operator2arg(std::multiplies<double>()) {}
    Potega::Potega() : Operator2arg(pow) {}
    Dziel::Dziel() : Operator2arg(std::divides<double>()) {}
    /*************************** OBLICZANIE ***************************/

    double Operator1arg::oblicz(std::stack<double> *env)
    {
        if (env->empty())
            throw std::invalid_argument("Niepoprawne wyrażenie ONP");

        auto val = env->top();
        env->pop();

        auto evaluated = fun(val);
        env->push(evaluated);
        return evaluated;
    }

    double Operator2arg::oblicz(std::stack<double> *env)
    {
        if (env->empty())
            throw std::invalid_argument("Niepoprawne wyrażenie ONP");
        auto val1 = env->top();
        env->pop();
        if (env->empty())
            throw std::invalid_argument("Niepoprawne wyrażenie ONP");
        auto val2 = env->top();
        env->pop();

        auto evaluated = fun(val1, val2);
        env->push(evaluated);
        return evaluated;
    }

    /*************************** WYRAŻENIE ****************************/
    /******************************************************************/

    ONP::ONP(std::vector<std::string> list)
    {
        for (auto x : list)
        {
            int idx = isFunction(x);

            // Stala
            if (isConst(x))
            {
                if (x == "pi")
                    Wyr.push_back(new Pi());
                else if (x == "fi")
                    Wyr.push_back(new Fi());
                else if (x == "e")
                    Wyr.push_back(new E());
            }

            // Liczba
            else if (isNum(x))
            {
                Wyr.push_back(new Liczba(stod(x)));
            }

            // Zmienna
            else if (idx == 0)
            {
                Wyr.push_back(new Zmienna(x));
            }

            // Funkcja
            else
            {
                switch (idx)
                {
                case 1:
                    Wyr.push_back(new Bezwgl());
                    break;
                case 2:
                    Wyr.push_back(new Sgn());
                    break;
                case 3:
                    Wyr.push_back(new Floor());
                    break;
                case 4:
                    Wyr.push_back(new Ceil());
                    break;
                case 5:
                    Wyr.push_back(new Frac());
                    break;
                case 6:
                    Wyr.push_back(new Sin());
                    break;
                case 7:
                    Wyr.push_back(new Cos());
                    break;
                case 8:
                    Wyr.push_back(new Atan());
                    break;
                case 9:
                    Wyr.push_back(new Acot());
                    break;
                case 10:
                    Wyr.push_back(new Ln());
                    break;
                case 11:
                    Wyr.push_back(new Exp());
                    break;
                case 12:
                    Wyr.push_back(new Modulo());
                    break;
                case 13:
                    Wyr.push_back(new Min());
                    break;
                case 14:
                    Wyr.push_back(new Max());
                    break;
                case 15:
                    Wyr.push_back(new Logarytm());
                    break;
                case 16:
                    Wyr.push_back(new Potega());
                    break;
                case 17:
                    Wyr.push_back(new Dodaj());
                    break;
                case 18:
                    Wyr.push_back(new Odejmij());
                    break;
                case 19:
                    Wyr.push_back(new Dziel());
                    break;
                case 20:
                    Wyr.push_back(new Mnoz());
                    break;
                default:
                    std::clog << "Nieznana operacja: " << x << std::endl;
                }
            }
        }
    }

    double ONP::oblicz()
    {
        auto env = new std::stack<double>();

        for (Wyrazenie *x : Wyr)
        {
            try
            {
                x->oblicz(env);
            }
            catch (const std::exception &e)
            {
                std::clog << e.what() << std::endl;
                return 0;
            }
        }

        if (env->size() != 1)
        {
            std::clog << "Niepoprawne wyrażenie ONP" << std::endl;
            return 0;
        }
        return env->top();
    }
}; // namespace kalkulator