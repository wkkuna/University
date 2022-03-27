fn dig_pow(n: i64, p: i32) -> i64 {
    let digits: Vec<i64> = n
        .to_string()
        .chars()
        .map(|x| x.to_digit(10).unwrap() as i64)
        .collect();
    let nod = digits.len();
    let p = p as usize;

    let sum = (0..nod)
        .zip(p..p + nod)
        .fold(0, |acc, (i, x)| acc + digits[i].pow(x as u32));

    match sum % n {
        0 => sum / n,
        _ => -1,
    }
}

fn main() {
    println!("Hello, world!");
}

#[test]
fn test0() {
    assert_eq!(dig_pow(89, 1), 1);
}

#[test]
fn test1() {
    assert_eq!(dig_pow(123, 2), -1);
}

#[test]
fn test2() {
    assert_eq!(dig_pow(666, 3), -1);
}

#[test]
fn test3() {
    assert_eq!(dig_pow(46288, 3), 51);
}

#[test]
fn test4() {
    assert_eq!(dig_pow(6, 1), 1);
}
