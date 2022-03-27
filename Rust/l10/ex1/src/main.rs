struct Sudoku {
    data: Vec<Vec<u32>>,
}

impl Sudoku {
    fn is_valid(&self) -> bool {
        let size = self.data.len() as u32;
        let valid_sum = (1..=size).into_iter().sum();
        let mut col_sum = vec![0; size as usize];
        let mut sq_sum = vec![0; size as usize];
        let sqt = (size as f64).sqrt() as u32;

        // validate rows
        for (row, r) in (&self.data).iter().zip(0..size) {
            if row.iter().sum::<u32>() != valid_sum {
                return false;
            }

            // validate columns
            col_sum = col_sum
                .iter()
                .enumerate()
                .map(|(i, x)| x + row[i])
                .collect();

            // validate squares
            let first_sq_idx = ((r / sqt) * sqt) as usize;

            for (i, x) in row.iter().enumerate() {
                let sq_off = i / sqt as usize;
                sq_sum[first_sq_idx + sq_off] += x;
            }
        }

        col_sum.iter().all(|&x| x == valid_sum) && sq_sum.iter().all(|&x| x == valid_sum)
    }
}

fn main() {
    let sudoku = Sudoku {
        data: vec![vec![1]],
    };
    assert!(sudoku.is_valid());
}

#[test]
fn test0() {
    let sudoku = Sudoku {
        data: vec![vec![1]],
    };
    assert!(sudoku.is_valid());
}

#[test]
fn test1() {
    let sudoku = Sudoku {
        data: vec![
            vec![1, 2, 3, 4, 5],
            vec![1, 2, 3, 4],
            vec![1, 2, 3, 4],
            vec![1],
        ],
    };
    assert!(!sudoku.is_valid());
}

#[test]
fn test2() {
    let sudoku = Sudoku {
        data: vec![
            vec![1, 2, 3, 4, 5, 6, 7, 8, 9],
            vec![1, 2, 3, 4, 5, 6, 7, 8, 9],
            vec![1, 2, 3, 4, 5, 6, 7, 8, 9],
            vec![1, 2, 3, 4, 5, 6, 7, 8, 9],
            vec![1, 2, 3, 4, 5, 6, 7, 8, 9],
            vec![1, 2, 3, 4, 5, 6, 7, 8, 9],
            vec![1, 2, 3, 4, 5, 6, 7, 8, 9],
            vec![1, 2, 3, 4, 5, 6, 7, 8, 9],
            vec![1, 2, 3, 4, 5, 6, 7, 8, 9],
        ],
    };
    assert!(!sudoku.is_valid());
}

#[test]
fn test3() {
    let sudoku = Sudoku {
        data: vec![
            vec![7, 8, 4, 1, 5, 9, 3, 2, 6],
            vec![5, 3, 9, 6, 7, 2, 8, 4, 1],
            vec![6, 1, 2, 4, 3, 8, 7, 5, 9],
            vec![9, 2, 8, 7, 1, 5, 4, 6, 3],
            vec![3, 5, 7, 8, 4, 6, 1, 9, 2],
            vec![4, 6, 1, 9, 2, 3, 5, 8, 7],
            vec![8, 7, 6, 3, 9, 4, 2, 1, 5],
            vec![2, 4, 3, 5, 6, 1, 9, 7, 8],
            vec![1, 9, 5, 2, 8, 7, 6, 3, 4],
        ],
    };
    assert!(sudoku.is_valid());
}

#[test]
fn test4() {
    let sudoku = Sudoku {
        data: vec![
            vec![1, 4, 2, 3],
            vec![3, 2, 4, 1],
            vec![4, 1, 3, 2],
            vec![2, 3, 1, 4],
        ],
    };
    assert!(sudoku.is_valid());
}
