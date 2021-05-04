//Wiktoria Kuna 316418 zad 1 lista 1
#include "ex1.hpp"

int64_t str_to_int64(string str_num)
{
    string MINN = "-9223372036854775808";
    string MAXX = "9223372036854775807";

    bool neg = 0;

    if (str_num[0] == '-')
        neg = 1;

    if (str_num.size() - neg > MAXX.size() || (((!neg && str_num > MAXX) || (neg && str_num > MINN)) && str_num.size() - neg == MAXX.size()))
        throw invalid_argument("Poza zakresem");

    int64_t num = 0;
    int64_t iter = 0, sgn = 1;

    if (neg)
    {
        iter = 1;
        sgn = -1;
    }

    while (iter < (int64_t)str_num.size())
    {
        if (str_num[iter] <= '9' && str_num[iter] >= '0')
            num = num * 10 + sgn * (int64_t)(str_num[iter] - '0');
        else
            throw invalid_argument("Nie jest liczbą całkowitą");

        iter++;
    }

    return num;
}

bool is_prime(int64_t num)
{
    if (num == 1 || num == 0)
        return false;

    int64_t maxi = floor(sqrt(INT64_MAX));

    if (num == INT64_MIN)
        return false;

    if (num % 2 == 0)
        return false;

    for (int64_t i = 3; i * i <= abs(num) && i < maxi; i += 2)
        if (num % i == 0)
            return false;

    return true;
}

vector<int64_t> num_factorization(int64_t num)
{
    vector<int64_t> vec;

    if (num == 0 || num == 1)
        vec.push_back(num);

    if (num < 0)
        vec.push_back(-1);

    if (is_prime(num) == true)
    {
        vec.push_back(abs(num));
        return vec;
    }

    bool neg = 0;
    if (num < 0)
        neg = 1;

    int64_t iter = 2;
    int64_t m = ceil(sqrt((abs(num + neg))));

    while (num % iter == 0)
    {
        vec.push_back(iter);
        num /= iter;
    }

    iter++;

    while ((num > 1 || num < -1) && iter <= m)
    {
        while (num % iter == 0)
        {
            vec.push_back(iter);
            num /= iter;
        }
        iter+=2;
    }

    if (abs(num) > 1)
        vec.push_back(num);

    return vec;
}

void print(vector<int64_t> vec, int64_t k)
{
    cout << k << " = " << vec[0];
    vec.erase(vec.begin());

    for (int64_t item : vec)
        cout << " * " << item;
    cout << endl;
}

int main(int argc, char *argv[])
{
    string str;

    if (argc == 1)
        cerr << argv[0] << ": Aby użyć programu należy podać conajmniej jedną liczbę całkowitą" << endl;
    else
    {
        for (int i = 1; i < argc; i++)
        {
            str.clear();
            str = argv[i];
            try
            {
                int64_t k = str_to_int64(str);
                vector<int64_t> vec = num_factorization(k);
                print(vec, k);
            }
            catch (invalid_argument &e)
            {
                cerr << argv[1] << " " << e.what() << endl;
                return -1;
            }
        }
    }
    return 0;
}