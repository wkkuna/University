fn last_digit(lst: &[u64]) -> u64 {
    lst.iter().rev().fold(1, |acc, x| {
        let base = if *x < 20 { *x } else { *x % 20 + 20 };
        let exp = if acc < 4 { acc } else { acc % 4 + 4 } as u32;
        base.pow(exp)
    }) % 10
}

fn main() {
    last_digit(&vec![499942, 898102, 846073]);
}

#[test]
fn test0() {
    assert_eq!(last_digit(&vec![]), 1);
}

#[test]
fn test1() {
    assert_eq!(last_digit(&vec![4966662, 8934502, 8123133]), 6);
}

#[test]
fn test2() {
    assert_eq!(last_digit(&vec![9999999999, 0, 12345678]), 1);
}

#[test]
fn test3() {
    assert_eq!(last_digit(&vec![213, 323, 32, 323, 323, 65, 89, 52]), 3);
}

#[test]
fn test4() {
    assert_eq!(last_digit(&vec![11, 22, 33, 44, 55, 66, 77, 88]), 1);
}
