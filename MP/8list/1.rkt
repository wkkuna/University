#lang racket

; Do let-env.rkt dodajemy wartosci boolowskie
;
; Miejsca, ktore sie zmienily oznaczone sa przez !!!

; --------- ;
; Wyrazenia ;
; --------- ;

(struct const    (val)      #:transparent)
(struct binop    (op l r)   #:transparent)
(struct var-expr (id)       #:transparent)
(struct let-expr (id e1 e2) #:transparent)
(struct if-expr  (eb et ef) #:transparent)

(define (expr? e)
  (match e
    [(const n) (or (number? n) (boolean? n))] ; <----------------- !!!
    [(binop op l r) (and (symbol? op) (expr? l) (expr? r))]
    [(var-expr x) (symbol? x)]
    [(let-expr x e1 e2)
     (and (symbol? x) (expr? e1) (expr? e2))]
    [(if-expr eb et ef) ; <--------------------------------------- !!!
     (and (expr? eb) (expr? et) (expr? ef))]
    [_ false]))

(define (parse q)
  (cond
    [(number? q) (const q)]
    [(eq? q 'true)  (const 'true)]  ; <---------------------------- !!!
    [(eq? q 'false) (const 'false)] ; <---------------------------- !!!
    [(symbol? q) (var-expr q)]
    [(and (list? q) (eq? (length q) 3) (eq? (first q) 'let))
     (let-expr (first (second q))
               (parse (second (second q)))
               (parse (third q)))]
    [(and (list? q) (eq? (length q) 4) (eq? (first q) 'if)) ; <--- !!!
     (if-expr (parse (second q))
              (parse (third q))
              (parse (fourth q)))]
    [(and (list? q) (eq? (length q) 3) (symbol? (first q)))
     (binop (first q)
            (parse (second q))
            (parse (third q)))]))

(define (test-parse) (parse '(let [x (+ 2 2)] (+ x 1))))

; ---------- ;
; Srodowiska ;
; ---------- ;

(struct environ (xs))

(define env-empty (environ null))
(define (env-add x v env)
  (environ (cons (cons x v) (environ-xs env))))
(define (env-lookup x env)
  (define (assoc-lookup xs)
    (cond [(null? xs) (error "Unknown identifier" x)]
          [(eq? x (car (car xs))) (cdr (car xs))]
          [else (assoc-lookup (cdr xs))]))
  (assoc-lookup (environ-xs env)))

; --------- ;
; Ewaluacja ;
; --------- ;

(define (value? v)
  (or (number? v) (bool? v)))

(define (op->proc op)
  (match op ['+ +] ['- -] ['* *] ['/ /] ['% modulo] ; <----------- !!!
            ['= =] ['> >] ['>= >=] ['< <] ['<= <=]
            ['and (lambda (x y) (and x y))]
            ['or  (lambda (x y) (or  x y))]))

(define (eval-env e env)
  (match e
    [(const n)
     (cond [(eq? n 'true)  1]
           [(eq? n 'false) 0]
           [else           n])]
    [(binop op l r) ((op->proc op) (eval-env l env)
                                   (eval-env r env))]
    [(let-expr x e1 e2)
     (eval-env e2 (env-add x (eval-env e1 env) env))]
    [(var-expr x) (env-lookup x env)]
    [(if-expr eb et ef) (if (eval-env eb env) ; <----------------- !!!
                            (eval-env et env)
                            (eval-env ef env))]))

(define (eval e) (eval-env e env-empty))

(define program
  '(if (or (< (% 123 10) 5)
           true)
       (+ 2 3)
       (/ 2 0)))

(define (test-eval) (eval (parse program)))
