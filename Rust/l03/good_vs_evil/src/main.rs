fn points(force: &str, values: Vec<i32>) -> i32 {
    force
        .split(" ")
        .zip(values)
        .map(|(x, y)| x.parse::<i32>().unwrap() * y)
        .sum()
}

fn good_vs_evil(good: &str, evil: &str) -> String {
    let good_values = vec![1, 2, 3, 3, 4, 10];
    let evil_values = vec![1, 2, 2, 2, 3, 5, 10];
    let good_force = points(good, good_values);
    let evil_force = points(evil, evil_values);

    match good_force - evil_force {
        0 => String::from("Battle Result: No victor on this battle field"),
        x if x < 0 => String::from("Battle Result: Evil eradicates all trace of Good"),
        x if x > 0 => String::from("Battle Result: Good triumphs over Evil"),
        _ => String::from("Battle Result: Unknown"),
    }
}

fn main() {
    good_vs_evil("0 0 0 0 0 0", "0 0 0 0 0 0 0");
}

#[test]
fn test1() {
    assert_eq!(
        good_vs_evil("0 0 0 0 0 5", "0 0 0 0 0 0 0"),
        "Battle Result: Good triumphs over Evil"
    );
}

#[test]
fn test2() {
    assert_eq!(
        good_vs_evil("0 0 0 0 0 2", "0 4 0 5 0 4 10"),
        "Battle Result: Evil eradicates all trace of Good"
    );
}

#[test]
fn test3() {
    assert_eq!(
        good_vs_evil("1 0 0 0 0 10", "1 0 0 0 0 0 10"),
        "Battle Result: No victor on this battle field"
    );
}

#[test]
fn test4() {
    assert_eq!(
        good_vs_evil("0 2 0 1 0 2", "0 4 0 5 0 4 10"),
        "Battle Result: Evil eradicates all trace of Good"
    );
}

#[test]
fn test5() {
    assert_eq!(
        good_vs_evil("1 3 5 0 0 10", "1 3 0 0 5 0 10"),
        "Battle Result: No victor on this battle field"
    );
}
