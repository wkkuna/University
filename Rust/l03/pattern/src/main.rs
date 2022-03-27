fn push_modulo(v: &mut Vec<String>, idx: usize, s1: &str, s2: &str) {
    match idx % 2 {
        0 => v.push(String::from(s1)),
        1 => v.push(String::from(s2)),
        _ => unreachable!(),
    };
}

fn zoom(n: i32) -> String {
    let n = n as usize;

    let (s1, s2) = match n % 4 {
        1 => ("■", "□"),
        3 => ("□", "■"),
        _ => unreachable!(),
    };

    let mut v = vec![];

    for i in 0..n as usize {
        for j in 0..n as usize {
            let cond = match i {
                i if i <= n / 2 => (j < i || j > n - i - 1),
                _ => (j > i || j < n - i - 1),
            };
            push_modulo(&mut v, if cond { j } else { i }, s1, s2);
        }
        v.push(String::from("\n"));
    }
    v[..v.len() - 1].join("")
}

fn main() {
    assert_eq!(zoom(1), "■");
}

#[test]
fn test1() {
    assert_eq!(zoom(1), "■");
}

#[test]
fn test2() {
    assert_eq!(
        zoom(3),
        "\
□□□
□■□
□□□"
    );
}

#[test]
fn test3() {
    assert_eq!(
        zoom(5),
        "\
■■■■■
■□□□■
■□■□■
■□□□■
■■■■■"
    );
}

#[test]
fn test4() {
    assert_eq!(
        zoom(7),
        "\
□□□□□□□
□■■■■■□
□■□□□■□
□■□■□■□
□■□□□■□
□■■■■■□
□□□□□□□"
    );
}

#[test]
fn test5() {
    assert_eq!(
        zoom(9),
        "\
■■■■■■■■■
■□□□□□□□■
■□■■■■■□■
■□■□□□■□■
■□■□■□■□■
■□■□□□■□■
■□■■■■■□■
■□□□□□□□■
■■■■■■■■■"
    );
}
