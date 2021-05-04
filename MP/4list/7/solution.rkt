#lang racket
(provide make-hnode tagged-list? leaf leaf? hnode? hnode-elem hnode-left hnode-rank hnode-right
         hord? heap? rank make-elem elem-priority elem-val empty-heap heap-insert heap-merge
         heap-min heap-pop heap-empty?)

(define (inc n)
  (+ n 1))

;;; tagged lists
(define (tagged-list? len-xs tag xs)
  (and (list? xs)
       (= len-xs (length xs))
       (eq? (first xs) tag)))

;;; ordered elements
(define (make-elem pri val)
  (cons pri val))

(define (elem-priority x)
  (car x))

(define (elem-val x)
  (cdr x))

;;; leftist heaps (after Okasaki)

;; data representation
(define leaf 'leaf)

(define (leaf? h) (eq? 'leaf h))

(define (hnode? h)
  (and (tagged-list? 5 'hnode h)
       (natural? (caddr h))))
;;---------------------------------------MAKE-HNODE---------------------------------------
(define (make-hnode elem heap-a heap-b)
  (cond [(>= (rank heap-a) (rank heap-b))
         (list 'hnode elem (inc (rank heap-b)) heap-a heap-b)]
        [else
         (list 'hnode elem (inc (rank heap-a)) heap-b heap-a)]))
;;----------------------------------------------------------------------------------------
(define (hnode-elem h)
  (second h))

(define (hnode-left h)
  (fourth h))

(define (hnode-right h)
  (fifth h))

(define (hnode-rank h)
  (third h))

(define (hord? p h)
  (or (leaf? h)
      (<= p (elem-priority (hnode-elem h)))))

(define (heap? h)
  (or (leaf? h)
      (and (hnode? h)
           (heap? (hnode-left h))
           (heap? (hnode-right h))
           (<= (rank (hnode-right h))
               (rank (hnode-left h)))
           (= (rank h) (inc (rank (hnode-right h))))
           (hord? (elem-priority (hnode-elem h))
                  (hnode-left h))
           (hord? (elem-priority (hnode-elem h))
                  (hnode-right h)))))

(define (rank h)
  (if (leaf? h)
      0
      (hnode-rank h)))

;; operations

(define empty-heap leaf)

(define (heap-empty? h)
  (leaf? h))

(define (heap-insert elt heap)
  (heap-merge heap (make-hnode elt leaf leaf)))

(define (heap-min heap)
  (hnode-elem heap))

(define (heap-pop heap)
  (heap-merge (hnode-left heap) (hnode-right heap)))

;;---------------------------------------HEAP-MERGE---------------------------------------
(define (heap-merge h1 h2)
  (cond
    [(leaf? h1) h2]
    [(leaf? h2) h1]
    [else
     (let ([h1-p (elem-priority (hnode-elem h1))]
           [h2-p (elem-priority (hnode-elem h2))])
       (cond 
       [(< h1-p h2-p)
        (make-hnode (hnode-elem h1) (hnode-left h1) (heap-merge h2 (hnode-right h1)))]
       [else
        (make-hnode (hnode-elem h2) (hnode-left h2) (heap-merge h1 (hnode-right h2)))]))]))
;;----------------------------------------------------------------------------------------

;;------------------------------------------TESTS------------------------------------------
(require rackunit)
;;lefist heap examples:
(define x '(hnode (9 . 3) 2 (hnode (10 . 1) 2 (hnode (11 . 2) 1 leaf leaf)
                                   (hnode (15 . 0) 1 leaf leaf))
                  (hnode (12 . 4) 1 (hnode (18 . 5) 1 leaf leaf) leaf)))

(define y '(hnode (19 . 3) 2 (hnode (20 . 1) 2 (hnode (21 . 2) 1 leaf leaf)
                                    (hnode (25 . 0) 1 leaf leaf))
                  (hnode (22 . 4) 1 (hnode (28 . 5) 1 leaf leaf) leaf)))

(define z '(hnode (1 . 3) 2 (hnode (3 . 1) 2 (hnode (6 . 2) 1 leaf leaf)
                                   (hnode (4 . 0) 1 leaf leaf))
                  (hnode (2 . 4) 1 (hnode (7 . 5) 1 leaf leaf) leaf)))

;;Merge-tests
(check-true (heap? (heap-merge 'leaf 'leaf)) "Merge heap failed for two empty heaps")
(check-true (heap? (heap-merge 'leaf x)) "Merge heap failed for first argument being empty heap")
(check-true (heap? (heap-merge x 'leaf)) "Merge heap failed for second argument being empty heap")
(check-true (heap? (heap-merge x x)) "Merge heap failed for two equal heaps")
(check-true (heap? (heap-merge x y)) "Merge heap failed for two different heaps (1)")
(check-true (heap? (heap-merge z y)) "Merge heap failed for two different heaps (2)")
(check-true (heap? (heap-merge z x)) "Merge heap failed for two different heaps (3)")
(check-within (heap-merge y x) (heap-merge x y) 0 "Merge heap failed: (merge-heap y x) not equal to (merge-heap x y)")
(check-within (heap-merge y z) (heap-merge z y) 0 "Merge heap failed: (merge-heap y z) not equal to (merge-heap z y)")