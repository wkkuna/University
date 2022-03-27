use std::collections::BTreeMap;

fn letter_frequency(input: &str) -> BTreeMap<char, i32> {
    input
        .to_lowercase()
        .chars()
        .filter(|c| c.is_alphabetic())
        .fold(BTreeMap::new(), |mut acc, c| {
            *acc.entry(c).or_insert(0) += 1;
            acc
        })
}

fn main() {
    print!("");
    letter_frequency("abhdifhuiahsodas");
}

#[test]
fn test0() {
    let answer: BTreeMap<char, i32> = [].iter().cloned().collect();

    assert_eq!(letter_frequency(""), answer);
}

#[test]
fn test1() {
    let answer: BTreeMap<char, i32> = [('a', 2), ('c', 1), ('l', 1), ('t', 1), ('u', 1)]
        .iter()
        .cloned()
        .collect();

    assert_eq!(letter_frequency("actual"), answer);
}

#[test]
fn test2() {
    let answer: BTreeMap<char, i32> = [
        ('a', 3),
        ('b', 2),
        ('f', 1),
        ('p', 1),
        ('s', 1),
        ('t', 2),
        ('u', 1),
        ('x', 5),
    ]
    .iter()
    .cloned()
    .collect();

    assert_eq!(letter_frequency("AaabBF UttsP xxxxx"), answer);
}

#[test]
fn test3() {
    let answer: BTreeMap<char, i32> = [
        ('n', 3),
        ('d', 2),
        ('s', 2),
        ('u', 2),
        ('a', 1),
        ('b', 1),
        ('c', 1),
        ('e', 1),
        ('i', 1),
        ('k', 1),
    ]
    .iter()
    .cloned()
    .collect();

    assert_eq!(letter_frequency(" Bunnies and duck!s  ?.,  "), answer);
}

#[test]
fn test4() {
    let answer: BTreeMap<char, i32> = [('o', 2), ('d', 1), ('f', 1)].iter().cloned().collect();

    assert_eq!(letter_frequency("fo od"), answer);
}
