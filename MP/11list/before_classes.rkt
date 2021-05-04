#lang racket
(require racket/contract)
;; ------------------- ZADANIE 1 -------------------

(define/contract (suffixes xs)
  (parametric->/c [a] (-> (listof a) (listof (listof a))))
  (if (null? xs)
      null
      (cons xs (suffixes (cdr xs)))))

;; ------------------- ZADANIE 2 -------------------

(define/contract (sublists  xs)
  (parametric->/c [a] (-> (listof a) (listof (listof a))))
  (if (null? xs)
      (list  null)
      (append-map (lambda (ys) (list (cons (car xs) ys) ys))
                  (sublists (cdr xs)))))

;; ------------------- ZADANIE 3 -------------------

;(parametric->/c [a b] (-> a #neg b #neg a #pos))
;(parametric->/c [a b c] (-> (-> a #pos b #pos c #neg) (-> a #pos b #neg) a #neg c #pos))
;(parametric->/c [a b c] (-> (-> b #pos c #neg) (-> a #pos b #neg) (-> a #neg c #pos)))
;(parametric->/c [a] (-> (-> (-> a #neg a #pos) a #neg) a #pos))

(define/contract (ex1 x y)
  (parametric->/c [a b] (-> a b a))
  x)

(define/contract (ex2 f g x)
  (parametric->/c [a b c] (-> (-> a b c) (-> a b) a c))
  (f x (g x)))

(define/contract (ex3 f g)
  (parametric->/c [a b c] (-> (-> b c) (-> a b) (-> a c)))
  (lambda (x) (f (g x))))

(define (id x)
  (parametric->/c [a] (-> a a))
  x)

(define (ex4 f)
  (parametric->/c [a] (-> (-> (-> a a) a) a))
  (f f))
  

;; ------------------- ZADANIE 4 -------------------

(define/contract (proc x)
  (parametric->/c [a b] (-> a b))
  (proc x))

;; ------------------- ZADANIE 5 -------------------

(define (foldl-map f a xs)
  (parametric->/c [e acc c]
                  (-> (-> e acc (cons/c c acc)) e acc (cons/c (listof c) acc)))
  (define (it a xs ys)
    (if (null? xs)
        (cons (reverse  ys) a)
        (let [(p (f (car xs) a))]
          (it (cdr p)
              (cdr xs)
              (cons (car p) ys)))))
  (it a xs null))

