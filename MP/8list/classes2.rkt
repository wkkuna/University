#lang racket

;;Pary

; Do boolean.rkt dodajemy pary
;
; Miejsca, ktore sie zmienily oznaczone sa przez !!!

; --------- ;
; Wyrazenia ;
; --------- ;

(struct const     (val)      #:transparent)
(struct binop     (op l r)   #:transparent)
(struct var-expr  (id)       #:transparent)
(struct let-expr  (id e1 e2) #:transparent)
(struct if-expr   (eb et ef) #:transparent)
(struct cons-expr (e1 e2)    #:transparent) ; <------------------- !!!
(struct unop      (op arg)   #:transparent) ; <------------------- !!!

(define (expr? e)
  (match e
    [(const n) (or (number? n) (boolean? n))]
    [(binop op l r) (and (symbol? op) (expr? l) (expr? r))]
    [(unop op arg) (and (symbol? op) (expr? arg))]
    [(var-expr x) (symbol? x)]
    [(let-expr x e1 e2)
     (and (symbol? x) (expr? e1) (expr? e2))]
    [(if-expr eb et ef)
     (and (expr? eb) (expr? et) (expr? ef))]
    [(cons-expr e1 e2) (and (expr? e1) (expr? e2))] ; <----------- !!!
    [_ false]))

; e to podformula
; arg to ciag znakowy c[a,d]+r
(define (c-exp arg e)
        (cond 
             [(eq? (car arg) #\c)  (c-exp (cdr arg) e)]
             [(eq? (car arg) #\a)  (unop 'car (c-exp (cdr arg) e))]
             [(eq? (car arg) #\d)  (unop 'cdr (c-exp (cdr arg) e))]
             [(eq? (car arg) #\r)  e]))

             

(define (parse q)
  (cond
    [(number? q) (const q)]
    [(eq? q 'true)  (const true)]
    [(eq? q 'false) (const false)]
    [(symbol? q) (var-expr q)]
    [(and (list? q) (eq? (length q) 3) (eq? (first q) 'cons)) ; <- !!!
     (cons-expr (parse (second q))
                (parse (third q)))]
    [(and (list? q) (eq? (length q) 3) (eq? (first q) 'let))
     (let-expr (first (second q))
               (parse (second (second q)))
               (parse (third q)))]
    [(and (list? q) (eq? (length q) 4) (eq? (first q) 'if))
     (if-expr (parse (second q))
              (parse (third q))
              (parse (fourth q)))]
    [(and (list? q) (eq? (length q) 3) (symbol? (first q)))
     (binop (first q)
            (parse (second q))
            (parse (third q)))]
    [(and (list? q) (eq? (length q) 2))  
        (let ([x (string->list (symbol->string (first q)))])
               (if (and (eq? (first x) #\c) (eq? (last x) #\r))
                   (c-exp x (parse (second q)))
                   (unop (first q) (parse (second q)))))]))


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
  (or (number? v)
      (boolean? v)
      (and (pair? v) (value? (car v)) (value? (cdr v)))))

(define (op->proc op)
  (match op ['+ +] ['- -] ['* *] ['/ /] ['% modulo]
            ['= =] ['> >] ['>= >=] ['< <] ['<= <=]
            ['and (lambda (x y) (and x y))]
            ['or  (lambda (x y) (or  x y))]
            ['pair? pair?] ['not not]
            ['car car] ['cdr cdr]))

(define (eval-env e env)
  (match e
    [(const n) n]
    [(binop op l r) ((op->proc op) (eval-env l env)
                                   (eval-env r env))]
    [(unop op arg) ((op->proc op) (eval-env arg env))]
    [(let-expr x e1 e2)
     (eval-env e2 (env-add x (eval-env e1 env) env))]
    [(var-expr x) (env-lookup x env)]
    [(if-expr eb et ef) (if (eval-env eb env)
                            (eval-env et env)
                            (eval-env ef env))]
    [(cons-expr e1 e2) (cons (eval-env e1 env) ; <---------------- !!!
                             (eval-env e2 env))])) ; <------------------- !!!

(define (eval e) (eval-env e env-empty))

(eval(parse '(cdr (cons 1 (not (pair? (cons 2 3)))))))


(define program
  '(car (if true (cons 1 2) false)))

(define (test-eval) (eval (parse program)))
(test-eval)

