#lang racket
;;Wiktoria Kuna 316418
(require rackunit)
(define epsilon 0)

(provide merge split mergesort)

;;Merge
(define (merge xs ys)
  (cond [(null? xs) ys]
        [(null? ys) xs]
        [(< (car xs) (car ys))
         (cons (car xs) (merge (cdr xs) ys))]
        [else
         (cons (car ys)(merge (cdr ys) xs))]))


;;Split
(define (split xs)
  (define (split-iter i n xs ys)
    (if (= i n)
        (cons ys xs)
        (split-iter (+ i 1) n (cdr xs) (if (null? ys)
                                           (car xs)
                                           (cons (car xs) ys)))))
  (split-iter 0 (ceiling (/ (length xs) 2)) xs '()))


;;Merge sort
(define (mergesort xs)
  (if (null? xs)
      null
      (let ([s (split xs)])
        (if (null? (cdr s))
            xs
            (merge (mergesort (car s))
                   (mergesort (cdr s)))))))
          


;;---------------------------------TESTS---------------------------------

;;Merge tests
(check-within (merge '() '()) '() epsilon "Merge test failed for null null")
(check-within (merge '(1 2 3) '()) '(1 2 3) epsilon "Merge test failed for list null")
(check-within (merge '() '(1 2 3)) '(1 2 3) epsilon "Merge test failed for null list")
(check-within (merge '(1 2 11 11) '(0 2 2 8 15)) '(0 1 2 2 2 8 11 11 15) epsilon "Merge fail")
(check-within (merge '(0 1 2) '(2 2 8 11 12)) '(0 1 2 2 2 8 11 12) epsilon "Merge fail")
(check-within (merge '(1 1) '(2 2 2)) '(1 1 2 2 2) epsilon "Merge fail")
(check-within (merge '(11) '(3 8 13 16)) '(3 8 11 13 16) epsilon "Merge fail")


;;Split tests
(check-within (split '()) '(()) epsilon "Split test failed for null")
(check-within (split '(1 2 3 4 5 6)) '((1 2 3) 4 5 6) epsilon "Split test failed for even NoE")
(check-within (split '(1 2 3 4 5)) '((1 2 3) 4 5) epsilon "Split test failed for uneven NoE")
(check-within (split '(1)) '((1)) epsilon "Split test failed for one element")

;;Merge sort tests
(check-within (mergesort '()) '() epsilon "Mergesort fail for null")
(check-within (mergesort '(1 1)) '(1 1) epsilon "Mergesort fail for one element")
(check-within (mergesort '(4 3 9 1)) '(1 3 4 9) epsilon "Mergesort fail for different numbers")
(check-within (mergesort '(1 1 1 1)) '(1 1 1 1) epsilon "Mergesort fail for same numbers")
(check-within (mergesort '(1 2 3)) '(1 2 3) epsilon "Mergesort fail for sorted list")