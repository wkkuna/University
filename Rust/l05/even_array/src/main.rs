fn even_numbers(array: &Vec<i32>, number: usize) -> Vec<i32> {
    let v = array
        .iter()
        .filter(|&x| x % 2 == 0)
        .cloned()
        .collect::<Vec<i32>>();
    v[v.len().saturating_sub(number)..].to_vec()
}

fn main() {
    println!("Hello, world!");
    assert_eq!(
        even_numbers(&vec!(6, -25, 3, 7, 5, 5, 7, -3, 23), 1),
        vec!(6)
    );
}

#[test]
fn test1() {
    assert_eq!(
        even_numbers(&vec!(6, -25, 3, 7, 5, 5, 7, -3, 23), 1),
        vec!(6)
    );
}

#[test]
fn test2() {
    assert_eq!(
        even_numbers(&vec!(-22, 5, 3, 11, 26, -6, -7, -8, -9, -8, 26), 2),
        vec!(-8, 26)
    );
}

#[test]
fn test3() {
    assert_eq!(
        even_numbers(&vec!(1, 2, 3, 4, 5, 6, 7, 8, 9), 3),
        vec!(4, 6, 8)
    );
}

#[test]
fn test4() {
    assert_eq!(
        even_numbers(&vec!(6, 8, 1, 1, 1, 1, 3, 5, 6, 9, 9, 7), 5),
        vec!(6, 8, 6)
    );
}

#[test]
fn test5() {
    assert_eq!(
        even_numbers(&vec!(1, 3, 5, 3, 3, 9, 23, 33, 7, 1), 1),
        vec!()
    );
}
