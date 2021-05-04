using System;
using Xunit;
using FluentAssertions;
using z2;

namespace test
{
    public class UnitTest
    {
        [Fact] //!Fakty
        public void Test1()
        {
            //arrange
            LazyList example = new LazyList();

            //act 
            var size0 = example.size();

            var el20 = example.element(20);
            var size1 = example.size();

            example.element(38);
            var size2 = example.size();

            example.element(100);
            var size3 = example.size();

            var el20v2 = example.element(20);

            //assert
            size0.Should().Be(0);
            size1.Should().Be(20);
            size2.Should().Be(38);
            size3.Should().Be(100);

            el20v2.Should().Be(el20);
        }

        [Fact] //!Fakty
        public void Test2()
        {
            //arrange
            Prime example = new Prime();

            //kth prime number
            int kthPrimeNumber(int k)
            {
                int NOTpirme = 0;
                int iterator = 0;
                int currentNum = 0;

                while (iterator - NOTpirme < k)
                {
                    if (currentNum < 2 || (currentNum % 2 == 0 && currentNum != 2))
                        NOTpirme++;
                    else
                        for (int i = 3; i <= Math.Sqrt(currentNum); i += 2)
                            if (currentNum % i == 0)
                            {
                                NOTpirme++;
                                break;
                            }

                    iterator++;
                    currentNum++;
                }

                return --currentNum;
            }

            //act
            var size0 = example.size();

            var el42 = example.element(42);
            var size1 = example.size();

            var el3 = example.element(3);
            var size2 = example.size();

            var el33 = example.element(33);
            var size3 = example.size();

            var el100 = example.element(100);
            var size4 = example.size();

            var el3v2 = example.element(3);
            var size5 = example.size();

            //assert

            size0.Should().Be(0);
            size1.Should().Be(42);
            size2.Should().Be(42);
            size3.Should().Be(42);
            size4.Should().Be(100);
            size5.Should().Be(100);

            el42.Should().Be(kthPrimeNumber(42));
            el3.Should().Be(kthPrimeNumber(3));
            el33.Should().Be(kthPrimeNumber(33));
            el100.Should().Be(kthPrimeNumber(100));
            el3v2.Should().Be(kthPrimeNumber(3));

        }
    }
}
