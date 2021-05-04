#lang racket
(provide parse eval)

; --------- ;
; Wyrazenia ;
; --------- ;

(struct const      (val)      #:transparent)
(struct binop      (op l r)   #:transparent)
(struct var-expr   (id)       #:transparent)
(struct let-expr   (id e1 e2) #:transparent)
(struct if-expr    (eb et ef) #:transparent)
(struct cons-expr  (e1 e2)    #:transparent)
(struct car-expr   (e)        #:transparent)
(struct cdr-expr   (e)        #:transparent)
(struct null-expr  ()         #:transparent)
(struct null?-expr (e)        #:transparent)
(struct app        (f e)      #:transparent) 
(struct lam        (id e)     #:transparent) 

(define (expr? e)
  (match e
    [(const n) (or (number? n) (boolean? n))]
    [(binop op l r) (and (symbol? op) (expr? l) (expr? r))]
    [(var-expr x) (symbol? x)]
    [(let-expr x e1 e2)
     (and (symbol? x) (expr? e1) (expr? e2))]
    [(if-expr eb et ef)
     (and (expr? eb) (expr? et) (expr? ef))]
    [(cons-expr e1 e2) (and (expr? e1) (expr? e2))]
    [(car-expr e) (expr? e)]
    [(cdr-expr e) (expr? e)]
    [(null-expr) true]
    [(null?-expr e) (expr? e)]
    [(app f e) (and (expr? f) (expr? e))]
    [(lam id e) (and (symbol? id) (expr? e))]
    [_ false]))

(define (parse q)
  (cond
    [(number? q) (const q)]
    [(eq? q 'true)  (const true)]
    [(eq? q 'false) (const false)]
    [(eq? q 'null)  (null-expr)]
    [(symbol? q) (var-expr q)]
    [(and (list? q) (eq? (length q) 2) (eq? (first q) 'null?))
     (null?-expr (parse (second q)))]
    [(and (list? q) (eq? (length q) 3) (eq? (first q) 'cons))
     (cons-expr (parse (second q))
                (parse (third q)))]
    [(and (list? q) (eq? (length q) 2) (eq? (first q) 'car))
     (car-expr (parse (second q)))]
    [(and (list? q) (eq? (length q) 2) (eq? (first q) 'cdr))
     (cdr-expr (parse (second q)))]
    [(and (list? q) (eq? (length q) 3) (eq? (first q) 'let))
     (let-expr (first (second q))
               (parse (second (second q)))
               (parse (third q)))]
    [(and (list? q) (eq? (length q) 4) (eq? (first q) 'if))
     (if-expr (parse (second q))
              (parse (third q))
              (parse (fourth q)))]
    [(and (list? q) (eq? (length q) 3) (eq? (first q) 'lambda))
     (parse-lam (second q) (third q))]
    [(and (list? q) (pair? q) (not (op->proc (car q))))
     (parse-app q)]
    [(and (list? q) (eq? (length q) 3) (symbol? (first q)))
     (binop (first q)
            (parse (second q))
            (parse (third q)))]))

(define (parse-app q)
  (define (parse-app-accum q acc)
    (cond [(= 1 (length q)) (app acc (parse (car q)))]
          [else (parse-app-accum (cdr q) (app acc (parse (car q))))]))
  (parse-app-accum (cdr q) (parse (car q))))

(define (parse-lam pat e)
  (cond [(= 1 (length pat))
         (lam (car pat) (parse e))]
        [else
         (lam (car pat) (parse-lam (cdr pat) e))]))

; ---------- ;
; Srodowiska ;
; ---------- ;

(struct environ (xs) #:transparent)

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

(struct clo (id e env) #:transparent)
(struct lazy-clo (e env) #:transparent)


(define (value? v)
  (or (number? v)
      (boolean? v)
      (and (pair? v) (value? (car v)) (value? (cdr v)))
      (null? v)
      (clo? v)
      (lazy-clo? v))) ; <----------------------------------------------!!!

(define (op->proc op)
  (match op ['+ +] ['- -] ['* *] ['/ /] ['% modulo]
    ['= =] ['> >] ['>= >=] ['< <] ['<= <=]
    ['and (lambda (x y) (and x y))]
    ['or  (lambda (x y) (or  x y))]
    [_ false]))

(define (eval-env e env)
  (match e
    [(const n) n]
    [(binop op l r) ((op->proc op) (eval-env l env)
                                   (eval-env r env))]
    [(let-expr x e1 e2)
     (eval-env e2 (env-add x (eval-env e1 env) env))]
    
    [(var-expr x) ; <--------------------------------------------------!!!
     (match (env-lookup x env)
       [(lazy-clo e env) (eval-env e env)]
       [val val])]
    
    [(if-expr eb et ef) (if (eval-env eb env)
                            (eval-env et env)
                            (eval-env ef env))]
    
    [(cons-expr e1 e2) ; <---------------------------------------------!!!
     (cons (lazy-clo e1 env)
           (lazy-clo e2 env))]
    
    [(car-expr e) ; <--------------------------------------------------!!!
     (match (eval-env e env)
       [(cons (lazy-clo e env) whatever)
        (eval-env e env)])]

    [(cdr-expr e) ; <--------------------------------------------------!!!
     (match (eval-env e env)
       [(cons whatever (lazy-clo e env))
        (eval-env e env)])]
    
    [(null-expr) null]
    [(null?-expr e) (null? (eval-env e env))]
    [(lam x e) (clo x e env)]
    
    [(app f e) ; <-----------------------------------------------------!!!
     (match (eval-env f env)
       [(clo x body fun-env)
        (eval-env body (env-add x (lazy-clo e env) fun-env))])]))

(define (eval e) (eval-env e env-empty))

(module+ test
  (require rackunit)

  (define t0
    (eval (parse '((lambda (x y) x) 1 (/ 1 0)))))
  (define t1
    (eval (parse '(let [if-fun (lambda (b t e) (if b t e))]
                    (if-fun  true 4 (/ 5 0))))))
  (define t2
    (eval (parse '(car (cons (+ 2 2) (/ 5 0))))))
  (define t3
    (eval (parse
           '(car (cdr (cdr (cons (/ 5 0) (cons not (cons (+ 1 1) (cons quite interesting))))))))))
  (define t4
    (eval (parse
           '(car (cdr (cons 9 (cons 8 (+ basically nothing))))))))
  (define t5
    (eval (parse
           '(let [x 4] (let [f (lambda (y) (+ x y))] (let [x 0] (f 10)))))))

  (check-equal? t0 1 "t0 FAILED")
  (check-equal? t1 4 "t1 FAILED")
  (check-equal? t2 4 "t2 FAILED")
  (check-equal? t3 2 "t3 FAILED")
  (check-equal? t4 8 "t4 FAILED")
  (check-equal? t5 14 "t5 FAILED"))
