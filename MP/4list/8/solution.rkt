#lang racket
(require "leftist.rkt")
(provide heapsort)
;;---------------------------------------HEAP-SORT----------------------------------------
(define (heapsort xs)
  (define (onto-heap ys h)
    (if (null? ys)
        h
        (onto-heap (cdr ys) (heap-insert (make-elem (car ys) (car ys)) h))))
  
  (define (off-heap h)
    (if (heap-empty? h)
        '()
        (cons (elem-val (heap-min h)) (off-heap (heap-pop h) ))))
  (off-heap (onto-heap xs 'leaf)))

;;----------------------------------------------------------------------------------------

;;; check that a list is sorted (useful for longish lists)
(define (sorted? xs)
  (cond [(null? xs)              true]
        [(null? (cdr xs))        true]
        [(<= (car xs) (cadr xs)) (sorted? (cdr xs))]
        [else                    false]))


;;------------------------------------------TESTS------------------------------------------
(require rackunit)
;;Sort-test
(check-true (sorted? (heapsort '())) "Heapsort failed for null")
(check-true (sorted? (heapsort '(2))) "Heapsort failed for one element")
(check-true (sorted? (heapsort '(5 2))) "Heapsort failed for two different elements")
(check-true (sorted? (heapsort '(2 2))) "Heapsort failed for two equal elements")
(check-true (sorted? (heapsort '(0 1 2 2 6 8 11))) "Heapsort failed for sorted list")
(check-true (sorted? (heapsort '(43 1 0 232 88 91 2))) "Heapsort failed unsorted list (1)")
(check-true (sorted? (heapsort '(9 8 7 6 2))) "Heapsort failed unsorted list (2)")
(check-true (sorted? (heapsort '(0 9 2525 3 2 123 78 2))) "Heapsort failed unsorted list (3)")
(check-true (sorted? (heapsort '(0 9 4 5 6 287 17 26 7 674 8 98 6 244 4 44 2323 536 90 87 33 76 1 3 6 8 3 54 78 51 77 859 0 16  0 0 0 0 9 23 46 6 72 52 5 3 2 123 78 2))) "Heapsort failed quite long list (4)")
