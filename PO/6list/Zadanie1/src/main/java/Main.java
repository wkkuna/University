//Wiktoria Kuna 316418
//Przykładowy program
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

public class Main {
    public static void main(String[] argv) {
        var x = new Dictionary<Integer, String>();
        x.insert(300, "acxcz");
        x.insert(7, "xxxxc");
        x.insert(2, "aaaa");
        x.insert(-1, "aaav");
        x.insert(0, "aaaabb");
        x.insert(5, "aaaabbb");

        try (FileOutputStream fos = new FileOutputStream("tmp.txt");
             ObjectOutputStream oos = new ObjectOutputStream(fos);
        ) {
            oos.writeObject(x);
        } catch (Exception e) {
        }
        try (FileInputStream fis = new FileInputStream("tmp.txt");
             ObjectInputStream ois = new ObjectInputStream(fis)) {
            var b = (Dictionary<Integer, String>) ois.readObject();
            System.out.println(b.find(2));
            System.out.println(b.find(-1));
            System.out.println(b.find(0));
            System.out.println(b.find(5));
            System.out.println(b.find(7));
            System.out.println(b.find(300));
        } catch (Exception e) {
        }
    }
}
