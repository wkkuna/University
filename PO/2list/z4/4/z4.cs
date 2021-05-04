//Wiktoria Kuna 316418

//Ponieważ w zadaniu napisane było, że należy zaimplementować listę "kolejnych liczb całkowitych", której
//elementami mają być "losowe liczby całkowite", zdecydowałam się wybrać niestety tylko jedno z obu wymagań,
//ale przeimplementowanie na kolejne liczby całkowite nie byłoby bardzo skomplikowane.

using System;
using System.Collections.Generic;
using strm;

namespace z2
{

    public class LazyList
    {
        protected IntStream myStream = new RandomStream();
        protected List<int> LL = new List<int> { };
        public int size() => LL.Count;

        public LazyList() => this.myStream = new RandomStream();

        public int element(int idx)
        {
            for (int i = size(); i < idx; i++)
                LL.Add(myStream.next());

            return LL[idx - 1];
        }
    }

    public class Prime : LazyList
    {
        public Prime() => this.myStream = new PrimeStream();
    }

}

