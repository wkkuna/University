//Wiktoria Kuna 316418
#include <iostream>
#include <vector>
#include <string>
#include <exception>

using namespace std;

const vector<pair<int, string>> rzym =
    {{1000, "M"}, {900, "CM"}, {500, "D"}, {400, "CD"}, {100, "C"}, {90, "XC"}, 
    {50, "L"}, {40, "XL"}, {10, "X"}, {9, "IX"}, {5, "V"}, {4, "IV"}, {1, "I"}};

string bin2rom(int x)
{
    string romNum;

    int j = 0;
    while (x > 0)
    {
        while (x - rzym[j].first >= 0)
        {
            x -= rzym[j].first;
            romNum += rzym[j].second;
        }
        j++;
    }
    return romNum;
}

bool isNumber(string x)
{
    for (auto e : x)
        if (e > '9' || e < '0')
            return false;

    return true;
}

bool inRange(int x){return x >= 1 and x <= 3999;}

int main(int argc, char **argv)
{
    if (argc == 1)
        throw invalid_argument("Run program with at least one parameter");

    for (int i = 1; i < argc; i++)
        if (isNumber(argv[i]))
        {
            try
            {
                if (inRange(stoi(argv[i])))
                {
                    string str = bin2rom(stoi(argv[i]));
                    cout << str << endl;
                }
            }
            catch (const std::exception &e){}
        }
}
