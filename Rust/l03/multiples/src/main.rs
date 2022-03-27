fn solution(num: i32) -> i32 {
  (0..num).filter(|x| x % 3 == 0 || x % 5 == 0).sum()
}

fn main() {
  println!("Hello, world!");
  assert_eq!(solution(6), 8);
}

#[test]
fn test1() {
  assert_eq!(solution(6), 8);
}

#[test]
fn test2() {
  assert_eq!(solution(11), 33);
}

#[test]
fn test3() {
  assert_eq!(solution(10), 23);
}

#[test]
fn test4() {
  assert_eq!(solution(0), 0);
}

#[test]
fn test5() {
  assert_eq!(solution(15), 45);
}
