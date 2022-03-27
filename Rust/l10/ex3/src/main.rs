fn comp(a: Vec<i64>, b: Vec<i64>) -> bool {
    let mut a: Vec<i64> = a.iter().map(|x| x * x).collect();
    let mut b = b;
    a.sort();
    b.sort();
    a == b
}

fn main() {
    comp(vec![], vec![]);
}

#[test]
fn test0() {
    let a1 = vec![];
    let a2 = vec![];
    assert_eq!(comp(a1, a2), true);
}

#[test]
fn test1() {
    let a1 = vec![2, 6, 8];
    let a2 = vec![2 * 2, 8 * 8];
    assert_eq!(comp(a1, a2), false);
}

#[test]
fn test2() {
    let a1 = vec![-14, -9, 1, 1];
    let a2 = vec![1, 1, 9 * 9, 15 * 15];
    assert_eq!(comp(a1, a2), false);
}

#[test]
fn test3() {
    let a1 = vec![121, 144, 19, 161, 19, 144, 19, 11];
    let a2 = vec![
        11 * 11,
        121 * 121,
        144 * 144,
        19 * 19,
        161 * 161,
        19 * 19,
        144 * 144,
        19 * 19,
    ];
    assert_eq!(comp(a1, a2), true);
}

#[test]
fn test4() {
    let a1 = vec![121, 144, 19, 161, 19, 144, 19, 11];
    let a2 = vec![
        11 * 21,
        121 * 121,
        144 * 144,
        19 * 19,
        161 * 161,
        19 * 19,
        144 * 144,
        19 * 19,
    ];
    assert_eq!(comp(a1, a2), false);
}
