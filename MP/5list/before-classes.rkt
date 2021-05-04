#lang racket
(define (var? t)
  (symbol? t))

(define (operator? t)
  (or (eq? t 'neg)
      (eq? t 'conj)
      (eq? t 'disj)))

(define (neg? t)
  (and (list? t)
       (= 2 (length t))
       (eq?'neg (car t))))

(define (conj? t)
  (and (list? t)
       (= 3 (length t))
       (eq?'conj (car t))))

(define (disj? t)
  (and (list? t)
       (= 3 (length t))
       (eq?'disj (car t))))

(define (prop? f)
  (or (var? f)
      (and(neg? f)(prop? (neg-subf f)))
      (and(disj? f)(prop? (disj-left f))(prop? (disj-rght f)))
      (and(conj? f)(prop? (conj-left f))(prop? (conj-rght f)))))

;;1
(define (neg operand)
  (list 'neg operand))

(define (conj operand-p operand-q)
  (list 'conj operand-p operand-q))

(define (disj operand-p operand-q)
  (list 'disj operand-p operand-q))

(define (neg-subf t)
  (second t))

(define (conj-left t)
  (second t))
  
(define (conj-rght t)
  (third t))

(define (disj-left t)
  (second t))
  
(define (disj-rght t)
  (third t))

;;2
;;  Dla dowolnej formuł rachunku zdań x y, jeśli zachodzi:
;;  1. (prop? x) oraz (prop? y)
;;  2. oraz jeśli dla dowolnych zmiennych p q zachodzi (prop? (neg p)) (prop? (conj p q)) (prop? (disj p q))

;;3
(define (free-vars xs)
  (filter (lambda (x) (and
                       (var? x)
                       (not (operator? x))))
          (flatten xs)))

;;4
(define (gen-vals  xs)
  (if (null? xs)
      (list  null)
      (let* ((vss   (gen-vals (cdr xs)))
             (x     (car xs))
             (vst   (map (lambda(vs) (cons (list x true)   vs)) vss))
             (vsf   (map (lambda(vs) (cons (list x false) vs)) vss)))
        (append  vst  vsf))))

;(apply (lambda (x) (apply + x)) '((1 2) (3 4)))

;(define (eval-formula formula values))
  

