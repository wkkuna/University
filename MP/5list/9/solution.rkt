#lang racket
;;Wiktoria Kuna 316418
(require "props.rkt")
(provide falsifiable-cnf?)
;;---------------------Potrzebne predykaty i konstruktory--------------------
(define (lit p x)
  (list 'lit p x))

(define lit-polarity second)
(define lit-var third)

(define (lit? f)
  (and (list? f)
       (= (length f) 3)
       (eq? (first f) 'lit)
       (boolean? (lit-polarity f))
       (var? (lit-var f))))
;;--------------------------convert-to-nnf (z zajęć)-------------------------

(define (convert-to-nnf f)
  (cond [(conj? f) (conj (convert-to-nnf (conj-left f))
                         (convert-to-nnf (conj-right f)))]
        [(disj? f) (disj (convert-to-nnf (disj-left f))
                         (convert-to-nnf (disj-right f)))]
        [(var? f) (lit #t f)]
        [(neg? f) (convert-neg (neg-subf f))]))

(define (convert-neg f)
  (cond [(conj? f) (disj (convert-neg (conj-left f))
                         (convert-neg (conj-right f)))]
        [(disj? f) (conj (convert-neg (disj-left f))
                         (convert-neg (disj-right f)))]
        [(var? f) (lit #f f)]
        [(neg? f) (convert-to-nnf (neg-subf f))]))

;;--------------------------convert-to-cnf (z zajęć)-------------------------
(define (cnf-lit l) (list (list l)))

(define cnf-conj append)

(define (cross-by f xs ys)
  (append-map (lambda (x)
                 (map (lambda (y) (f x y))
                      ys))
               xs))

(define (cnf-disj f1 f2)
  (cross-by append f1 f2))

(define (convert-to-cnf f)
  (cond [(conj? f) 
           (cnf-conj (convert-to-cnf (conj-left f))
                     (convert-to-cnf (conj-right f)))]
        [(disj? f) 
           (cnf-disj (convert-to-cnf (disj-left f))
                     (convert-to-cnf (disj-right f)))]
        [(lit? f) (cnf-lit f)]))

;;-----------------------------------ĆW. 9-----------------------------------

;; Funkcja add-negated dodaje zmienną i jej odpowiednie wartościowanie do listy
;; values o ile nie występuje ona już w tej liście, natomiast, gdy napotyka
;; prawo wyłączonego środka zwraca fałsz
(define (add-negated x values)
  (define (add xss exists?)
    (let ((var (lit-var x)) (p (lit-polarity x)))
      (cond [(null? xss)
             (cond [exists? values]
                   [else (cons (list var (not p)) values)])]
            [(eq? var (caar xss))
                  (cond [(eq? p (cadar xss)) #f]
                        [else (add (cdr xss) #t)])]
            [else (add (cdr xss) exists?)])))
  (add values #f))

;; Funkcja falsifiable-clause? generuje na bieżąco listę potencjalnych
;; wartościowań falsyfikujących klauzulę
(define (falsifiable-clause? clause)
  (define (gen-val xs values)
    (if (null? xs)
        values
        (let* ((x (car xs))
               (val-extnd (add-negated x values)))
          (if (eq? val-extnd #f)
              #f
              (gen-val (cdr xs) val-extnd)))))
  (gen-val clause '()))


(define (cnf-falsifiable? f) 
  (if (null? f)
      #f
      (let ((current-clause (falsifiable-clause? (car f))))
        (if (eq? current-clause #f)
            (cnf-falsifiable? (cdr f))
            current-clause))))

(define (falsifiable-cnf? f)
  (cnf-falsifiable? (convert-to-cnf (convert-to-nnf f))))

;;-------------------------------Przemyślenia----------------------------------;;
;; falsifiable-cnf? przyjmuje formułę, wykonuje jej translację do nnf,         ;;
;; by potem przetranslować ją do cnf.                                          ;;
;; Następnie korzystając z reprezentacji cnf, rozbija zapytanie czy formuła    ;;
;; jest falsyfikowalna na takowe zapytanie dla kolejnych klauzul.              ;;
;; Jeśli takową znajdzie zwraca #t, wpp. wartościowanie falsyfikujące klauzulę.;;
;;                                                                             ;;
;; falsifiable-cnf? w najgorszym przypadku sprawdzi m klauzul w złożoności     ;;
;; kwadratowej.                                                                ;;
;; Z kolei falsifiable-eval? dla n zmiennych musi sprawdzić 2^n przypadków,    ;;
;; za każdym podstawiając odpowiednie wartości za zmienne i obliczając wartość ;;
;; formuły.                                                                    ;;
;;                                                                             ;;
;; Przy małej ilości zmiennych falsifiable-eval? może działać szybciej dla     ;;
;; tautologi, jednakże wraz ze wzrostem zmiennych drastycznie rośnie jej       ;;
;; złożoność.                                                                  ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;;-----------------------------------Testy-------------------------------------;;
(module+ test
(require rackunit)

;;Przykładowe formuły
(define p
  (list 'disj (list 'conj 'a 'b) (list 'neg 'a)))

(define pp
  (list 'disj (list 'neg (list 'conj 'a 'b))
              (list 'conj (list 'disj 'p (list 'neg p))
                    (list 'neg 'a))))

;;Przykładowe tautologie
;;Prawo symplifikacji
(define phi
  (list 'disj (list 'neg 'p) (list 'disj 'p 'q)))

;;Prawo sprzeczności
(define psi
  (list 'neg (list 'conj 'p (list 'neg 'p))))

;;Prawo DeMorgana dla koniunkcji
(define kappa
  (list 'disj (list 'conj (list 'neg (list 'conj 'p 'q))
                          (list 'disj (list 'neg 'p)
                                      (list 'neg 'q)))
              (list 'conj (list 'neg (list 'neg (list 'conj 'p 'q)))
                          (list 'neg (list 'disj (list 'neg 'p)
                                                 (list 'neg 'q))))))

(check-within (falsifiable-cnf? 'p) '((p #f)) 0 "falsifiable-cnf? failed for (a)")
(check-within (falsifiable-cnf? (list 'neg 'a)) '((a #t)) 0 "falsifiable-cnf? failed for (¬a)")
(check-within (falsifiable-cnf? (list 'conj 'b 'a)) '((b #f)) 0 "falsifiable-cnf? failed for simple (a ∧ b)")
(check-within (falsifiable-cnf? (list 'disj 'b 'a)) '((a #f) (b #f)) 0  "falsifiable-cnf? failed for (a v b)")
(check-eq? (falsifiable-cnf? (list 'disj (list 'neg 'a) 'a)) #f "falsifiable-cnf? failed for (p v ¬p)")
(check-within (falsifiable-cnf? p) '((a #t) (b #f)) 0 "falsifiable-cnf? failed for ((a ∧ b) v ¬a)")
(check-within (falsifiable-cnf? pp) '((p #f) (b #t) (a #t)) 0 "falsifiable-cnf? failed for (¬(a ∧ b) v ((p v ¬p) ∧ ¬a))")
(check-eq? (falsifiable-cnf? phi) #f "falsifiable-cnf? failed for (¬p v (p v q))")
(check-eq? (falsifiable-cnf? psi) #f "falsifiable-cnf? failed for (¬(p ∧ ¬p))")
(check-eq? (falsifiable-cnf? kappa) #f "falsifiable-cnf? failed for DeMorgan's law (negating conj): ((¬(p ∧ q) ∧ (¬p v ¬q)) v (¬(¬(p ∧ q)) ∧ (¬(¬p v ¬q))))"))