#lang racket

; Do fun.rkt dodajemy rekurencyjne let-y
;
; Miejsca, ktore sie zmienily oznaczone sa przez !!!

; --------- ;
; Wyrazenia ;
; --------- ;

(struct const       (val)      #:transparent)
(struct binop       (op l r)   #:transparent)
(struct var-expr    (id)       #:transparent)
(struct let-expr    (id e1 e2) #:transparent)
(struct letrec-expr (id e1 e2) #:transparent) ; <----------------- !!!
(struct if-expr     (eb et ef) #:transparent)
(struct cons-expr   (e1 e2)    #:transparent)
(struct car-expr    (e)        #:transparent)
(struct cdr-expr    (e)        #:transparent)
(struct null-expr   ()         #:transparent)
(struct null?-expr  (e)        #:transparent)
(struct app         (f e)      #:transparent)
(struct lam         (id e)     #:transparent)
(struct quote-expr  (e)        #:transparent)
(struct read-ac     ()         #:transparent)
(struct display-ac  (e)        #:transparent)
(struct begin-expr  (es)       #:transparent)

(define (op->proc op)
  (match op ['+ +] ['- -] ['* *] ['/ /] ['% modulo]
            ['= =] ['> >] ['>= >=] ['< <] ['<= <=]
            ['and (lambda (x y) (and x y))]
            ['or  (lambda (x y) (or  x y))]
            [_ false]))

(define (expr? e)
  (match e
    [(const n) (or (number? n) (boolean? n))]
    [(binop op l r) (and (symbol? op) (expr? l) (expr? r))]
    [(var-expr x) (symbol? x)]
    [(let-expr x e1 e2)
     (and (symbol? x) (expr? e1) (expr? e2))]
    [(letrec-expr x e1 e2) ; <------------------------------------ !!!
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
    [(quote-expr e) #t]
    [(read-ac) #t]
    [(display-ac e) (expr? e)]
    [_ false]))

(define (parse q)
  (cond
    [(number? q) (const q)]
    [(eq? q 'true)  (const true)]
    [(eq? q 'false) (const false)]
    [(eq? q 'null)  (null-expr)]
    
    [(and (list? q) (eq? (length q) 2) (eq? (first q) 'display))
     (display-ac (parse (second q)))]

    [(and (list? q) (eq? (length q) 1) (eq? (first q) 'read))
     (read-ac)]
    
    [(and (list? q) (eq? (length q) 2) (eq? (first q) 'quote) (list? (second q)))
     (quote-expr (second q))]
    [(symbol? q) (var-expr q)]
    [(and (list? q) (eq? (length q) 2) (eq? (first q) 'null?))
     (null?-expr (parse (second q)))]

    [(and (list? q) (eq? (length q) 3) (eq? (first q) 'letrec*))
     (desugar-letrec* (second q) (third q))]
    
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
    [(and (list? q) (eq? (length q) 3) (eq? (first q) 'letrec)) ; <!!!
     (letrec-expr (first (second q))
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

(define (de-let es)
  (if (null? es)
      null
      (

(define (desugar-letrec* es e2)
  (if (null? es)
      (parse e2)
      (let ([sym (caar es)]
            [val (cadar es)])
      (letrec-expr sym (parse val)
                   (desugar-letrec* (cdr es) e2)))))

(define (parse-app q)
  (define (parse-app-accum q acc)
    (cond [(= 1 (length q)) (app acc (parse (car q)))]
          [else (parse-app-accum  (cdr q) (app acc (parse (car q))))]))
  (parse-app-accum (cdr q) (parse (car q))))

(define (parse-lam pat e)
  (cond [(= 1 (length pat))
         (lam (car pat) (parse e))]
        [else
         (lam (car pat) (parse-lam (cdr pat) e))]))

; ---------- ;
; Srodowiska ;
; ---------- ;

(struct blackhole () #:transparent) ; <------------------------- !!!
(struct environ (xs) #:transparent)

(define env-empty (environ null))
(define (env-add x v env)
  (environ (cons (mcons x v) (environ-xs env)))) ; <-------------- !!!
(define (env-lookup x env)
  (define (assoc-lookup xs)
    (cond [(null? xs) (error "Unknown identifier" x)]
          [(eq? x (mcar (car xs))) ; <---------------------------- !!!
             (match (mcdr (car xs))
               [(blackhole) (error "Stuck forever in a black hole!")]
               [x x])]
          [else (assoc-lookup (cdr xs))]))
  (assoc-lookup (environ-xs env)))
(define (env-update! x v xs) ; <---------------------------------- !!!
  (define (assoc-update! xs)
    (cond [(null? xs) (error "Unknown identifier" x)]
          [(eq? x (mcar (car xs))) (set-mcdr! (car xs) v)]
          [else (env-update! x v (cdr xs))]))
  (assoc-update! (environ-xs xs)))


(define map-expr
  '(letrec (map (lambda (f) (lambda (xs)
                              (if (null? xs)
                                  null
                                  (cons (f (car xs) (map f (cdr xs))))))))
     (map (lambda (x) (+ x 1)) '(1 2 3))))

(define filter-expr
  '(letrec (filter (lambda (pred) (lambda (lst)
                                    (if (null? lst)
                                        null
                                        (if (pred (car lst))
                                            (cons (car lst) (filter pred (cdr lst)))
                                            (filter pred (cdr lst)))))))))

(define start-env
   env-empty)

; --------- ;
; Ewaluacja ;
; --------- ;

(struct clo (id e env) #:transparent)

(define (value? v)
  (or (number? v)
      (boolean? v)
      (and (pair? v) (value? (car v)) (value? (cdr v)))
      (null? v)
      (clo? v)
      (blackhole? v))) ; <---------------------------------------- !!!


(define (eval-env e env)
  (match e
    [(const n) n]
    [(binop op l r) ((op->proc op) (eval-env l env)
                                   (eval-env r env))]
    [(let-expr x e1 e2)
     (eval-env e2 (env-add x (eval-env e1 env) env))]
    [(letrec-expr x e1 e2) ; <------------------------------------ !!!
     (let* ([new-env (env-add x (blackhole) env)]
            [v (eval-env e1 new-env)])
       (begin
          (env-update! x v new-env)
          (eval-env e2 new-env)))]
    [(var-expr x) (env-lookup x env)]
    [(if-expr eb et ef) (if (eval-env eb env)
                            (eval-env et env)
                            (eval-env ef env))]
    [(cons-expr e1 e2) (cons (eval-env e1 env)
                             (eval-env e2 env))]
    [(car-expr e) (car (eval-env e env))]
    [(cdr-expr e) (cdr (eval-env e env))]
    [(null-expr) null]
    [(null?-expr e) (null? (eval-env e env))]
    [(lam x e) (clo x e env)]
    [(app f e)
     (let ([vf (eval-env f env)]
           [ve (eval-env e env)])
       (match vf [(clo x body fun-env)
                  (eval-env body (env-add x ve fun-env))]))]
    [(quote-expr e) e]
    [(display-ac e) (display (eval-env e env))]
    [(read-ac)    (read)]))

(define (eval e) (eval-env e start-env))

(define program
  '(letrec
     [fact (lambda (n) (if (= n 0) 1 (* n (fact (- n 1)))))]
   (letrec
     [even-odd
       (cons
         (lambda (x)
           (if (= x 0) true  ((cdr even-odd) (- x 1))))
         (lambda (x)
           (if (= x 0) false ((car even-odd) (- x 1)))))]
   (let [even (car even-odd)]
   (let [odd  (cdr even-odd)]
   (even (fact 6)))))))

(define PROGRAM
  '(letrec [from-to (lambda (n k)
                      (if (> n k)
                          null
                          (cons n (from-to (+ n 1) k))))]
   (letrec [sum (lambda (xs)
                  (if (null? xs)
                      0
                      (+ (car xs) (sum (cdr xs)))))]
   (sum (from-to 1 36)))))

(define (test-eval) (eval (parse PROGRAM)))

(define aaa
  '(letrec* ([is-even? (lambda (n)
                       (or (= 0 n)
                           (is-odd? (- n 1))))]
           [is-odd? (lambda (n)
                      (and (> n 0)
                           (is-even? (- n 1))))])
    (is-odd? 11)))

(parse aaa)


