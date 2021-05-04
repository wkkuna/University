#lang racket
;; Zadanie 1
(define (var? t)
  (symbol? t))

(define (operator? t)
  (or (eq? t 'neg)
      (eq? t 'conj)
      (eq? t 'disj)))

(define (neg? t)
  (and (list? t)
       (= 2 (length t))
       (eq? 'neg (car t))))

(define (conj? t)
  (and (list? t)
       (= 3 (length t))
       (eq? 'conj (car t))))

(define (disj? t)
  (and (list? t)
       (= 3 (length t))
       (eq? 'disj (car t))))

(define (prop? f)
  (or (var? f)
      (and (neg? f)
           (prop? (neg-subf f)))
      (and (disj? f)
           (prop? (disj-left f))
           (prop? (disj-rght f)))
      (and (conj? f)
           (prop? (conj-left f))
           (prop? (conj-rght f)))))


(define (neg opnd)
    (list 'neg opnd))

(define (conj opnd-a opnd-b)
    (list 'conj opnd-a opnd-b))

(define (disj opnd-a opnd-b)
    (list 'disj opnd-a opnd-b))

(define neg-subf second)

(define conj-left second)

(define conj-rght third)

(define disj-left second)

(define disj-rght third)


(define (literal v)
    (if (neg? v)
         (list 'lit 'neg (neg-subf v))
         (list 'lit 'pos v)))

(define (literal? v)
        (and (list? v)
             (= 3 (length v))
			 (eq? (car v) 'lit)))

;; (list 'lit 'pos 'a)
(define (positive? v)
		(eq? (second v) 'pos))


;; Zadanie 2

;; (P ) : prop -> bool
;; 1) (var? x)          --> (P x)
;; 2) (P x)             --> (P (neg x))
;; 3) (P x), (P y)      --> (P (conj x y))
;; 4) (P x), (P y)      --> (P (disj x y))


;; Zadanie 3


(define p
  (list 'neg (list 'disj (list 'conj 'a 'b) (list 'neg 'a))))
  ;;  ~ ( (a /\ b) \/ ~a)

(define pp (neg (disj (conj 'a 'b) (neg 'a))))

(define (free-vars f)
        (define (free-vars-aux f)
            (cond [(var? f) (list f)]
                  [(literal? f) (list (third f))]
                  [(neg? f) (free-vars-aux (neg-subf f))]
                  [(disj? f)  (append (free-vars-aux (disj-left f))                   
                                      (free-vars-aux (disj-rght f)))]
                  [(conj? f)  (append (free-vars-aux (conj-left f))                   
                                      (free-vars-aux (conj-rght f)))]))
        (remove-duplicates (free-vars-aux f)))


;; Zadanie 4

(define (gen-vals  xs)
  (if (null? xs)
      (list  null)
      (let* ((vss   (gen-vals (cdr xs)))
             (x     (car xs))
             (vst   (map (lambda(vs) (cons (list x true)   vs)) vss))
             (vsf   (map (lambda(vs) (cons (list x false) vs)) vss)))
        (append  vst  vsf))))

(gen-vals (free-vars p))
;;; '( ((a #t) (b #t)) 
 ;     ((a #t) (b #f)) 
 ;     ((a #f) (b #t)) 
 ;     ((a #f) (b #f))
 ;   )

(define (eval-formula values formula)
    (define (search-value variable lst)
        (if (eq? (caar lst) variable)
            (cdar lst)
            (search-value variable (cdr lst))))

    (cond [(var? formula) (search-value formula values)]
          [(literal? formula) (if (positive? formula)
                                  (search-value formula values)
                                  (not (search-value formula values)))]
          [(neg? formula) (not (eval-formula values (neg-subf formula)))]  
          [(conj? formula) (and (eval-formula values (conj-left formula)) 
                                (eval-formula values (conj-rght formula)))]
          [(disj? formula) (or (eval-formula values (disj-left formula)) 
                               (eval-formula values (disj-rght formula)))]))

(define valuation (car (gen-vals (free-vars p))))
valuation ;; '( (a #t) (b #t) )

(eval-formula valuation p) ;; #f

(define (falsifiable-eval? formula)
        (define (search list-values)
            (if (null? list-values) 
                  false
                  (if (eval-formula (car list-values) formula) 
                      (search (cdr list-values))
                      (car list-values))))
        (search (gen-vals (free-vars formula))))

;;Zadanie 5
;; ~ ( (a /\ b) \/ ~a) -~>  ( ~(a /\ b) /\ ~~a ) -~> ( (~a \/ ~b)  /\ a)

(define (nnf? f)
    (or (literal? f)
        (and (conj? f)
             (nnf? (conj-left f))
             (nnf? (conj-rght f)))
        (and (disj? f)
             (nnf? (disj-left f))
             (nnf? (disj-rght f)))))

;;wzajemnie rekurencyjne
(define (even? n)
    (if (= n 0)
        true
        (odd? (- n 1))))

(define (odd? n)
    (if (= n 0)
        false
        (even? (- n 1))))

(define (even1? n)
    (define (even2? n flag)
        (if (= n 0)
            flag
            (even2? (- n 1) (not flag))))
    (even2? n true))

;; Zadanie 6
;; ~ ( (a /\ b) \/ ~a) -~>  ( ~(a /\ b) /\ ~~a ) -~> ( (~a \/ ~b)  /\ a)

(define (convert-to-nnf f)
    (define (ctn f flag)
        (cond [(var? f)   (if flag 
                              (literal (neg f))
                              (literal f))]  
              [(neg? f)    (ctn (neg-subf f) (not flag))]
              [(conj? f)   (if flag ;; (A \/ B)
                                (disj (ctn (conj-left f) flag) (ctn (conj-rght f) flag))
                                (conj (ctn (conj-left f) flag) (ctn (conj-rght f) flag)))]
              [(disj? f)   (if flag 
                                (conj (ctn (disj-left f) flag) (ctn (disj-rght f) flag))
                                (disj (ctn (disj-left f) flag) (ctn (disj-rght f) flag)))]
                              ))
    (ctn f #f))
    
;( (~a \/ ~b)  /\ a)
(convert-to-nnf p) ; '(conj (disj (lit neg a) (lit neg b)) (lit pos a))

;; Zadanie 8
;; (~a \/ b \/ a) /\ (c \/ ~c) /\ ~b

(define (forall l p?)
    (if (null? l)
        true
        (and (p? (car l)) (forall (cdr l) p?))))

(define disjs list)
(define (disjs? l)
        (list? l))

(define cnf list)
(define (cnf? f)
    (and (list? f)
         (forall f (lambda (l) (disj? l)))))


(define (convert-to-cnf f)

    (define (ctc-merge xss yss acc)
        (if (null? yss)
            acc
            (ctc-merge xss (cdr yss) 
                (append (map (lambda (xs) (append (car yss) xs)) xss) acc))))
        
        (cond 
            [(literal? f)   (cnf (list f))]
            [(conj? f)      (let 
                                ([l (convert-to-cnf (conj-left f))]
                                 [r (convert-to-cnf (conj-rght f))])
                              (append  l r))]
            [(disj? f)      (let 
                                ([l (convert-to-cnf (disj-left f))]
                                 [r (convert-to-cnf (disj-rght f))])
                              (ctc-merge l r '()))]))
                    

;   ~ ( (a /\ b) \/ ~a) \/ ~ ( (a /\ b) \/ ~a)
;   ( (~a \/ ~b)  /\ a) \/  w  
  
(convert-to-cnf (convert-to-nnf (disj p 'w)))


(define (eval-cnf f v)
 (define (search-value variable lst)
        (if (eq? (caar lst) variable)
            (cdar lst)
            (search-value variable (cdr lst))))
 (define (clause xs)
    (if (null? xs)  
        #f
        (if (search-value (car xs) v)
            #t
            (clause (cdr xs)))))
(define (aux f)
 (if (null? f)
     #f
     (if (clause (car f))
        (aux (cdr f))
        #f)))
(aux f))

    
;;; (define (nnf? f)
;;;     (or (literal? f)
;;;         (and (conj? f)
;;;              (nnf? (conj-left f))
;;;              (nnf? (conj-rght f)))
;;;         (and (disj? f)
;;;              (nnf? (disj-left f))
;;;              (nnf? (disj-rght f)))))


;;; (define (convert-to-nnf f)
;;;     (define (ctn f flag)
;;;         (cond [(var? f)   (if flag 
;;;                               (literal (neg f))
;;;                               (literal f))]  
;;;               [(neg? f)    (ctn (neg-subf f) (not flag))]
;;;               [(conj? f)   (if flag ;; (A \/ B)
;;;                                 (disj (ctn (conj-left f) flag) (ctn (conj-rght f) flag))
;;;                                 (conj (ctn (conj-left f) flag) (ctn (conj-rght f) flag)))]
;;;               [(disj? f)   (if flag 
;;;                                 (conj (ctn (disj-left f) flag) (ctn (disj-rght f) flag))
;;;                                 (disj (ctn (disj-left f) flag) (ctn (disj-rght f) flag)))]
;;;                               ))


;; (P ) : prop -> bool
;; 1) (var? x)          --> (P x)
;; 2) (P x)             --> (P (neg x))
;; 3) (P x), (P y)      --> (P (conj x y))
;; 4) (P x), (P y)      --> (P (disj x y))


; (nnf? (convert-to-nnf f))
; (P x) = (lambda (x) (nnf? (convert-to-nnf x)))

; 1) (var? x) ->  (nnf? (convert-to-nnf x)) = (nnf? (literal x)) 
; 2) (P x)    ->  (nnf? (convert-to-nnf (neg x)))  = (nnf? (ctn (neg-subf (neg x)) #t))) = (nnf? (ctn x #t)) 
; 3) (P x), (P y) -> (nnf? (convert-to-nnf (conj x y))) = (nnf? (conj (ctn (conj-left (conj x y)) #f) (ctn (conj-right (conj x y)) #f))) =
; = (nnf? (conj (ctn x #f) (ctn y #f))) = (and (nnf? (ctn x #f)) (nnf? (ctn y #f))))
