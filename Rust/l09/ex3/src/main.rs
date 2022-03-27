fn part_list(arr: Vec<&str>) -> String {
    let n = arr.len();
    let mut result = String::new();

    for i in 1..n {
        result = format!(
            "{}({}, {})",
            result,
            &arr[..i].join(" "),
            &arr[i..].join(" ")
        )
    }
    result
}

fn main() {
    part_list(vec!["Bunny", "hops"]);
}

#[test]
fn test0() {
    let answer = "(Bunny, hops)";

    assert_eq!(part_list(vec!["Bunny", "hops"]), answer);
}

#[test]
fn test1() {
    let answer = "(Mom, loves spaghetti)(Mom loves, spaghetti)";

    assert_eq!(part_list(vec!["Mom", "loves", "spaghetti"]), answer);
}

#[test]
fn test2() {
    let answer = "(Smell, of napalm in the morning)(Smell of, napalm in the morning)(Smell of napalm, in the morning)(Smell of napalm in, the morning)(Smell of napalm in the, morning)";

    assert_eq!(
        part_list(vec!["Smell", "of", "napalm", "in", "the", "morning"]),
        answer
    );
}

#[test]
fn test3() {
    let answer = "(Ducks, duckies ducklings)(Ducks duckies, ducklings)";

    assert_eq!(part_list(vec!["Ducks", "duckies", "ducklings"]), answer);
}

#[test]
fn test4() {
    let answer = "(Stinky, cheese)";

    assert_eq!(part_list(vec!["Stinky", "cheese"]), answer);
}
