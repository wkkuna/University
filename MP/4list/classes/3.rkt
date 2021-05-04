#lang racket


(define (btree? t)
    (or (eq? t 'leaf)
        (and (list? t)
             (= 4 (length t))
             (eq? (car t) 'node)
             (btree? (caddr t) ) 
             (btree? (cadddr t)))))

;; mirror :: Tree -> Tree
(define (mirror t)
  (cond [(eq? t 'leaf) 'leaf]
        [else ]
        
        )

(mirror ’(node a (node b (node c leaf leaf) leaf) (node d leaf leaf))
;; czy znowu nie słychać?
;;rip

;; operacje na drzewach BST

(define (find x t)
  (cond
    [(leaf? t)            false]
    [(= (node-elem t) x)  true]
    [(> (node-elem t) x)  (find x (node-left t))]
    [(< (node-elem t) x)  (find x (node-right t))]))

(define (insert x t)
  (cond
    [(leaf? t)            (node x leaf leaf)]
    [(= (node-elem t) x)  t]
    [(> (node-elem t) x)  (node (node-elem t)
                                (insert x (node-left t))
                                (node-right t))]
    [(< (node-elem t) x)  (node (node-elem t)
                                (node-left t)
                                (insert x (node-right t)))]))
