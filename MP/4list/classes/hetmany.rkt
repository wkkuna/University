#lang racket
 
(define (map f xs)
    (if (null? xs)
        '()
         (cons (f (car xs)) (map f (cdr xs)))))


(define (concatMap f xs)
  (if (null? xs)
        '()
         (append (f (car xs)) (concatMap f (cdr xs)))))


; 1 2 3 -> 1 2 2 3 3 4
;chwilka

(define (from-to s e)
  (if (= s e) 
      (list e)
      (cons s (from-to (+ s 1) e))))

(define (queens board-size)
  ;; Return the representation of a board with 0 queens inserted
  (define (empty-board)
  '()) 
  ;; Return the representation of a board with a new queen at
  ;; (row, col) added to the partial representation `rest'
  (define (adjoin-position row col rest)
    (cons (cons row col) rest))
    
  ;; Return true if the queen in k-th column does not attack any of
  ;; the others
  (define (safe? k positions)
    (define row (caar positions))
    (define col (cdar positions))

    (define (horizontal li)
        ;; [(x1, k), (x2, k-1), (x3, k-2), .. , (xk, 1)]
        (if (null? li)
            #t
            (if (= row (caar li))
                #f
                (horizontal (cdr li)))))
    (define (diagonal i li)
        (if (null? li)
            #t
            (if (or (= (+ i row) (caar li) 
                    (= (- row i) (caar li)))
                #f
                (diagonal (+ i 1) (cdr li))))))
        
    (and (horizontal (cdr positions) 
         (diagonal 1 (cdr  positions)))))


  ;; Return a list of all possible solutions for k first columns
  (define (queen-cols k)
    (if (= k 0)
        (list (empty-board))
        (filter
         (lambda (positions) (safe? k positions))
         (concatMap
          (lambda (rest-of-queens)
            (map (lambda (new-row)
                   (adjoin-position new-row k rest-of-queens))
                 (from-to 1 board-size)))
          (queen-cols (- k 1))))))
  (queen-cols board-size))

[1 , 2, 3]

k+1
[ 
    
    [(1, k+1) (x1, k), (x2, k-1), (x3, k-2), .. , (xk, 1)],
    [(2, k+1) (x1, k), (x2, k-1), (x3, k-2), .. , (xk, 1)],
    [(3, k+1) (x1, k), (x2, k-1), (x3, k-2), .. , (xk, 1)]
    
    [],
    []
]