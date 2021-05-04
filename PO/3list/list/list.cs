//Wiktoria Kuna 316418
using System;

namespace list
{
    class node<T>
    {
        public T value;
        public node<T> next;
        public node<T> previous;

        public node(T val)
        {
            this.value = val;
            this.next = null;
            this.previous = null;
        }
    }
    public class List<T>
    {
        node<T> head;
        node<T> tail;

        public bool isEmpty() => (head == null);

        public void pushFront(T value)
        {
            if (isEmpty())
                head = tail = new node<T>(value);

            else
            {
                head.previous = new node<T>(value);
                head.previous.next = head;
                head = head.previous;
            }
        }

        public T popFront()
        {
            if (isEmpty())
                throw new ArgumentException("The list is empty");

            T value;

            if (head == tail)
            {
                value = head.value;
                head = tail = null;
            }

            else
            {
                value = head.value;
                head = head.next;
                head.previous = null;
            }
            return value;
        }

        public void pushBack(T value)
        {
            if (isEmpty())
                head = tail = new node<T>(value);

            else
            {
                tail.next = new node<T>(value);
                tail.next.previous = tail;
                tail = tail.next;
            }
        }

        public T popBack()
        {
            if (isEmpty())
                throw new ArgumentException("The list is empty");

            T value;

            if (head == tail)
            {
                value = head.value;
                head = tail = null;
            }

            else
            {
                value = tail.value;
                tail = tail.previous;
                tail.next = null;
            }
            return value;
        }

        public void print()
        {
            node<T> tmp = head;

            while (tmp != null)
            {
                Console.WriteLine(tmp.value);
                tmp = tmp.next;
            }
        }
    }
}
