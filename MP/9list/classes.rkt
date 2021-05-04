#lang racket

;; Zadanie 1
(define (mreverse! mxs)
  (define (aux prev curr)
    (if (null? curr)
        prev
        (let ([next (mcdr curr)])
          (set-mcdr! curr prev)
          (aux curr next))))
   (aux null mxs))

(define x (cons 1 (cons -2 (cons 3 (cons 4'())))))
; (mreverse! x)

;; Zadanie 2
(struct bdlist (v [prev #:mutable] [next #:mutable]) #:transparent)

(define (list->bdlist xs)
        (define (list->bdlist-aux xs prev)
          (if (null? xs)
              null
              (let ([temp (bdlist (car xs) prev null)])
                   (begin
                   (set-bdlist-next! temp (list->bdlist-aux (cdr xs) temp))
                   temp))))
        (list->bdlist-aux xs null))

(define (bdfilter pred xs)
        (define (bdfilter-aux xs prev)
                (cond [(null? xs) null]
                      [(pred (bdlist-v xs))
                             (let ([temp xs])
                                   (begin 
                                        (set-bdlist-prev! temp prev)
                                        (set-bdlist-next! temp (bdfilter-aux (bdlist-next xs) temp))
                                        temp))]
                      [else (bdfilter-aux (bdlist-next xs) prev)]))
        (bdfilter-aux xs null))

;(bdfilter positive? (list->bdlist x))

(define (cycle-bdlist! xs)
    (define (assoc xs list)
            (if (null? (bdlist-next xs))
                (begin
                    (set-bdlist-next! xs list)
                    (set-bdlist-prev! list xs))
                (assoc (bdlist-next xs) list)))
    (assoc xs xs))

    (define (decycle-bdlist! xs)
            (begin
                (set-bdlist-next! (bdlist-prev xs) null)
                (set-bdlist-prev! xs null)))

(define xx (list->bdlist x))
xx
(cycle-bdlist! xx)
xx


;;; #2=(bdlist 1 '() #1=(bdlist -2 #2# #0=(bdlist 3 #1# (bdlist 4 #0# '()))))
;;; #0=(bdlist 1 #3=(bdlist 4 #1=(bdlist 3 #2=(bdlist -2 #0# #1#) #3#) #0#) #2#)
;;; 1