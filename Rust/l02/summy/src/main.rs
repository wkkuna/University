fn summy(strng: &str) -> i32 {
    strng
        .split_whitespace()
        .map(|x| x.parse::<i32>().unwrap())
        .sum()
}

fn main() {
    println!("Hello, world!");
    println!("Summy from 1 2 3: {}", summy("1 2 3"));
}
#[test]
fn test1() {
    assert_eq!(summy("10 15"), 25);
}

#[test]
fn test2() {
    assert_eq!(summy("1 2 3 4 5"), 15);
}

#[test]
fn test3() {
    assert_eq!(summy("13 22 5"), 40);
}

#[test]
fn test4() {
    assert_eq!(summy("8 3"), 11);
}

#[test]
fn test5() {
    assert_eq!(summy("8 4 6"), 18);
}
