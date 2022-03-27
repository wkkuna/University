fn camel_case(str: &str) -> String {
    str.split_whitespace()
        .map(|x: &str| {
            let y = x.split_at(1);
            format!("{}{}", y.0.to_uppercase(), y.1.to_lowercase())
        })
        .collect::<Vec<String>>()
        .join("")
}

fn main() {
    println!("Hello, world!");
    println!(
        "Camel case for pretty little ducklings: {}",
        camel_case("pretty little ducklings")
    );
    println! {"{}", camel_case("")};
}

#[test]
fn test1() {
    assert_eq!(camel_case("test case"), "TestCase");
}

#[test]
fn test2() {
    assert_eq!(camel_case(""), "");
}

#[test]
fn test3() {
    assert_eq!(camel_case("  pampuchy "), "Pampuchy");
}

#[test]
fn test4() {
    assert_eq!(
        camel_case("rabbits are the best pets"),
        "RabbitsAreTheBestPets"
    );
}

#[test]
fn test5() {
    assert_eq!(camel_case("snakes    are   cool     "), "SnakesAreCool");
}
