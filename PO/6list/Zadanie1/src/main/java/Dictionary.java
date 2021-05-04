//Wiktoria Kuna 316418
import java.io.Serializable;
public class Dictionary<K extends Comparable<K>, V> implements Serializable {
    Element<K, V> head = null;

    public void insert(K key, V value) {
        //Empty list case
        if (head == null) {
            head = new Element<K, V>(key, value);
            return;
        }

        Element<K, V> tmp = head;
        //Element ought to be placed at the head of the list
        if (head.key.compareTo(key) > 0) {
            head = new Element<K, V>(key, value);
            head.next = tmp;
            return;
        }

        //Element ought to be placed in the middle of the list
        while (tmp != null && tmp.next != null) {
            if (tmp.next.key.compareTo(key) >= 0) {
                Element<K, V> next = tmp.next;
                tmp.next = new Element<K, V>(key, value);
                tmp.next.next = next;
                return;
            }
            tmp = tmp.next;
        }

        //Element ought to be placed at the end
        tmp.next = new Element<K, V>(key, value);
    }

    public V find(K key) throws Exception{
        Element<K, V> tmp = head;

        while (tmp != null) {
            if (tmp.key.compareTo(key) == 0)
                return tmp.value;
            tmp = tmp.next;
        }

        throw new Exception("Element with given key not found");
    }

    public void delete(K key) {
        Element<K, V> tmp = head;

        if (head == null)
            return;

        //delete at the head
        if (head != null && head.key.equals(key)) {
            head = head.next;
            return;
        }

        //delete in the middle
        while (tmp != null && tmp.next != null) {
            if (tmp.next.key.compareTo(key) == 0)
                tmp.next = tmp.next.next;
            tmp = tmp.next;
        }

        //delete at the end
        if (tmp != null && tmp.key.compareTo(key) == 0)
            tmp = null;
    }
}

