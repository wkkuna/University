fn expanded_form(n: u64) -> String {
    let mut idx = 0;
    let mut result = String::from("");

    let number = n.to_string();
    let mut values = number.split("").collect::<Vec<&str>>();

    values.reverse();

    for c in values {
        if c == "" {
            continue;
        }

        let comp = c.to_owned() + &format!("{:0^1$}", "", idx).to_owned();

        if c == "0" {
            idx += 1;
            continue;
        } else if result.is_empty() {
            result = format!("{}", comp);
        } else {
            result = format!("{} + {}", comp, result);
        }

        idx += 1;
    }

    result
}

fn main() {
    expanded_form(42);
    expanded_form(333);
}

#[test]
fn test1() {
    assert_eq!(expanded_form(42), "40 + 2");
}

#[test]
fn test2() {
    assert_eq!(expanded_form(333), "300 + 30 + 3");
}

#[test]
fn test3() {
    assert_eq!(expanded_form(0), "0");
}

#[test]
fn test4() {
    assert_eq!(expanded_form(55), "50 + 5");
}

#[test]
fn test5() {
    assert_eq!(expanded_form(666), "600 + 60 + 6");
}
