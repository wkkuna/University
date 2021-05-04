using System;
using Xunit;
using strm;
using FluentAssertions;

namespace test
{
    public class UnitTest1
    {
        [Fact]
        public void Test1()
        {
            var pm = new PrimeCollection();

            bool IsPrime(int x)
            {
                if (x == 2)
                    return true;

                if (x % 2 == 0)
                    return false;

                for (int i = 3; i <= Math.Sqrt(x); i += 2)
                    if (x % i == 0)
                        return false;

                return true;
            }

            foreach (var p in pm)
            {
                IsPrime((int)p).Should().Be(true);
                if ((int)p > 100000)
                    break;
            }
        }

        [Fact]
        public void Test2()
        {
            var pm = new PrimeCollection();

            var p = pm.GetEnumerator();

            var x = p.Current;
            p.MoveNext();
            var y = p.Current;
            var z = p.Current;
            p.Reset();
            var w = p.Current;

            x.Should().Be(2);
            y.Should().Be(3);
            z.Should().Be(y);
            w.Should().Be(x);
        }
    }
}
