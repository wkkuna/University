#lang racket
;; Wiktoria Kuna 316418
(provide (struct-out const) (struct-out binop) (struct-out var-expr)
         (struct-out let-expr) (struct-out var-dead) find-dead-vars)
; --------- ;
; Wyrazenia ;
; --------- ;

(struct const    (val)      #:transparent)
(struct binop    (op l r)   #:transparent)
(struct var-expr (id)       #:transparent)
(struct var-dead (id)       #:transparent)
(struct let-expr (id e1 e2) #:transparent)

(define (expr? e)
  (match e
    [(const n) (number? n)]
    [(binop op l r) (and (symbol? op) (expr? l) (expr? r))]
    [(var-expr x) (symbol? x)]
    [(var-dead x) (symbol? x)]
    [(let-expr x e1 e2) (and (symbol? x) (expr? e1) (expr? e2))]
    [_ false]))

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
            (parse (third q)))]))

; ------------;
; Środowisko  ;
; ------------;

(define env-empty             (set))
(define (env-add x env)       (set-add env x))
(define (env-lookup x env)    (set-member? env x))
(define (env-rmv x env)       (set-remove env x))
(define (env-union env1 env2) (set-union env1 env2))

; ---------------------------------- ;
; Wyszukaj ostatnie uzycie zmiennych ;
; ---------------------------------- ;

(define (sub-env e env)
  (match e
    [(const x)           env-empty]
    [(var-expr x)       (env-add x env)]
    [(binop op l r)     (env-union (sub-env l env)
                                   (sub-env r env))]
    [(let-expr x e1 e2) (env-union (sub-env e1 env)
                                   (env-rmv x (sub-env e2 env)))]))
    
(define (find-dead e env)
  (match e
    [(const n)      (const n)]
    [(var-expr x)   (if (env-lookup x env)
                        (var-expr x)
                        (var-dead x))]
    [(binop op l r)
        (binop op (find-dead l (env-union env (sub-env r env)))
                  (find-dead r env))]
    [(let-expr x e1 e2)
      (let* ([env2 (env-rmv x env)]
             [env1 (env-union env (env-rmv x (sub-env e2 env)))])
        (let-expr x (find-dead e1 env1) (find-dead e2 env2)))]))


(define (find-dead-vars e)
  (find-dead e env-empty))

; ------;
; Testy ;
; ------;

(module+ test
(require rackunit)
  
  (define p0
    (parse '(let (x 3) (+ x x))))
  
  (define p0res
    (let-expr 'x (const 3) (binop '+ (var-expr 'x) (var-dead 'x))))

  (define p1
    (parse '(let (y 3) (let (x 2) (+ x y)))))

  (define p1res
    (let-expr 'y (const 3)
              (let-expr 'x (const 2)
                        (binop '+ (var-dead 'x) (var-dead 'y)))))
  
  (define p2
    (parse '(let (x 3) (+ (let (x 4) x) x))))
  
  (define p2res
    (let-expr 'x (const 3)
              (binop '+ (let-expr 'x (const 4)
                                  (var-dead 'x))
                     (var-dead 'x))))
    
  (define p3
    (parse '(let (x 6) (+ x (let (y x) (+ y 3))))))

  (define p3res
    (let-expr 'x (const 6)
              (binop '+ (var-expr 'x)
                     (let-expr 'y (var-dead 'x)
                               (binop '+ (var-dead 'y) (const 3))))))

  (define p4
    (parse '(let (x 3) (+ (let (x 4)
                            (+ (let (x 5) x) x))
                          x))))

  (define p4res
    (let-expr 'x (const 3)
              (binop '+ (let-expr 'x (const 4)
                                  (binop '+ (let-expr 'x (const 5)
                                                      (var-dead 'x))
                                         (var-dead 'x)))
                     (var-dead 'x))))

  (define p5
    (parse '(let (x 3) (+ (let (y x)
                            (* (let (x y) x) 3))
                          x))))
                      
  (define p5res
    (let-expr 'x (const 3)
              (binop '+ (let-expr 'y (var-expr 'x)
                                  (binop '* (let-expr 'x (var-dead 'y)
                                                      (var-dead 'x))
                                         (const 3)))
                     (var-dead 'x))))

  (define p6
    (parse '(let (x 3) (+ (- x 3) (* 2 (/ x 1))))))

  (define p6res
    (let-expr 'x (const 3)
       (binop '+
              (binop '- (var-expr 'x) (const 3))
              (binop '* (const 2)
                        (binop '/ (var-dead 'x) (const 1))))))

  (define p7
    (parse '(let (x 6) (+ x (let (y 2) (+ y 3))))))
  
  (define p7res
    (let-expr 'x (const 6)
              (binop '+ (var-dead 'x)
                     (let-expr 'y (const 2)
                               (binop '+ (var-dead 'y) (const 3))))))

  (define p8
    (parse '(let (x 3) (+ x (* (let (y x) y) (let (y 3) y) )))))

  (define p8res
    (let-expr 'x (const 3)
              (binop '+ (var-expr 'x)
                     (binop '* (let-expr 'y (var-dead 'x)
                                         (var-dead 'y))
                            (let-expr 'y (const 3)
                                      (var-dead 'y))))))

  (define p9
    (parse '(let (x (* 3 (let (x 5) x)))
              (* (let (x (+ 3 (let (y x) y))) 3)
                 5))))

  (define p9res
    (let-expr
     'x
     (binop '* (const 3) (let-expr 'x (const 5) (var-dead 'x)))
     (binop
      '*
      (let-expr 'x (binop '+ (const 3) (let-expr 'y (var-dead 'x) (var-dead 'y))) (const 3))
      (const 5))))

  (define p10
    (let-expr 'x (const 3)
              (binop '+ (var-expr'x) (let-expr 'x (const 5)
                                               (binop '+ (var-expr 'x) (var-expr 'x))))))
  (define p10res
    (let-expr 'x (const 3)
              (binop '+ (var-dead'x)
                     (let-expr'x (const  5)
                              (binop'+ (var-expr'x) (var-dead'x))))))

  (define p11
    (let-expr 'x (const 3) (binop '+ (var-expr'x) (var-expr'x))))

  (define p11res
    (let-expr'x (const 3) (binop '+ (var-expr'x) (var-dead'x))))
    

  

  (check-equal? (find-dead-vars p0) p0res "Program p0 failed")
  (check-equal? (find-dead-vars p1) p1res "Program p1 failed")
  (check-equal? (find-dead-vars p2) p2res "Program p2 failed")
  (check-equal? (find-dead-vars p3) p3res "Program p3 failed")
  (check-equal? (find-dead-vars p4) p4res "Program p4 failed")
  (check-equal? (find-dead-vars p5) p5res "Program p5 failed")
  (check-equal? (find-dead-vars p6) p6res "Program p6 failed")
  (check-equal? (find-dead-vars p7) p7res "Program p7 failed")
  (check-equal? (find-dead-vars p8) p8res "Program p8 failed")
  (check-equal? (find-dead-vars p9) p9res "Program p9 failed")
  (check-equal? (find-dead-vars p10) p10res "Program p10 failed")
  (check-equal? (find-dead-vars p11) p11res "Program p11 failed"))
;; Kooperacja z Jakub Zając