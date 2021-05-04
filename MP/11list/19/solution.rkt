#lang racket
(provide (contract-out
          [with-labels with-labels/c]
          [foldr-map foldr-map/c]
          [pair-from pair-from/c ]))

(provide with-labels/c foldr-map/c pair-from/c)

;; 19.1
(define with-labels/c
  (parametric->/c [a b] (-> (-> a b) (listof a) (listof (list/c b a)))))

(define (with-labels f xs)
  (if (null? xs)
      null
      (cons (list (f (car xs)) (car xs))
            (with-labels f (cdr xs)))))

;; 19.2
(define foldr-map/c
  (parametric->/c [e acc c] (-> (-> e acc (cons/c c acc)) acc (listof e) 
                                (cons/c (listof c) acc))))
  
(define (foldr-map f a xs)
  (define (it a xs ys)
    (if (null? xs)
        (cons ys a)
        (let [(p (f (car xs) a))]
          (it (cdr p) (cdr xs) (cons (car p) ys)))))
  (it a (reverse xs) null))


;; 19.3

(define pair-from/c
  (parametric->/c [a b c] (-> (-> a b) (-> a c) (-> a (cons/c b c)))))

(define (pair-from f g)
  (lambda (x) (cons (f x) (g x))))