use itertools::Itertools;

fn longest(a1: &str, a2: &str) -> String {
    let s = format!("{}{}", a1, a2);
    s.chars().sorted().dedup().collect()
}

fn main() {
    println!("Hello, world!");
    println!("Longest from aaa and: {}", longest("aaa", "and"))
}

#[test]
fn test1() {
    assert_eq!(
        longest("xyaabbbccccdefww", "xxxxyyyyabklmopq"),
        "abcdefklmopqwxy"
    )
}

#[test]
fn test2() {
    assert_eq!(
        longest("abcdefghijklmnopqrstuvwxyz", "abcdefghijklmnopqrstuvwxyz"),
        "abcdefghijklmnopqrstuvwxyz"
    )
}

#[test]
fn test3() {
    assert_eq!(longest("aaaaaabbbbbbb", "ccccdddddddc"), "abcd")
}

#[test]
fn test4() {
    assert_eq!(longest("tata", "mama"), "amt")
}

#[test]
fn test5() {
    assert_eq!(longest("long", "short"), "ghlnorst")
}
