#lang racket
;; Wiktoria Kuna 316418 
(provide philosopher)

;; Dijkstra's solution
(define (philosopher dining-table k)
  (let ([f1 k]
        [f2 (modulo (+ k 1) 5)])
    (if (< f1 f2)
        (begin 
          ((dining-table 'pick-fork) f1)
          ((dining-table 'pick-fork) f2)
          ((dining-table 'put-fork) f2)
          ((dining-table 'put-fork) f1))
        (begin
          ((dining-table 'pick-fork) f2)
          ((dining-table 'pick-fork) f1)
          ((dining-table 'put-fork) f1)
          ((dining-table 'put-fork) f2)))))