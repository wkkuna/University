//Wiktoria Kuna 316418

using System;

namespace strm
{
    public class IntStream
    {
        protected int currentNumber = 0;

        virtual public bool eos() => currentNumber == Int32.MaxValue;

        virtual public int next() => eos() ? currentNumber : currentNumber++;

        public void reset() => currentNumber = 0;
    }

    public class PrimeStream : IntStream
    {
        readonly int Int32MaxPrime = 214748357;

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
        override public int next()
        {
            currentNumber = primeInt32Search(currentNumber);
            return currentNumber++;
        }

        override public bool eos() => currentNumber >= Int32MaxPrime;
    }

    public class RandomStream : IntStream
    {
        override public bool eos() => false;

        Random rand = new Random();

        override public int next() => rand.Next();
    }

    public class RandomWordStream
    {
        PrimeStream ps = new PrimeStream();
        RandomStream rs = new RandomStream();

        public string next()
        {
            string randStr = "";
            int strLen = ps.next();

            for (int i = 0; i < strLen; i++)
            {
                int randChar = rs.next() % 126;

                while (randChar < 33)
                    randChar = rs.next() % 126;

                randStr += (char)randChar;
            }

            return randStr;
        }
    }

}