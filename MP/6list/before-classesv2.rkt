#lang racket

(struct const (val)    #:transparent)
(struct binop (op l r) #:transparent)
(struct nonbinop (op arg) #:transparent)
(struct variable ()    #:transparent)

; 2 + 2 * x
(define 2+2*x (binop '+ (const 2)
                        (binop '* (const 2)
                                  (variable))))

(define (expr? e)
  (match e
    [(variable)     true]
    [(const n)      (number? n)]
    [(binop op l r) (and (symbol? op) (expr? l) (expr? r))]
    [(nonbinop op arg) (and (symbol? op) (expr? arg))]
    [_              false]))

; Wartosci
(define (value? v)
  (number? v))

(define (op->proc op)
  (match op ['+ +] ['- -] ['* *] ['/ /] ['^ expt]))

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
        [(eq? q 'x) (variable)]
        [(and (list? q) (eq? (length q) 3) (symbol? (first q)))
         (binop (first q) (parse (second q)) (parse (third q)))]
        [(and (list? q) (eq? (length q) 2) (symbol? (first q)))
         (nonbinop (first q) (parse (second q)))]))

(define (∂ e)
  (match e
    [(const _) 0]
    [(variable) 1]
    [(binop op l r) (cond [(eq? (op->proc op) '+)
                           (binop (op->proc op) (∂ l) (∂ r))]
                          [else (binop '+ (binop '* (∂ l) r) (binop '* l (∂ r)))])]))