#lang racket

; --------------------- ;
; Składnia abstrakcyjna ;
; --------------------- ;
(struct abs (x)        #:transparent)
(struct const (val)    #:transparent)
(struct binop (op l r) #:transparent)
(struct variable ()    #:transparent)

; 2 + 2 * 2
(define 2+2*2 (binop '+ (const 2)
                        (binop '* (const 2)
                                  (const 2))))

; Co to są wyrażenia?
(define (expr? e)
  (match e
    [(variable) true]
    [(abs x) (expr? x)]
    [(const n) (number? n)]
    [(binop op l r) (and (symbol? op) (expr? l) (expr? r))]
    [_ false]))

; Co to są wartości?
(define (value? v)
  (number? v))

(define (op->proc op)
  (match op ['+ +] ['- -] ['* *] ['/ /] ['^ expt]))

(define (eval e)
  (match e
    [(abs x) (if (< x 0) (- x) x)]
    [(const n) n]
    [(binop op l r) ((op->proc op) (eval l) (eval r))]))


;;Zadanie 1

;;; ; konkretna
;;; (+ (/ 8 (+ 2 3)) 10 1)

;;; ; abstrakcyjna
;;; (binop '+
;;;           (binop '/ (const 8) 
;;;                     (binop '+ (const 2) (const 3)))
;;;           (binop '+ (const 10) (const 1)))

; konkretna

;;; (+ 1 2 (* 3 4) 5)

; abstrakcyjna

;;; (binop '+ 
;;;         (const 1)
;;;         (binop '+ (const 2)
;;;                   (binop '+ (binop '*  (const 3) 
;;;                                         (const 4))
;;;                              (const 5))))

; Zadanie 2
(define (square x) (* x x))

(define (cont-frac num den k)
  (define (frac i)
    (if (< i k)
        (binop '/ (const (num i))  (binop '+ (const (den i)) (frac (+ i 1))))
        (binop '/ (const (num i))  (const (den i)))))
  (frac 1))

(define (count-pi-v2 approximation-level)
  (define (num k)
    (if (= k 1)
        1.0
        (square (- (* 2 k) 1))))
  (define (den k)
    6)
  (binop '+ (const 3) (cont-frac num den approximation-level)))

(eval (count-pi-v2 4))

; Zadanie 3

(eval (abs -10))
(eval (binop '^ (const 2) (const 5)))

;;Zadanie 4
;;wersja prostsza
(define (pretty-print e)
  (match  e
    [(const n) (number->string n)]
    [(abs op arg) (string-append "|" (pretty-print arg) "|")]
    [(binop op l r) (string-append "(" (pretty-print l) " "
                                   (symbol->string op) " "
                                   (pretty-print r) ")")])) 

;;Wskazówka: do wersji trudniejszej skorzystać z łączności operatorów
; 2 + ((3 + 5) + 6)
; (2 + 3) + 5 
; 2 + 3 + 5
; 2 ^ (3 ^ 4) 
; (2 ^ 3) ^ 4
; 2 ^ 3 ^ 4
(pretty-print (count-pi-v2 4)) 

;;Zadanie 5
(define (parse q)
  (cond [(number? q) (const q)]
        [(eq? q 'x) (variable)]
        [(and (list? q) (eq? (length q) 3) (symbol? (first q)))
         (binop (first q) (parse (second q)) (parse (third q)))]))

; (a ^ b) ^ c = a ^ (b * c)
; x ^ x
; x ^ x ^ x
(define (∂ f) ;  D(f(x) ^ g(x))  = D(log((E ^ f(x)) ^ g(x))) = D(log (E ^ (f * g)) )
 (match f
    [(const n)      (const 0)]
    [(variable)     (const 1)]
    [(binop '+ g h) (binop '+ (∂ g) (∂ h))]
    [(binop '* g h) (binop '+ (binop '* (∂ g) h))
                              (binop '* g (∂ h))]))  

		