//Wiktoria Kuna 316418
using System;
using Xunit;
using FluentAssertions;
using dictionary;

namespace dictionary_test
{
    public class dictionaryTest
    {
        [Fact]
        public void TestA()
        {
            //arrange
            var dd = new Dictionary<int, int>();

            //act
            dd.insert(1, 2);
            dd.insert(4, 8);
            dd.insert(0, 3);
            dd.insert(2, 0);
            dd.insert(9, 11);
            dd.insert(1, 10);

            //assert
            dd.find(4).Should().Be(8);
            dd.find(0).Should().Be(3);
            dd.find(9).Should().Be(11);
            dd.find(0).Should().Be(3);
            dd.find(2).Should().Be(0);

            try
            {
                dd.find(3);
                dd.find(6);
            }
            catch (Exception e)
            {
                e.Message.Should().Be("Element with given key not found");
            }

        }
        [Fact]
        public void TestB()
        {
            //arrange
            var dd = new Dictionary<int, string>();

            //act
            dd.insert(3, "abc");
            dd.insert(1, "bac");
            dd.insert(6, "acb");
            dd.insert(2, "aaa");

            //assert
            dd.find(2).Should().Be("aaa");
            dd.find(1).Should().Be("bac");
            dd.find(6).Should().Be("acb");
            dd.find(3).Should().Be("abc");

            try
            {
                dd.find(10);
                dd.find(0);
            }
            catch (Exception e)
            {
                e.Message.Should().Be("Element with given key not found");
            }
        }
        [Fact]
        public void TestC()
        {
            //arrange
            var dd = new Dictionary<string, float>();

            //act
            dd.insert("a", 1.32f);
            dd.insert("ad", 3.4f);
            dd.insert("asmd", 9.0002f);
            dd.insert("lsd", 32.32f);

            //assert
            dd.find("a").Should().Be(1.32f);
            dd.find("ad").Should().Be(3.4f);
            dd.find("asmd").Should().Be(9.0002f);
            dd.find("lsd").Should().Be(32.32f);

            try
            {
                dd.find("b");
                dd.find("cat");
                dd.find("pleaseLetMyOutIDontWannaStayHomeAnymore");
            }
            catch (Exception e)
            {
                e.Message.Should().Be("Element with given key not found");
            }
        }
        [Fact]
        public void deleteCheck()
        {
            //arrange
            var dd = new Dictionary<int, char>();

            //act 

            dd.insert(1, 'c');
            dd.insert(2, 'c');
            dd.insert(3, 'c');
            dd.insert(4, 'c');
            dd.insert(5, 'c');
            dd.insert(6, 'c');

            dd.delete(3);
            dd.delete(1);
            dd.delete(6);

            //assert

            try
            {
                dd.find(3);
                dd.find(1);
                dd.find(6);
            }
            catch (Exception e)
            {
                e.Message.Should().Be("Element with given key not found");
            }
        }
    }
}
