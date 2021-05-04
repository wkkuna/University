;;Wiktoria Kuna 316418
#lang racket
(provide (struct-out complex) parse eval)

(struct complex (re im) #:transparent)
(define value?
  complex?)

(struct const (val)    #:transparent)
(struct i     ()       #:transparent)
(struct binop (op l r) #:transparent)

;;------------------------Complex Arithmetic------------------------
;;------------------------------------------------------------------

(define (+/-complex op x y)
  (complex
   (op (complex-re x) (complex-re y))
   (op (complex-im x) (complex-im y))))

(define +complex
  (lambda (x y) (+/-complex + x y)))

(define -complex
  (lambda (x y) (+/-complex - x y)))

(define (*complex x y)
  (complex
   (- (* (complex-re x) (complex-re y))
      (* (complex-im x) (complex-im y)))
   (+ (* (complex-re x) (complex-im y))
      (* (complex-im x) (complex-re y)))))
(define (/complex x y)
  (let ([sq-sum (+ (expt (complex-re y) 2)
                   (expt (complex-im y) 2))])
    (complex
     (/ (+ (* (complex-re x) (complex-re y))
           (* (complex-im x) (complex-im y)))
        sq-sum)
     (/ (- (* (complex-im x) (complex-re y))
           (* (complex-re x) (complex-im y)))
        sq-sum))))

;;-------------------------------Eval-------------------------------
;;------------------------------------------------------------------

(define (op->proc op)
  (match op
    ['+ +complex]
    ['- -complex]
    ['* *complex]
    ['/ /complex]))

(define (eval e)
  (match e
    [(const n)       (complex n 0)]
    [(i)             (complex 0 1)]
    [(complex re im) e]
    [(binop op l r)  ((op->proc op) (eval l) (eval r))]))

;;------------------------------Parse-------------------------------
;;------------------------------------------------------------------

(define (parse q)
  (cond [(number? q) (const q)]
        [(eq? q 'i)  (i)]
        [(and (list? q) (eq? (length q) 3) (symbol? (first q)))
         (binop (first q) (parse (second q)) (parse (third q)))]))

;;------------------------------Tests-------------------------------
;;------------------------------------------------------------------
(module+ test
 (require rackunit)

  (let* [(epsilon 1e-10)
         (x  (make-rectangular 1.0 2.7))
         (y (make-rectangular 5.9 91.0))
         (z (make-rectangular 34.7 22.8))

         (e1  (+ x y))
         (e1c (eval (parse '(+ (+ 1.0 (* 2.7 i))
                               (+ 5.9 (* 91.0 i))))))

         (e2  (- z y))
         (e2c (eval (parse '(- (+ 34.7 (* 22.8 i))
                               (+ 5.9 (* 91.0 i))))))

         (e3  (* x z))
         (e3c (eval (parse '(* (+ 1.0 (* 2.7 i))
                               (+ 34.7 (* 22.8 i))))))

         (e4 (/ z y))
         (e4c (eval (parse '(/ (+ 34.7 (* 22.8 i))
                               (+ 5.9 (* 91.0 i))))))


         (extra (+ (- x z) (* x (/ y z))))
         (extrac (eval (parse '(+ (- (+ 1.0 (* 2.7 i))
                                     (+ 34.7 (* 22.8 i)))
                                  (* (+ 1.0 (* 2.7 i))
                                     (/ (+ 5.9 (* 91.0 i))
                                        (+ 34.7 (* 22.8 i))))))))]
    (check-within e1c (complex (real-part e1) (imag-part e1)) epsilon "Complex addition fail")
    (check-within e2c (complex (real-part e2) (imag-part e2)) epsilon "Complex subtraction fail")
    (check-within e3c (complex (real-part e3) (imag-part e3)) epsilon "Complex multiplication fail")
    (check-within e4c (complex (real-part e4) (imag-part e4)) epsilon "Complex division fail")
    (check-within extrac (complex (real-part extra) (imag-part extra)) epsilon "Complex arithmetics fail")))