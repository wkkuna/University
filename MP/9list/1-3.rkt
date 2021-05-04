#lang racket
;; ------------------------- 1 ----------------------------
(define (mreverse! mxs)
  (define (aux prev curr)
    (if (null? curr)
        prev
        (let ([next (mcdr curr)])
          (set-mcdr! curr prev)
          (aux curr next))))
  (aux null mxs))

(define x (mcons 1 (mcons 2 (mcons 3 '()))))

;; ------------------------- 2 ----------------------------

(struct bd     (first last) #:mutable)
(struct bdlist (v [prev #:mutable] [next #:mutable]))

(define (list->bdlist xs)
  (define (aux prev xs)
    (if (null? xs)
        prev
        (let ([node (bdlist (car xs) prev null)])
          (set-bdlist-next! prev node)
          (aux node (cdr xs)))))
(let ([head (bdlist (car xs) null null)])
  (bd head (aux head (cdr xs)))))

(define b (list->bdlist '(1 2 3)))

(define (bdfilter pred? bds)
  (define (aux bdxs)
    (if (null? bdxs)
        (void)
        (let ([next (bdlist-next bdxs)]
              [prev (bdlist-prev bdxs)])
          (cond
            [(pred? (bdlist-v bdxs)) (aux next)]
            [(and (null? prev) (null? next))
             (set-bd-first! bds null)
             (set-bd-last!  bds null)]
            [(null? prev)
             (set-bdlist-prev!  next null)
             (set-bd-first! bds next)
             (aux next)]
            [(null? next)
             (set-bdlist-next! prev null)
             (set-bd-last! bds prev)]
            [else
             (set-bdlist-next! prev next)
             (set-bdlist-prev! next prev)
             (aux next)])
          )))
  (aux (bd-first bds)))

(bdfilter (lambda (x) (eq? x 2)) b)

;; ------------------------- 3 ----------------------------
             
(define (cycle-bdlist! bds)
  (set-bdlist-next! (bd-last bds) (bd-first bds))
  (set-bdlist-prev! (bd-first bds) (bd-last bds)))

(define (decycle-bdlist! bds)
  (set-bdlist-next! (bd-last bds) null)
  (set-bdlist-prev! (bd-first bds) null))