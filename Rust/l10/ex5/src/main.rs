use std::cmp;
fn print(n: i32) -> Option<String> {
    if n < 0 || n % 2 == 0 {
        return None;
    };

    let mut output = "".to_string();
    for i in 0..n {
        let idx = cmp::min(i, n - i - 1) as usize;
        output = format!(
            "{}{}{}\n",
            output,
            " ".repeat((n as usize - (2 * idx + 1)) / 2),
            "*".repeat(2 * idx + 1)
        );
    }
    Some(output)
}

fn main() {
    print(0);
}

#[test]
fn test0() {
    assert_eq!(print(0), None);
}
#[test]
fn test1() {
    assert_eq!(print(-6), None);
}
#[test]
fn test2() {
    assert_eq!(print(1), Some("*\n".to_string()));
}
#[test]
fn test3() {
    assert_eq!(print(5), Some("  *\n ***\n*****\n ***\n  *\n".to_string()));
}
#[test]
fn test4() {
    assert_eq!(
        print(7),
        Some("   *\n  ***\n *****\n*******\n *****\n  ***\n   *\n".to_string())
    );
}
