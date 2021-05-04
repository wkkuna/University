#lang racket

;;zadanie1

; --------- ;
; Wyrazenia ;
; --------- ;

(struct const         (val)      #:transparent)
(struct binop         (op l r)   #:transparent)
(struct var-expr      (id)       #:transparent)
(struct let-expr      (id e1 e2) #:transparent)
(struct if-expr       (eb et ef) #:transparent)
(struct boolean-expr? (val)      #:transparent)
(struct number-expr?  (val)      #:transparent)
(struct and-expr      (e1 e2)    #:transparent)
(struct or-expr       (e1 e2)    #:transparent)


(define (expr? e)
  (match e
    [(const n) (or (number? n)
                   (eq? n 'true)
                   (eq? n 'false))] ; <----------------- !!!
    [(binop op l r) (and (symbol? op) (expr? l) (expr? r))]
    [(var-expr x) (symbol? x)]
    [(let-expr x e1 e2)
     (and (symbol? x) (expr? e1) (expr? e2))]
     [(number-expr? x) (expr? x)]
     [(boolean-expr? x) (expr? x)]
    [(if-expr eb et ef) ; <--------------------------------------- !!!
     (and (expr? eb) (expr? et) (expr? ef))]
    [(and-expr e1 e2) 
      (and (expr? e1) (expr? e2))]
    [(or-expr e1 e2) 
      (and (expr? e1) (expr? e2))]
    [_ false]))

(define (parse q)
  (cond
    [(number? q) (const q)]
    [(eq? q 'true)  (const 'true)]  ; <---------------------------- !!!
    [(eq? q 'false) (const 'false)] ; <---------------------------- !!!
    [(symbol? q) (var-expr q)]
    [(and (list? q) (= 3 (length q)) (equal? 'and (first q)))
       (and-expr (parse (second q)) (parse (third q)))]
    [(and (list? q) (= 3 (length q)) (equal? 'or (first q)))
       (or-expr (parse (second q)) (parse (third q)))]
    [(and (list? q) (eq? (length q) 3) (eq? (first q) 'let))
     (let-expr (first (second q))
               (parse (second (second q)))
               (parse (third q)))]
    [(and (list? q) (eq? (length q) 4) (eq? (first q) 'if)) ; <--- !!!
     (if-expr (parse (second q))
              (parse (third q))
              (parse (fourth q)))]
    [(and (list? q) (= 2 (length q)) (equal? 'number? (first q)))
        (number-expr? (parse (second q)))]
    [(and (list? q) (= 2 (length q)) (equal? 'boolean? (first q)))
        (boolean-expr? (parse (second q)))]
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
  (number? v))

(define (op->proc op)
  (match op ['+ +] ['- -] ['* *] ['/ /] ['% modulo] ; <----------- !!!
            ['= =] ['> >] ['>= >=] ['< <] ['<= <=])) 

(define (eval-env e env)
  (match e
    [(const n) 
       (cond
       [(number? n) n]
       [(eq? n 'false) false]
       [(eq? n 'true) true])]
    [(number-expr? x) (number? (eval-env x env))]
    [(boolean-expr? x) (boolean? (eval-env x env))]       
    [(binop op l r) ((op->proc op) (eval-env l env)
                                   (eval-env r env))]
    [(let-expr x e1 e2)
     (eval-env e2 (env-add x (eval-env e1 env) env))]
    [(var-expr x) (env-lookup x env)]
    [(if-expr eb et ef) (if (eval-env eb env) ; <----------------- !!!
                            (eval-env et env)
                            (eval-env ef env))]
    [(and-expr e1 e2)   (and (eval-env e1 env) (eval-env e2 env))]
    [(or-expr e1 e2)    (or  (eval-env e1 env) (eval-env e2 env))]))

(define (eval e) (eval-env e env-empty))

