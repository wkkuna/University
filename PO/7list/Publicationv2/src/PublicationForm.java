//Wiktoria Kuna 316418
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;

public class PublicationForm {
    private JPanel panel;

    private JLabel titleLabel;
    private JLabel authorLabel;
    private JLabel publisherLabel;
    private JLabel publicationDateLabel;
    private JTextField titleTextField;
    private JTextField authorTextField;
    private JTextField publisherTextField;
    private JLabel dateInfoLabel;
    private JComboBox dayComboBox;
    private JComboBox monthComboBox;
    private JComboBox yearComboBox;
    private JButton saveToFileButton;
    private JButton clearButton;
    private JButton displayButton;
    private JTextPane dateFailureLog;
    private JTextPane changesLog;


    private String filename;
    private String className;


    private Publication currentPublication;
    private String date = "-";

    void setCurrentObject() {
        clearObject();
        if (filename.equals("Book"))
            currentPublication = new Book(currentPublication, authorTextField.getText());

        currentPublication.publisher = publisherTextField.getText();
        currentPublication.title = titleTextField.getText();

        String day = dayComboBox.getSelectedItem().toString();
        String month = monthComboBox.getSelectedItem().toString();
        String year = yearComboBox.getSelectedItem().toString();

        if (day.compareTo("-") != 0 && ((month.equals("-")) || year.equals("-")) || month.compareTo("-") != 0 && year.equals("-")) {
            dateFailureLog.setText("Invalid Data Format");
            dateFailureLog.setVisible(true);
            date = "-";
        } else {
            dateFailureLog.setVisible(false);
            date = day.equals("-") ? "" : day + " ";
            date += month.equals("-") ? "" : month + " ";
            date += year.equals("-") ? "-" : year;
        }
        currentPublication.publicationDate = date;
    }

    void clearObject() {
        switch (className) {
            case "Publication":
                currentPublication = new Publication("", "", "-");
                break;
            case "Book":
                currentPublication = new Book("", "", "-", "");
                break;
            case "Magazine":
                currentPublication = new Magazine("", "", "");
                break;
        }
    }

    public PublicationForm(String filename, String className) throws Exception {
        this.className = className;
        this.filename = filename;

        authorLabel.setVisible(className.equals("Book"));
        authorTextField.setVisible(className.equals("Book"));

        var file = new File(filename);

        if (file.exists()) {
            try (FileInputStream fis = new FileInputStream(filename);
                 ObjectInputStream ois = new ObjectInputStream(fis)) {

                currentPublication = (Publication) ois.readObject();
                changesLog.setText(currentPublication.toString());

            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        } else
            setCurrentObject();

        displayButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                setCurrentObject();
                changesLog.setText(currentPublication.toString());
            }
        });


        clearButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                clearObject();
                changesLog.setText(currentPublication.toString());
                dateFailureLog.setVisible(false);
            }
        });
        saveToFileButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                displayButton.doClick();

                if (!file.exists()) {
                    try {
                        file.createNewFile();
                    } catch (IOException ioException) {
                        ioException.printStackTrace();
                    }
                }

                try (FileOutputStream fos = new FileOutputStream(filename);
                     ObjectOutputStream oos = new ObjectOutputStream(fos);
                ) {
                    oos.writeObject(currentPublication);
                } catch (Exception ex) {
                    System.out.println(ex.getMessage());
                }

            }
        });
    }


    public static void main(String[] args) throws Exception {
        if (args.length != 2)
            throw new Exception("Pass file name and class name as parameters");
        if (args[1].compareTo("Publication") != 0 && args[1].compareTo("Book") != 0 && args[1].compareTo("Magazine") != 0)
            throw new Exception("Unknown class");

        JFrame frame = new JFrame("PublicationForm");
        frame.setContentPane(new PublicationForm(args[0], args[1]).panel);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setLocationRelativeTo(null);
        frame.setMinimumSize(frame.getMinimumSize());
        frame.setPreferredSize(frame.getPreferredSize());
        frame.setVisible(true);
    }
}
