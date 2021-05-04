#lang racket
(define (treesort xs)
    (define (aux t xs)
        (if (null? xs)
            t
            (aux (insert (car xs)) (cdr xs)))
    (flatten (aux 'leaf xs))))