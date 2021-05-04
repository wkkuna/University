;Wiktoria Kuna 316418
#lang racket

;; ---------------
;; Jezyk wejsciowy
;; ---------------
(provide (struct-out const) (struct-out binop) (struct-out var-expr)
         (struct-out let-expr) (struct-out pos) (struct-out var-free)
         (struct-out var-bound) annotate-expression)

(struct pos (file line col)     #:transparent)
  
(struct const    (val)          #:transparent)
(struct binop    (op l r)       #:transparent)
(struct var-expr (id)           #:transparent)
(struct let-expr (loc id e1 e2) #:transparent)

(define (expr? e)
  (match e
    [(const n)      (number? n)]
    [(binop op l r) (and (symbol? op) (expr? l) (expr? r))]
    [(var-expr x)   (symbol? x)]
    [(let-expr loc x e1 e2)
     (and (pos? loc) (symbol? x) (expr? e1) (expr? e2))]
    [_ false]))

(define (make-pos s)
  (pos (syntax-source s)
       (syntax-line   s)
       (syntax-column s)))

(define (parse e)
  (let ([r (syntax-e e)])
    (cond
      [(number? r) (const r)]
      [(symbol? r) (var-expr r)]
      [(and (list? r) (= 3 (length r)))
       (match (syntax-e (car r))
         ['let (let* ([e-def (syntax-e (second r))]
                      [x     (syntax-e (first e-def))])
                 (let-expr (make-pos (first e-def))
                           (if (symbol? x) x (error "parse error!"))
                           (parse (second e-def))
                           (parse (third r))))]
         [op   (binop op (parse (second r)) (parse (third r)))])]
      [else (error "parse error!")])))

;; ---------------
;; Jezyk wyjsciowy
;; ---------------

(struct var-free  (id)     #:transparent)
(struct var-bound (pos id) #:transparent)

(define (expr-annot? e)
  (match e
    [(const n)         (number? n)]
    [(binop op l r)    (and (symbol? op) (expr-annot? l) (expr-annot? r))]
    [(var-free x)      (symbol? x)]
    [(var-bound loc x) (and (pos? loc) (symbol? x))]
    [(let-expr loc x e1 e2)
     (and (pos? loc) (symbol? x) (expr-annot? e1) (expr-annot? e2))]
    [_ false]))

; ------------;
; Środowisko  ;
; ------------;

(struct environ (xs))

(define env-empty (environ null))

(define (env-add x v env)
  (environ (cons (cons x v) (environ-xs env))))

(define (env-lookup x env)
  (define (assoc-lookup xs)
    (cond [(null? xs) #f]
          [(eq? x (car (car xs))) (cdr (car xs))]
          [else (assoc-lookup (cdr xs))]))
  (assoc-lookup (environ-xs env)))

; ------------;
; annot-expr  ;
; ------------;

(define (annotate-expression e)
  (define (ann-expr-env e env)
    (match e
      [(const n) (const n)]
      [(binop op l r) (binop op (ann-expr-env l env) (ann-expr-env r env))]
      [(var-expr id)
       (let ([x (env-lookup id env)])
         (if x
             (var-bound x id)
             (var-free id)))]
      [(let-expr loc x e1 e2)
       (let-expr loc x (ann-expr-env e1 env)
                 (ann-expr-env e2 (env-add x loc env)))]))
  (ann-expr-env e env-empty))


(module+ test
  
  (define test0
    #'(+ x y))

  (define test
    #'(let [w 5]
        (let [z x]
          (let [y (* zx x)]
            (* y (* zx (* w z)))))))

  (define test2
    #'(let [x 2]
        (* (let [x 3] x) x))))
