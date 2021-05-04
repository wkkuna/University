//Wiktoria Kuna 316418
import java.io.Serializable;

public class Publication implements Serializable {
    String title;
    String publisher;
    String publicationDate;

    public Publication(String title, String publisher, String publicationDate) {
        this.title = title;
        this.publisher = publisher;
        this.publicationDate = publicationDate;
    }

    public Publication() {
    }


    @Override
    public String toString() {
        return this.getClass().getName() + "\n" +
                "Title: " + title + "\n" +
                "Publisher:" + publisher + "\n" +
                "Publication date: " + publicationDate + "\n";
    }
}