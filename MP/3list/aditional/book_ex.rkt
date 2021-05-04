#lang racket

;;IMPORTANT
;(define (filter predicate sequence)
;  (cond [(null? sequence) null]
;        [(predicate (car sequence))
;         (cons (car sequence)
;               (filter predicate (cdr sequence)))]
;        [else (filter predicate (cdr sequence))]))

;;2.30
;;plain
(define (square-tree items)
  (cond [(null? items) null]
        [(not (pair? items)) (expt items 2)]
        [else (cons (square-tree (car items))
                    (square-tree (cdr items)))]))

;;using map
(define (square-tree-m items)
  (map (lambda (sub-items)
         (if (pair? sub-items)
             (square-tree-m sub-items)
             (* sub-items sub-items)))
         items))

;;2.32
(define (subsets s)
  (if (null? s)
      (list null)
      (let [(rest (subsets (cdr s)))]
        (append rest (map (lambda (x) (cons (car s) x)) rest)))))


;;IMPORTANT
(define (accumulate op initial sequence)
  (if (null? sequence)
      initial
      (op (car sequence)
          (accumulate op initial (cdr sequence)))))
;;IMPORTANT
;(define (map procedure items)
;  (if (null? items)
;      null
;      (cons (procedure (car items))
;            (map procedure (cdr items)))))

;;2.33
(define (map p sequence)
  (accumulate (lambda (x y) (cons (p x)  y)) null sequence))

(define (append seq1 seq2)
  (accumulate cons seq2 seq1))

(define (length sequence)
  (accumulate (lambda (x y) (+ 1 y)) 0 sequence))

;;2.35
(define (count-leaves xs)
  (accumulate + 0 (map
                   (lambda (x)
                     (cond [(pair? x) (count-leaves x)]
                           [(null? x) 0]
                           [else 1]))
                      xs)))

;;2.53
;(list 'a 'b 'c)
;(list (list 'george))
;(cdr '((x1 x2) (y1 y2)))
;(cadr '((x1 x2) (y1 y2)))
;(pair? (car '(a short list)))
;(memq 'red '((red shoes) (blue socks)))
;(memq 'red '(red shoes blue socks))


;;Permutation
(define (flatmap proc seq)
  (accumulate append null (map proc seq)))

(define (permutations s)
  (if (null? s)                      ; empty set?
      (list null)                   ; sequence containing empty set
      (flatmap (lambda (x)
                 (map (lambda (p) (cons x p))
                      (permutations (remove x s))))
               s)))


