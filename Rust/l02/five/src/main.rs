fn dont_give_me_five(start: isize, end: isize) -> isize {
    (start..=end)
        .filter(|x| !x.to_string().contains('5'))
        .collect::<Vec<isize>>()
        .len() as isize
}

fn main() {
    println!("Hello, world!");
    println!("Don't give me five!! 1-5: {}", dont_give_me_five(1, 5))
}

#[test]
fn test1() {
    assert_eq!(dont_give_me_five(1, 9), 8);
}

#[test]
fn test2() {
    assert_eq!(dont_give_me_five(4, 17), 12);
}

#[test]
fn test3() {
    assert_eq!(dont_give_me_five(1, 3), 3);
}

#[test]
fn test4() {
    assert_eq!(dont_give_me_five(50, 60), 1);
}

#[test]
fn test5() {
    assert_eq!(dont_give_me_five(60, 80), 19);
}
