fn spin_words(words: &str) -> String {
    words
        .split(' ')
        .map(|x| {
            if x.len() >= 5 {
                x.chars().rev().collect::<String>()
            } else {
                (x).to_string()
            }
        })
        .collect::<Vec<String>>()
        .join(" ")
}

fn main() {
    assert_eq!(
        spin_words("Stop Spinning My Words"),
        "Stop gninnipS My sdroW"
    );
}

#[test]
fn test1() {
    assert_eq!(
        spin_words("Stop Spinning My Words"),
        "Stop gninnipS My sdroW"
    );
}

#[test]
fn test2() {
    assert_eq!(spin_words("This is a test"), "This is a test");
}

#[test]
fn test3() {
    assert_eq!(spin_words("Welcome"), "emocleW");
}

#[test]
fn test4() {
    assert_eq!(spin_words(""), "");
}

#[test]
fn test5() {
    assert_eq!(spin_words("Chicken"), "nekcihC");
}
