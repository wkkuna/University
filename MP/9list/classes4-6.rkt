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
    [_ false]))

(define (parse q)
  (cond
    [(number? q) (const q)]
    [(eq? q 'true)  (const true)]
    [(eq? q 'false) (const false)]
    [(eq? q 'null)  (null-expr)]
    [(symbol? q) (var-expr q)]
    
    [(and (list? q) (eq? (length q) 2) (eq? (first q) 'quote) (symbol? (second q)))
     (quote-expr (second q))]

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
      (blackhole? v)
      (symbol? v))) ; <---------------------------------------- !!!

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
    [(quote-expr e) e]))

(define (eval e) (eval-env e env-empty))

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

(define zadanie5
        '(letrec [append (lambda (xs ys)
                                 (if (null? xs)
                                     ys
                                     (cons (car xs) (append (cdr xs) ys))))] 
         (letrec [map (lambda (f xs)
                              (if (null? xs)
                                  null
                                  (cons (f (car xs)) (map f (cdr xs)))))] 
         (letrec [filter (lambda (pred xs)
                                 (if (null? xs)
                                     null
                                     (if (pred (car xs))
                                         (cons (car xs) (filter pred (cdr xs)))
                                         (filter pred (cdr xs)))))]
         (append (cons 1 (cons 2 null)) (cons 3 null))))))
(eval (parse zadanie5)) 
(define (test-eval) (eval (parse PROGRAM)))

;(parse '(car '(1 2 3)))
;(test-eval)

;;; [4, 2, 7,2 ,1] [1, 4] -> [2, 7, 2 ...] [1, 4, 4] -> [7 2..] [1 , 2, 4, 4]


(define zadanie6
    '(letrec [insert (lambda (l x) 
                        (if (null? l)
                            (cons x null)
                            (if (> x (car l))
                                (cons (car l) (insert (cdr l) x))
                                (cons x l))))]

    (letrec [insertion-sort (lambda (xs)
                (letrec [sort (lambda (l acc)
                                    (if (null? l)
                                        acc
                                        (sort (cdr l) (insert acc (car l)))))]
                        (sort xs null)))]
    (insertion-sort (cons 6 (cons 2 (cons 7 (cons 1 null))))))))

(eval (parse zadanie6))