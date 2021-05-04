using System;
using FluentAssertions;
using Xunit;
using strm;

namespace test
{
    public class UnitTests
    {

        [Fact] //! FAKTY
        public void Test1()
        {
            //arrange
            IntStream ints = new IntStream();
            
            //act
            int first = ints.next();
            int second = ints.next();

            Random r = new Random();
            int random = r.Next(2, 817);

            int rres = 2;

            for (int i = 2; i <= random; i++)
                rres = ints.next();

            //assert
            first.Should().Be(0);
            second.Should().Be(1);
            rres.Should().Be(random);
        }

        [Fact] //! FAKTY
        public void Test1_5()
        {
            //arrange
            IntStream ints = new IntStream();
            
            //act
            int first = ints.next();
            int second = ints.next();
            ints.reset();
            int third = ints.next();

            //assert
            first.Should().Be(0);
            second.Should().Be(1);
            third.Should().Be(0);
        }

        [Fact] //! FAKTY
        public void Test2()
        {
            //arrange
            PrimeStream ps = new PrimeStream();

            //act
            int p0 = ps.next(),
            p1 = ps.next(),
            p = 0;

            for (int i = 0; i < 100; i++)
                p = ps.next();

            int res = p;

            for (int i = 2; i < p; i++)
                if (p % i == 0)
                {
                    res = 0;
                    break;
                }

            //assert
            p0.Should().Be(2);
            p1.Should().Be(3);
            res.Should().Be(p);
        }

        [Fact] //! FAKTY
        public void Test3()
        {
            //arrange
            RandomStream rs = new RandomStream();

            //act
            int p0 = rs.next(),
            p1 = rs.next(),
            p2 = rs.next();

            //assert
            p0.Should().BeInRange(int.MinValue, int.MaxValue);
            p1.Should().BeInRange(int.MinValue, int.MaxValue);
            p2.Should().BeInRange(int.MinValue, int.MaxValue);
        }


        [Fact] //! FAKTY
        public void Test4()
        {
            //arrange
            RandomWordStream rws = new RandomWordStream();
            PrimeStream ps = new PrimeStream();

            //act
            string str0 = rws.next();
            string str1 = rws.next();
            string str2 = rws.next();

            //arrange
            str0.Length.Should().Be(ps.next());
            str1.Length.Should().Be(ps.next());
            str2.Length.Should().Be(ps.next());
        }
    }


}
