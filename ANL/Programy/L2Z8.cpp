#include <iostream>
#include <cmath>
typedef double TYPE;
using namespace std;

TYPE bad(TYPE x)
{
    return (4040.0 * (sqrt((pow(x, 11) + 1.0)) - 1.0)) / pow(x, 11);
}

TYPE bit_better(TYPE x)
{
    return (4040.0/(sqrt(pow(x,11)+1.0)+1.0));
}


int main()
{
    int N = 10;
    // cout.precision(ios::scientific);
    

    TYPE x = 100.0;
    int k = 2;
    while(x > 0.000000000001)
    {
        cout << "10^("<< k << "): Przed: " << bad(x) << " Po: " << bit_better(x) << endl;
        x /=N;
        k--;
    }
    
}
