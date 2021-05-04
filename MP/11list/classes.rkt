#lang racket

(require racket/contract)
;;; Zadanie 1
(define/contract (suffixes xs)
    (parametric->/c [a] (-> (listof a) (listof (listof a))))
    (if (null? xs)
        xs
        (cons xs (suffixes  (cdr xs)))))


;;; Zadanie 2
(define (sublists  xs)
(parametric->/c [a] (-> (listof a) (listof (listof a))))
(if (null? xs)
    (list  null)
    (append-map (lambda(ys) (list (cons (car xs) ys) ys))
                (sublists (cdr xs)))))


;;; Zadanie 3

(define/contract (first x y)
(parametric->/c [a b] (-> a b a))
    x)

(define/contract (second x y z)
(parametric->/c [a b c] (-> (-> b c) (-> a b) a c))
 (x (y z)))

(define/contract (third f g)
(parametric->/c [a b c] (-> (-> b c) (-> a b) (-> a c)))
 (lambda (a) (f (g a))))

(define/contract (forth f)
(parametric->/c [a] (-> (-> (-> a a) a) a))
    (f (lambda (x) x)))


;;; Zadanie 4

(define (proc x)
(parametric->/c [a b] (-> a b))
    (proc x))

;;; Zadanie 5

(define (foldl-map f a xs)
(parametric->/c [e acc c] (-> (-> e acc (cons/c c acc)) acc (listof e) 
                                (cons/c (listof c) acc)))
    (define (it a xs ys)
        (if (null? xs)
            (cons (reverse  ys) a)
            (let [(p (f (car xs) a))]
             (it (cdr p) (cdr xs) (cons (car p) ys)))))
    (it a xs null))

;;; Zadanie 6

(struct const    (val)      #:transparent)
(struct binop    (op l r)   #:transparent)
(struct let-expr (x e1 e2)  #:transparent)
(struct var-expr (x)        #:transparent)


(define expr/c 
  (flat-rec-contract expr
        (struct/c const number?)
        (struct/c binop symbol? expr expr)
        (struct/c let-expr symbol? expr expr)
        (struct/c var-expr symbol?)))

(define (value? v)
  (number? v))

(define (expr? e)
  (match e
    [(const n) (number? n)]
    [(binop op l r) (and (symbol? op) (expr? l) (expr? r))]
    [(var-expr x) (symbol? x)]
    [(let-expr x e1 e2) (and (symbol? x) (expr? e1) (expr? e2))]
    [_ false]))


(define/contract (subst e1 x e2)
(-> expr/c symbol? expr/c expr/c)
  (match e2
    [(var-expr y) (if (eq? x y) e1 (var-expr y))]
    [(const n) (const n)]
    [(binop op l r)
     (binop op (subst e1 x l) (subst e1 x r))]
    [(let-expr y e3 e4)
     (let-expr y (subst e1 x e3) 
                 (if (eq? x y) e4 (subst e1 x e4)))]))

(define/contract (eval e)
  (-> expr/c value?)
  (match e
    [(const n) n]
    [(binop op l r) ((op->proc op) (eval l) (eval r))]
    [(let-expr x e1 e2)
     (eval (subst (const (eval e1)) x e2))]))