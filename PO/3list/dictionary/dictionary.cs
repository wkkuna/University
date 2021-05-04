//Wiktoria Kuna 316418
using System;

namespace dictionary
{
    class element<K, V> where K : IComparable<K>
    {
        public K key;
        public V value;
        public element<K, V> next;

        public element(K key, V value)
        {
            this.key = key;
            this.value = value;
            this.next = null;
        }
    }

    public class Dictionary<K, V> where K : IComparable<K>
    {
        element<K, V> head = null;

        public void insert(K key, V value)
        {
            //Empty list case
            if (head == null)
            {
                head = new element<K, V>(key, value);
                return;
            }

            element<K, V> tmp = head;
            //Element ought to be placed at the head of the list
            if (head.key.CompareTo(key) > 0)
            {
                head = new element<K, V>(key, value);
                head.next = tmp;
                return;
            }


            //Element ought to be placed in the middle of the list
            while (tmp != null && tmp.next != null)
            {

                if (tmp.next.key.CompareTo(key) >= 0)
                {
                    element<K, V> next = tmp.next;
                    tmp.next = new element<K, V>(key, value);
                    tmp.next.next = next;
                    return;
                }
                tmp = tmp.next;
            }

            //Element ought to be placed at the end
            tmp.next = new element<K, V>(key, value);
        }

        public V find(K key)
        {
            element<K, V> tmp = head;

            while (tmp != null)
            {
                if (tmp.key.CompareTo(key) == 0)
                    return tmp.value;
                tmp = tmp.next;
            }

            throw new System.ArgumentException("Element with given key not found");
        }

        public void delete(K key)
        {
            element<K, V> tmp = head;

            if (head == null)
                return;

            //delete at the head
            if (head != null && head.key.CompareTo(key) == 0)
            {
                head = head.next;
                return;
            }

            //delete in the middle
            while (tmp != null && tmp.next != null)
            {
                if (tmp.next.key.CompareTo(key) == 0)
                    tmp.next = tmp.next.next;
                tmp = tmp.next;
            }

            //delete at the end
            if (tmp != null && tmp.key.CompareTo(key) == 0)
                tmp = null;
        }

        public void print()
        {
            element<K, V> tmp = head;
            while (tmp != null)
            {
                Console.WriteLine("<{0}, {1}>\n", tmp.key, tmp.value);
                tmp = tmp.next;
            }
        }
    }
}
