fn last_digit(str1: &str, str2: &str) -> i32 {
  if str2 == "0" {
    return 1;
  }

  let vec = match str1.chars().last().unwrap().to_digit(10).unwrap() {
    0 => vec![0],
    1 => vec![1],
    2 => vec![6, 2, 4, 8],
    3 => vec![1, 3, 9, 7],
    4 => vec![6, 4],
    5 => vec![5],
    6 => vec![6],
    7 => vec![1, 7, 9, 3],
    8 => vec![6, 8, 4, 2],
    9 => vec![1, 9],
    _ => vec![],
  };

  let last_digits = match str2.len() {
    x if x < 2 => str2.parse::<i32>().unwrap(),
    _ => str2[str2.len() - 2..].parse::<i32>().unwrap(),
  };

  match last_digits {
    0 => vec[0],
    _ => vec[(last_digits % (vec.len()) as i32) as usize],
  }
}

fn main() {
  println!("Hello, world!");
  assert_eq!(last_digit("4", "1"), 4);
}

#[test]
fn test1() {
  assert_eq!(last_digit("4", "1"), 4);
}

#[test]
fn test2() {
  assert_eq!(
    last_digit(
      "3715290469715693021198967285016729344580685479654510946723",
      "68819615221552997273737174557165657483427362207517952651"
    ),
    7
  );
}

#[test]
fn test3() {
  assert_eq!(last_digit("3", "3"), 7);
}

#[test]
fn test4() {
  assert_eq!(last_digit("0", "0"), 1);
}

#[test]
fn test5() {
  assert_eq!(last_digit("45", "352352352352"), 5);
}
