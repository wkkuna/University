#lang racket
;;Wykład
(struct const (val)    #:transparent)
(struct binop (op l r) #:transparent)
(struct nonbinop (op arg) #:transparent)
; 2 + 2 * 2
(define 2+2*2 (binop '+ (const 2)
                        (binop '* (const 2)
                                  (const 2))))

; Co to są wyrażenia?
(define (expr? e)
  (match e
    [(const n) (number? n)]
    [(binop op l r) (and (symbol? op) (expr? l) (expr? r))]
    [(nonbinop op arg) (and (symbol? op) (expr? arg))]
    [_ false]))

; Co to są wartości?
(define (value? v)
  (number? v))

(define (op->proc op)
  (match op ['+ +] ['- -] ['* *] ['/ /] ['^ expt] [^abs abs]))

(define (eval e)
  (match e
    [(const n) n]
    [(binop op l r) ((op->proc op) (eval l) (eval r))]
    [(nonbinop op arg) ((op->proc op) (eval arg))]))

; ------------------------- ;
; Trochę składni konkretnej ;
; ------------------------- ;

(define (parse q)
  (cond [(number? q) (const q)]
        [(and (list? q) (eq? (length q) 3) (symbol? (first q)))
         (binop (first q) (parse (second q)) (parse (third q)))]))
;------------------------------------------1------------------------------------------
;;1.1
; (+ (/ 8 (+ 2 3)) 10 1)
; (binop '+ (binop '+ (binop '/ (const 8)
;                            (binop '+ (const 2) (const 3)))
;                  (const 10))
;        (const 1))
;;1.2
; (+ 1 2 (* 3 4) 5)
; (binop '+ (binop '+ (binop '+ (const 1) (const 2)) (binop '* (const 3) (const 4))) (const 5))
;------------------------------------------2------------------------------------------
(define (square x) (* x x))

(define (count-pi-v2 approximation-level)
  (define (num k)
    (if (= k 1)
        1.0
        (square (- (* 2 k) 1))))
  (define (den k)
     6)
  (binop '+ (const 3) (cont-frac-expr num den approximation-level)))


(define (cont-frac-expr num den k)
  (define (frac i)
    (if (< i k)
        (binop '/ (const (num i)) (binop '+ (const (den i)) (frac (+ i 1))))
        (binop '/ (const (num i)) (const (den i)))))
  (frac 1))


;------------------------------------------4------------------------------------------
(struct stack (xs))

(define empty-stack (stack null))
(define (empty-stack? s) (null? (stack-xs s)))
(define (top s) (car (stack-xs s)))
(define (push a s) (stack (cons a (stack-xs s))))
(define (pop s) (stack (cdr (stack-xs s))))


(define (pretty-print e)
  (match  e
    [(const n) (number->string n)]
    [(nonbinop op arg) (string-append "|" (pretty-print arg) "|")]
    [(binop op l r) (string-append "(" (pretty-print l) " "
                                   (symbol->string op) " "
                                   (pretty-print r) ")")])) 
