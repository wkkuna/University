//Wiktoria Kuna 316418
public class Book extends Publication{
    String author;

    public Book() {
    }

    public Book(String title, String publisher, String publicationDate, String author) {
        super(title, publisher, publicationDate);
        this.author = author;
    }

    public Book(Publication publication, String author)
    {
        this.author = author;
        publisher = publication.publisher;
        publicationDate = publication.publicationDate;
        title = publication.title;
    }

    @Override
    public String toString() {
        return this.getClass().getName() + "\n" +
                "Title: " + title + "\n" +
                "Author: " + author + "\n" +
                "Publisher:" + publisher + "\n" +
                "Publication date: " + publicationDate + "\n";
    }
}
