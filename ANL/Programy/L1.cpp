#include <iostream>
#include <cmath>
typedef float TYPE;
using namespace std;

double ex1(double x)
{
    return (4040 * (sqrt((pow(x, 11) + 1)) - 1)) / pow(x, 11);
}

double ex1b(double x)
{
    return 4040 / (sqrt(pow(x, 11) + 1) + 1);
}

TYPE ex2(TYPE x)
{
    return (TYPE)((TYPE)12120 * (TYPE)((TYPE)x - (TYPE)sin((TYPE)x)) / (TYPE)pow((TYPE)x, (TYPE)3));
}

float ex3(int n)
{
    float y[51];
    y[0] = 1.0;
    y[1] = -1.0 / 7.0;
    for (int i = 2; i <= n; i++)
    {
        y[i] = 1.0 / 7.0 * (69.0 * y[i - 1] + 10.0 * y[i - 2]);
        cout << i << ": " << y[i]<<endl;
    }
    return y[n];
}

TYPE ex4(int n)
{
    TYPE tab[21];
    tab[0]=(TYPE)log((TYPE)2021/(TYPE)2020);

    cout << "0: "<< tab[0] << endl;

    for(int i=1; i<=n; i++)
    {
        tab[i] = (TYPE)1/(TYPE)i - (TYPE)2020*(TYPE)tab[i-1];
        cout << i << ": "<< tab[i] <<endl;
    }

    return (TYPE)tab[n];
}

TYPE ex5()
{
    TYPE y = 0, yy = 0;
    unsigned int k = 0;
    while (true)
    {
        y += 4*(TYPE)pow(-1, k) / (TYPE)((TYPE)2 * (TYPE)k + (TYPE)1);

        if (abs(yy - y) < (TYPE)pow(10, -4))
        {
            break;
        }
        yy = y;
        k += 1;
    }
    return k;
}

int main()
{
    // cout<<ex1(0.001) << " " <<ex1b(0.001);
    cout.precision(ios::scientific);
    // for (int i = 11; i <= 20; i++)
    // {
    //     cout << i<< ": " << ex2((TYPE)pow(10, -i)) << endl;
    // }

    cout << ex5();
}

/* ex7
    def anyATG(x)
        if -1 <= x && x <= 1
            ATG(x)
        elsif x > 1
            2 * ATG(1) - ATG(1/x)
        else
            -2 * ATG(1) - ATG(1/x)
        end
    end
*/