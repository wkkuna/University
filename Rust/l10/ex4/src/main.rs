fn encode(msg: String, n: i32) -> Vec<i32> {
    let code = n
        .to_string()
        .chars()
        .map(|x| x.to_digit(10).unwrap())
        .collect::<Vec<u32>>();
    msg.chars()
        .enumerate()
        .map(|(y, x)| ((x as u32 - 'a' as u32) + code[y % code.len()] + 1) as i32)
        .collect()
}

fn main() {
    encode("bunnyflop".to_string(), 2137);
}

#[test]
fn test0() {
    assert_eq!(encode("".to_string(), 1939), vec![]);
}

#[test]
fn test1() {
    assert_eq!(
        encode("masterpiece".to_string(), 220521),
        vec![15, 3, 19, 25, 7, 19, 18, 11, 5, 8, 7]
    );
}

#[test]
fn test2() {
    assert_eq!(encode("ducks".to_string(), 1939), vec![5, 30, 6, 20, 20]);
}

#[test]
fn test3() {
    assert_eq!(
        encode("bunnyflop".to_string(), 2137),
        vec![4, 22, 17, 21, 27, 7, 15, 22, 18]
    );
}

#[test]
fn test4() {
    assert_eq!(
        encode("cakecakecakecakecakecake".to_string(), 1802),
        vec![4, 9, 11, 7, 4, 9, 11, 7, 4, 9, 11, 7, 4, 9, 11, 7, 4, 9, 11, 7, 4, 9, 11, 7]
    );
}
