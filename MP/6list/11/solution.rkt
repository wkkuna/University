;;Wiktoria Kuna 316418
#lang racket
(provide (struct-out const) (struct-out binop) rpn->arith)

;; -------------------------------
;; Wyrazenia w odwr. not. polskiej
;; -------------------------------

(define (rpn-expr? e)
  (and (list? e)
       (pair? e)
       (andmap (lambda (x) (or (number? x) (member x '(+ - * /))))
               e)))

;; ----------------------
;; Wyrazenia arytmetyczne
;; ----------------------

(struct const (val)    #:transparent)
(struct binop (op l r) #:transparent)

(define (arith-expr? e)
  (match e
    [(const n) (number? n)]
    [(binop op l r)
     (and (symbol? op) (arith-expr? l) (arith-expr? r))]
    [_ false]))

;; ----------
;; Kompilacja
;; ----------

(define (rpn->arith-am e xs)
  (cond [(null? e) (top xs)]
        [(number? (car e))
         (rpn->arith-am (cdr e)
                        (push (const (car e)) xs))]
        [(symbol? (car e))
         (let ([arg2 (top xs)]
               [arg1 (top (pop xs))])
         (rpn->arith-am (cdr e)
                        (push (binop (car e) arg1 arg2)
                              (pop (pop xs)))))])) 

(define (rpn->arith e)
 (rpn->arith-am e empty-stack))

;; ---------------
;; Stos i operacje
;; ---------------

(struct stack (xs))
  
(define empty-stack (stack null))
(define (empty-stack? s) (null? (stack-xs s)))
(define (top s) (car (stack-xs s)))
(define (push a s) (stack (cons a (stack-xs s))))
(define (pop s) (stack (cdr (stack-xs s))))
    
;; --------------------------
;; Testy i operacje do testów
;; --------------------------
    
(module+ test
  (require rackunit)

  (define (arith->rpn e)
    (match e
      [(const n) (list n)]
      [(binop op l r) (append (arith->rpn l)
                              (arith->rpn r)
                              (list op))]))

  (let ([x (const 1)]
        [y (binop '+ (const 3) (const 6))]
        [z (binop '+ (binop '* (const 3) (binop '- (const 1) (const 10)))
                     (binop '/ (const 4) (binop '+ (const 2) (const 1))))]
        [t (binop '/ (const 5)
                     (binop '- (const 2)
                               (binop '* (const 2) (const 6))))])
    (check-equal? (rpn->arith (arith->rpn x)) x "Constant rpn->arith failed")
    (check-equal? (rpn->arith (arith->rpn y)) y "One operator rpn->arith failed")
    (check-equal? (rpn->arith (arith->rpn z)) z "rpn->arith failed")
    (check-equal? (rpn->arith (arith->rpn t)) t "rpn->arith failed")))
