//Wiktoria Kuna 316418
#include "kalkulator.hpp"

using namespace kalkulator;

int main()
{
    std::cout << "Wpisz \"print <wyrazenieONP> \", aby obliczyc wyrazenie i wypisać jego wynik.\n";
    std::cout << "Wpisz \"assign <wyrazenieONP> to <zmienna> \", aby przypisać wyrazenie do zmiennej.\n";
    std::cout << "Wpisz \"clear\", aby wyczyscic zapamietane zmienne.\n";
    std::cout << "Wpisz \"exit\", aby wyjsc z programu.\n";

    auto zbior = Zmienna();

    while (1)
    {
        std::string in, cmd;

        std::getline(std::cin, in);
        std::istringstream instream{in};

        std::getline(instream, cmd, ' ');

        if (cmd == "print")
        {
            std::vector<std::string> op1;
            std::string arg;

            while (std::getline(instream, arg, ' '))
                op1.push_back(arg);

            auto x = ONP(op1);
            std::cout << x.oblicz() << std::endl;
        }

        else if (cmd == "assign")
        {
            std::vector<std::string> op1;
            std::string arg, op2, rest;
            std::getline(instream, arg, ' ');

            while (arg != "to")
            {
                op1.push_back(arg);
                if (!std::getline(instream, arg, ' '))
                    break;
            }

            std::getline(instream, op2, ' ');
            std::getline(instream, rest);

            if (!isLegal(op2) && !isNum(op2))
                std::clog << "Nieprawidlowa skladnia (ASSIGN: Nieprawidlowa nazwa dla zmiennej): " << op2 << std::endl;

            else if (op2 == "" || rest != "")
                std::clog << "Nieprawidlowa skladnia (ASSIGN: Nieprawidlowa ilosc argumentow)\n";

            else
                zbior.przypisz(op2, ONP(op1).oblicz());
        }

        else if (cmd == "clear")
        {
            std::string rest;
            std::getline(instream, rest);

            if (rest != "")
                std::clog << "Nieprawidlowa skladnia (CLEAR: Nieprawidlowa ilosc argumentow)\n";

            zbior.wyczysc();
        }

        else if (cmd == "exit")
        {
            std::string rest;
            std::getline(instream, rest);

            if (rest != "")
                std::clog << "Nieprawidlowa skladnia (EXIT: Nieprawidlowa ilosc argumentow)\n";
            else
                return 0;
        }

        else
            std::clog << "Nieznana komenda: " << cmd << std::endl;
    }
}