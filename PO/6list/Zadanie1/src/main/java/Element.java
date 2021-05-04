//Wiktoria Kuna 316418
import java.io.Serializable;
class Element<K extends Comparable<K>, V> implements Serializable{
    K key;
    V value;
    public Element<K, V> next;

    public Element(K key, V value) {
        this.key = key;
        this.value = value;
        this.next = null;
    }
}
