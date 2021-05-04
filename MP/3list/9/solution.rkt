#lang racket
(provide partition quicksort)

;;Partition
(define (partition n xs)
  (define (partition-tool op xs)
    (if (null? xs)
        null
        (if (op (car xs) n)
            (cons (car xs) (partition-tool op (cdr xs)))
            (partition-tool op (cdr xs)))))
  (cons (partition-tool <= xs) (partition-tool > xs)))
     
    
;;Quicksort
(define (quicksort xs)
  (if (null? xs)
      '()
      (let* ([x (car xs)]
             [xs (cdr xs)]
             [pair (partition x xs)]
             [left (car pair)]
             [right (cdr pair)])
        (append (quicksort left)
                (list x)
                (quicksort right)))))
                
;;---------------------------------- TESTS ----------------------------------
(require rackunit)
(define epsilon 0)

;;Partition tests
(check-within (partition 0 '()) '(()) epsilon "Partition failed for null")
(check-within (partition 1 '(1)) '((1)) epsilon "Partition failed for one elem. (<= n) list")
(check-within (partition 0 '(1)) '(()1) epsilon"Partition failed for one elem. (> n) list")
(check-within (partition 2 '(3 4 1 2)) '((1 2) 3 4) epsilon "Partition failed for even NoE")
(check-within (partition 2 '(3 4 5 2 1)) '((2 1) 3 4 5) epsilon "Partition failed for uneven NoE")
(check-within (partition 2 '(5 2 2 2 1)) '((2 2 2 1) 5) epsilon "Partition failed for reoccuring elem.")

;;Quicksort tests
(check-within (quicksort '()) '() epsilon "Quicksort failed for null")
(check-within (quicksort '(1)) '(1) epsilon "Quicksort failed for one element")
(check-within (quicksort '(2 1 3 8 9 0)) '(0 1 2 3 8 9) epsilon "Quicksort failed for unique elem with even NoE")
(check-within (quicksort '(2 1 5 9 1 3 7)) '(1 1 2 3 5 7 9) epsilon "Quicksort failed for unique elem with uneven NoE")
(check-within (quicksort '(2 2 4 1 2 5)) '(1 2 2 2 4 5) epsilon "Quicksort failed for ununique elem with even NoE")
(check-within (quicksort '(2 5 7 1 4 1 2 5 0)) '(0 1 1 2 2 4 5 5 7) epsilon "Quicksort failed for ununique elem with uneven NoE")