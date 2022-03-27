fn count_bits(n: i64) -> u32 {
    let mut n = n as u64;
    let m = [
        0x5555555555555555,
        0x3333333333333333,
        0x0f0f0f0f0f0f0f0f,
        0xff00ff00ff00ff,
        0xffff0000ffff,
        0xffffffff,
    ];

    for i in 0..=5 {
        let shift = 1 << i;
        n = (n & m[i]) + ((n >> shift) & m[i]);
    }
    n as u32
    // or n.count_ones but it felt like cheating
}

fn main() {
    count_bits(3);
}

#[test]
fn test0() {
    assert_eq!(count_bits(0), 0);
}

#[test]
fn test1() {
    assert_eq!(count_bits(32), 1);
}

#[test]
fn test2() {
    assert_eq!(count_bits(15), 4);
}

#[test]
fn test3() {
    assert_eq!(count_bits(-67), 62);
}

#[test]
fn test4() {
    assert_eq!(count_bits(-123), 59);
}
