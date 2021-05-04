 #lang racket

; zadanie 1
(struct const    (val)      #:transparent)
(struct binop    (op l r)   #:transparent)
(struct var-expr (id)       #:transparent)
(struct let-expr (id e1 e2) #:transparent)
(struct sigma (od do f x)   #:transparent)
(struct cal (bot top f x)   #:transparent)
(struct min (f)             #:transparent)



(define (expr? e)
  (match e
    [(const n) (number? n)]
    [(binop op l r) (and (or (symbol? op)
                             (member op (list '+ '- '* '/ '^)))
                    (expr? l) (expr? r))]
    [(var-expr x) (symbol? x)]
    [(let-expr x e1 e2) (and (symbol? x) (expr? e1) (expr? e2))]
    [(sigma od do f x) (and (expr? do)
                            (expr? od)
                            (expr? f)
                            (var-expr? x))]
    [(cal bot top f x) (and (expr? bot)
                            (expr? top)
                            (expr? f)
                            (var-expr? x))]
    [(min f) (expr? f)]
    [_ false]))

        



(cal (binop '+ (const 1) (const 1))
     (const 3)
     (binop '/ 
             (const 1) 
             (binop '^ 
                    (const 2) 
                    (binop '- (const 0) (var-expr 'x))))
     (var-expr 'x))


; zadanie 2

(define (parse q)
  (cond
    [(number? q) (const q)]
    [(symbol? q) (var-expr q)]
    [(and (list? q) (eq? (length q) 3) (eq? (first q) 'let))
     (let-expr (first (second q))
               (parse (second (second q)))
               (parse (third q)))]
    [(and (list? q) (eq? (length q) 3) (symbol? (first q)))
     (binop (first q)
            (parse (second q))
            (parse (third q)))]
    [(and (list? q) (eq? (length q) 5) (eq? (first q) 'sigma))
        (sigma (parse (second q))
               (parse (third q))
               (parse (fourth q))
               (var-expr (fifth q)))]
    [(and (list? q) (eq? (length q) 5) (eq? (first q) 'cal))
        (cal  (parse (second q))
               (parse (third q))
               (parse (fourth q))
               (var-expr (fifth q)))]
    [(and (list? q) (eq? (length q) 2) (eq? (first q) 'min)) 
        (min (parse (second q)))]))

; zadanie 3


(struct var (var)  #:transparent)
(struct neg (f)  #:transparent)
(struct conj (l r) #:transparent)
(struct disj (l r) #:transparent)
(struct exists (x subf) #:transparent)
(struct forall (x subf) #:transparent)


(define (form-expr? q)
  (match q
    [(var v) true]
    [(neg f) (form-expr? f)]
    [(conj l r) (and (form-expr? l) (form-expr? r))]
    [(disj l r) (and (form-expr? l) (form-expr? r))]
    [(exists x subf) (and (symbol? x) (form-expr? subf))]
    [(forall x subf) (and (symbol? x) (form-expr? subf))]
    [_ false]))

;; 'x
;; '(neg x)

(define (form-parse q)
  (cond 
    [(symbol? q) (var q)]
    [(and (list? q) (eq? (length q) 2) (eq? (first q) 'neg)) 
        (neg (form-parse (second q)))]  
    [(and (list? q) (eq? (length q) 3) (eq? (first q) 'conj)) 
        (conj (form-parse (second q)) (form-parse (third q)))]  
    [(and (list? q) (eq? (length q) 3) (eq? (first q) 'disj)) 
        (disj (form-parse (second q)) (form-parse (third q)))]  
    [(and (list? q) (eq? (length q) 3) (eq? (first q) 'exists)) 
        (exists (second q) (form-parse (third q)))]
    [(and (list? q) (eq? (length q) 3) (eq? (first q) 'forall)) 
        (forall (second q) (form-parse (third q)))]
    ))

;zadanie 4

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


(define (eval-f f) 
 (define (eval-qbf formula env)
    (match formula
      [(var-expr x) (env-lookup x env)]
      [(neg f) (not (eval-qbf f env))]
      [(disj l r) (or (eval-qbf l env) (eval-qbf r env))]
      [(conj l r) (and (eval-qbf l env) (eval-qbf r env))]
      [(forall x f) (and (eval-qbf f (env-add x #t env)) 
                         (eval-qbf f (env-add x #f env)))]
      [(exists x f) (or (eval-qbf f (env-add x #t env)) 
                        (eval-qbf f (env-add x #f env)))]))
(eval-qbf f env-empty))

;Zadanie 5
(define (rename formula)
(define (rename-f formula env counter)
    (match formula
    [(const n) (const n)]
    [(var-expr x) (var-expr (env-lookup x env))]
    [(binop op l r) (binop op 
                            (rename-f l env counter)
                            (rename-f r env counter))]
    [(let-expr x ex1 ex2) (let-expr (string->symbol(string-append(symbol->string 'x) (number->string counter)))
                                    (rename-f ex1 
                                              env
                                              (+ 1 counter))
                                    (rename-f ex2 
                                              (env-add x (string->symbol(string-append (symbol->string 'x) (number->string counter))) env) 
                                              (+ 1 counter)))]))
(rename-f formula env-empty 1))


;;; (rename ( binop '+
;;;     ( let-expr 'x ( const 1) ( var-expr 'x ) )
;;;     ( let-expr 'y ( const 1) ( var-expr 'y ) ) ) )

; (binop '+ (let-expr 'x1 (const 1) (var-expr 'x1)) (let-expr 'x1 (const 1) (var-expr 'x1)))

;zadanie 6
(define (rename2 formula)
  (define (rename-f formula env counter)
    (match formula
      [(const n) (list (const n) env counter)]
      [(var-expr x) (list (var-expr (env-lookup x env)) env counter)]
      [(binop op l r) (let* ([left (rename-f l env counter)]
                             [right (rename-f r (second left) (third left))])
                          (list (binop op (first left) (first right)) 
                                (second right)
                                (third right)))]
      [(let-expr x ex1 ex2) (let* ([new-var (string->symbol(string-append(symbol->string 'x) (number->string counter)))]
                                   [new-ex1 (rename-f ex1 env (+ 1 counter))]
                                   [new-ex2 (rename-f ex2 
                                                      (env-add x new-var (second new-ex1)) 
                                                      (third new-ex1))])
                (list (let-expr new-var (first new-ex1) (first new-ex2)) 
                      (second new-ex2) 
                      (third new-ex2)))]))
(first (rename-f formula env-empty 1)))

(rename2 ( binop '+
    ( let-expr 'x ( const 1) ( var-expr 'x ) )
    ( let-expr 'y ( const 1) ( var-expr 'y ) ) ) )
; (binop '+ (let-expr 'x1 (const 1) (var-expr 'x1)) 
;           (let-expr 'x2 (const 1) (var-expr 'x2)))


; zadanie 7

(define (opt-formula formula)
  (define (search-variable f v)
    (match f
      [(const n) #f]
      [(var-expr x) (equal? x v)]
      [(binop op l r) (or (search-variable l v) (search-variable r v))] 
      [(let-expr x ex1 ex2)
       (cond
         [(and (search-variable ex1 v) (search-variable ex2 x)) #t]
         [(and (not (equal? x v)) (search-variable ex2 v)) #t]
         [else #f])]))
  (match formula
    [(const n) (const n)]
    [(var-expr x) formula]
    [(binop op l r) (binop op (opt-formula l) (opt-formula r))]
    [(let-expr x ex1 ex2) (if (search-variable ex2 x)
                              (let-expr x (opt-formula ex1) (opt-formula ex2))
                              (opt-formula ex2))]))