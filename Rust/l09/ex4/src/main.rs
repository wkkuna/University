fn john(n: i32) -> Vec<i32> {
    john_and_ann(n, true)
}

fn ann(n: i32) -> Vec<i32> {
    john_and_ann(n, false)
}

fn sum_john(n: i32) -> i32 {
    john(n).iter().sum()
}

fn sum_ann(n: i32) -> i32 {
    ann(n).iter().sum()
}

fn john_and_ann(n: i32, john: bool) -> Vec<i32> {
    let mut jh: Vec<i32> = vec![];
    let mut an: Vec<i32> = vec![];

    for i in 0..n {
        match i {
            0 => {
                jh.push(0);
                an.push(1);
            }
            _ => {
                let idx = (i - 1) as usize;
                let t_ann = jh[idx] as usize;
                jh.push(i - an[t_ann]);
                let t_john = an[idx] as usize;
                an.push(i - jh[t_john]);
            }
        };
    }

    match john {
        true => jh,
        false => an,
    }
}

fn main() {
    john(42);
    ann(42);
    sum_john(42);
    sum_ann(42);
}

#[test]
fn test_basic() {
    assert_eq!(john(0), vec![]);
    assert_eq!(ann(0), vec![]);
    assert_eq!(sum_john(0), 0);
    assert_eq!(sum_ann(0), 0);
}

#[test]
fn test_john() {
    assert_eq!(john(14), vec![0, 0, 1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 7, 8]);
    assert_eq!(
        john(25),
        vec![0, 0, 1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 7, 8, 9, 9, 10, 11, 11, 12, 12, 13, 14, 14, 15]
    );
}
#[test]
fn test_ann() {
    assert_eq!(ann(10), vec![1, 1, 2, 2, 3, 3, 4, 5, 5, 6]);
    assert_eq!(
        ann(18),
        vec![1, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6, 7, 8, 8, 9, 9, 10, 11]
    );
}
#[test]
fn test_sum_john() {
    assert_eq!(sum_john(88), 2372);
    assert_eq!(sum_john(4), 3);
}
#[test]
fn test_sum_ann() {
    assert_eq!(sum_ann(21), 136);
    assert_eq!(sum_ann(95), 2776);
}
