//Wiktoria Kuna 316418

using System;
using System.Collections;
namespace strm
{
    public class PrimeCollection : IEnumerable
    {
        IEnumerator IEnumerable.GetEnumerator()
        {
            return (IEnumerator)GetEnumerator();
        }

        public PrimeCollectionEnum GetEnumerator()
        {
            return new PrimeCollectionEnum();
        }
    }

    public class PrimeCollectionEnum : IEnumerator
    {
        int currentNumber = 2;
        readonly int Int32MaxPrime = 214748357;
        public bool eos() => currentNumber >= Int32MaxPrime;
        bool isInt32Prime(int x)
        {
            if (x >= Int32MaxPrime || x < 2)
                return false;

            if (x == 2)
                return true;

            if (x % 2 == 0)
                return false;

            for (int i = 3; i <= Math.Sqrt(x); i += 2)
                if (x % i == 0)
                    return false;

            return true;
        }

        int primeInt32Search(int x)
        {
            while (!isInt32Prime(x++)) ;
            x--;

            if(!eos())
                return x;
            else 
                return currentNumber;
        }

        public object Current 
        {
            get
            {
                return currentNumber;
            }
        } 

        public bool MoveNext()
        {
            currentNumber++;
            currentNumber = primeInt32Search(currentNumber);
            return currentNumber <= Int32MaxPrime; 
        }

        public void Reset() => currentNumber = 2;
    }
}

