#lang racket
(provide conj conj-left conj-right conj? disj disj-left disj-right disj? neg neg-subf neg? var?)
(define (var? t)
  (symbol? t))

(define (neg? t)
  (and (list? t)
       (= 2 (length t))
       (eq? 'neg (car t))))

(define (conj? t)
  (and (list? t)
       (= 3 (length t))
       (eq? 'conj (car t))))

(define (disj? t)
  (and (list? t)
       (= 3 (length t))
       (eq? 'disj (car t))))

(define (neg opnd)
  (list 'neg opnd))

(define (conj opnd-a opnd-b)
  (list 'conj opnd-a opnd-b))

(define (disj opnd-a opnd-b)
  (list 'disj opnd-a opnd-b))

(define neg-subf second)

(define conj-left second)

(define conj-right third)

(define disj-left second)

(define disj-right third)
