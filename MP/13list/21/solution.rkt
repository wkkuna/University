#lang typed/racket
;; Wiktoria Kuna 316418
(provide parse typecheck)
; --------- ;
; Wyrazenia ;
; --------- ;
(define-type Expr
  (U const binop var-expr let-expr if-expr))
(define-type Value (U Number Boolean))
(define-type BinopSym
  (U '+ '- '/ '* '% '= '> '< '>= '<= 'and 'or))

(struct const    ([val : Value])          #:transparent)
(struct binop    ([op : BinopSym]
                  [l : Expr] [r : Expr])   #:transparent)
(struct var-expr ([id : Symbol])           #:transparent)
(struct let-expr ([id : Symbol]
                  [e1 : Expr] [e2 : Expr]) #:transparent)
(struct if-expr  ([eb : Expr]
                  [et : Expr] [ef : Expr]) #:transparent)

(define-predicate binop-sym? BinopSym)
(define-predicate expr? Expr)
(define-predicate value? Value)

(: parse (-> Any Expr))
(define (parse q)
  (match q
    [(? number?) (const q)]
    ['true  (const true)]
    ['false (const false)]
    [(? symbol?) (var-expr q)]
    [`(let (,x ,e1) ,e2)
     #:when (symbol? x)
     (let-expr x
               (parse e1)
               (parse e2))]
    [`(if ,eb ,et ,ef)
     (if-expr (parse eb)
              (parse et)
              (parse ef))]
    [`(,op ,l ,r)
     #:when (binop-sym? op)
     (binop op
            (parse l)
            (parse r))]))

(define (test-parse) (parse '(let [x (+ 2 2)] (+ x 1))))

; ---------- ;
; Zadanie 21 ;
; ---------- ;

(define-type  EType (U 'real 'boolean))

; ---------- ;
; Srodowisko ;
; ---------- ;


(define-type Env environ)

(struct environ ([xs : (Listof (Pairof Symbol EType))]))

(define env-empty (environ null))

(: env-add (-> Symbol EType Env Env))
(define (env-add x v env)
  (environ (cons (cons x v) (environ-xs env))))

(: env-lookup (-> Symbol Env EType))
(define (env-lookup x env)
  (: assoc-lookup (-> (Listof (Pairof Symbol EType)) EType)) 
  (define (assoc-lookup xs)
    (cond [(null? xs) (error "Unknown identifier" x)]
          [(eq? x (car (car xs))) (cdr (car xs))]
          [else (assoc-lookup (cdr xs))]))
  (assoc-lookup (environ-xs env)))

; ---------- ;
; typecheck  ;
; ---------- ;

(define (real->real? op)
  (member op '(+ - * / %)))
(define (real->bool? op)
  (member op '(= > < >= <=)))
(define (bool->bool? op)
  (member op '(and or)))

(: typecheck-env (-> Expr Env (U EType #f)))
(define (typecheck-env e env)
  (match e
    [(const n)
     (if (boolean? n)
         'boolean
         'real)]
    [(binop op l r)
     (cond
       [(and (real->real? op) (eq? (typecheck-env l env) 'real)
             (eq? (typecheck-env r env) 'real))  'real]
       [(and (real->bool? op) (eq? (typecheck-env l env) 'real)
             (eq? (typecheck-env r env) 'real))  'boolean]
       [(and (bool->bool? op) (eq? (typecheck-env l env) 'boolean)
             (eq? (typecheck-env r env) 'boolean))  'boolean]
       [else #f])]
    [(var-expr id) (env-lookup id env)]
    [(let-expr id e1 e2)
     (let ([v (typecheck-env e1 env)])
       (if (false? v)
           #f
           (typecheck-env e2 (env-add id v env))))]
    [(if-expr eb et ef)
     (let ([pred (typecheck-env eb env)]
           [e1   (typecheck-env et env)]
           [e2   (typecheck-env ef env)])
       (if (and (eq? pred 'boolean)
                (eq? e1 e2))
           e1
           #f))]))

(: typecheck (-> Expr (U EType #f)))
(define (typecheck e) (typecheck-env e env-empty))

; ---------- ;
;   testy    ;
; ---------- ;

(module+ test
  (require typed/rackunit)

  (define p0 (parse '(+ 1 false)))
  (define p1 (parse '(* 1 (+ 3 (- false 0)))))
  (define p2 (parse '(let [x false] (* 3 (and x true)))))
  (define p3 (parse '(let [x 1] (let [y 2] (if (> x y) (and true true) (+ 1 2))))))
  (define p4 (parse '(if true (+ 1 2) (* 4 6))))
  (define p5 (parse '(let [x 3] (let [y false] (if y (* 3 8) (% false 1))))))

  (check-eq? (typecheck (const 1)) 'real "Test failed for 'real const")
  (check-eq? (typecheck (const #f)) 'boolean "Test failed for 'boolean const")
  (check-eq? (typecheck p0) #f "p0 test failed")
  (check-eq? (typecheck p1) #f "p1 test failed")
  (check-eq? (typecheck p2) #f "p2 test failed")
  (check-eq? (typecheck p3) #f "p3 test failed")
  (check-eq? (typecheck p4) 'real "p4 test failed")
  (check-eq? (typecheck p5) #f "p5 test failed"))

;; Wykonane we współpracy z Jakub Zając
