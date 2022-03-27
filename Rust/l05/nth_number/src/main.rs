fn find_digit(num: i32, nth: i32) -> i32 {
    let tmp = num.abs().to_string();

    match nth {
        nth if nth <= 0 => -1,
        nth if nth > tmp.len() as i32 => 0,
        _ => tmp
            .chars()
            .nth(tmp.len() - nth as usize)
            .unwrap()
            .to_digit(10)
            .unwrap() as i32,
    }
}

fn main() {
    println!("Hello, world!");
    assert_eq!(find_digit(24, -8), -1);
}

#[test]
fn test1() {
    assert_eq!(find_digit(24, -8), -1);
}

#[test]
fn test2() {
    assert_eq!(find_digit(65, 0), -1);
}

#[test]
fn test4() {
    assert_eq!(find_digit(0, 20), 0);
}

#[test]
fn test5() {
    assert_eq!(find_digit(-456, 4), 0);
}
