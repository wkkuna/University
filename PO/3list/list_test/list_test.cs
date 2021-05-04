//Wiktoria Kuna 316418
using System;
using Xunit;
using FluentAssertions;
using list;

namespace list_test
{
    public class List_Test
    {
        [Fact]
        public void EmptyTest()
        {
            var ii = new List<int>();

            try
            {
                ii.popFront();
                ii.popFront();
            }
            catch (Exception e)
            {
                e.Message.Should().Be("The list is empty");
            }
        }

        [Fact]
        public void FrontTest()
        {
            //arrange
            var ii = new List<int>();
            var db = new List<double>();
            var str = new List<string>();

            //act
            ii.pushFront(1);
            var a = ii.popFront();
            
            ii.pushFront(1);
            ii.pushFront(2);
            var b = ii.popFront();

            db.pushFront(1.33);
            var c = db.popFront();

            db.pushFront(1.1);
            db.pushFront(2.90);
            var d = db.popFront();

            str.pushFront("IWantOut");
            var e = str.popFront();
            
            str.pushFront("A");
            str.pushFront("ToLiveMyLifeAlone");
            var f = str.popFront();

            //assert

            a.Should().Be(1);
            b.Should().Be(2);
            c.Should().Be(1.33);
            d.Should().Be(2.90);
            e.Should().Be("IWantOut");
            f.Should().Be("ToLiveMyLifeAlone");
        }

        [Fact]
        public void BackTest()
        {
            //arrange
            var ii = new List<int>();
            var db = new List<double>();
            var str = new List<string>();

            //act
            ii.pushBack(1);
            var a = ii.popBack();
            
            ii.pushBack(1);
            ii.pushBack(2);
            var b = ii.popBack();

            db.pushBack(1.33);
            var c = db.popBack();

            db.pushBack(1.1);
            db.pushBack(2.90);
            var d = db.popBack();

            str.pushBack("ShowMustGoOn");
            var e = str.popBack();
            
            str.pushBack("A");
            str.pushBack("...ButMySmileStillStaysOn");
            var f = str.popBack();


            //assert
            a.Should().Be(1);
            b.Should().Be(2);
            c.Should().Be(1.33);
            d.Should().Be(2.90);
            e.Should().Be("ShowMustGoOn");
            f.Should().Be("...ButMySmileStillStaysOn");
        }
    }
}
