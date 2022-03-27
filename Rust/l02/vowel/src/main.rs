fn get_count(string: &str) -> usize {
  string
    .chars()
    .map(|x| match x {
      'a' | 'e' | 'i' | 'o' | 'u' => 1,
      _ => 0,
    })
    .sum()
}

fn main() {
  println!("Hello, world!");
  println!("Get count from: aaabbbccc: {}", get_count("aaabbbccc"))
}

#[test]
fn test1() {
  assert_eq!(get_count("abracadabra"), 5);
}

#[test]
fn test2() {
  assert_eq!(get_count("ala ma kota"), 5);
}

#[test]
fn test3() {
  assert_eq!(get_count("kocham kaczuszki"), 5);
}

#[test]
fn test4() {
  assert_eq!(get_count("qwqrwrqwlkjps"), 0);
}

#[test]
fn test5() {
  assert_eq!(get_count("papapapapapapryka"), 7);
}
