#lang racket

;;; Racket sample code to compute best map between two sets of objects
;;; (such as dreq rows)
;;;

(provide best-map (struct-out distance))

(module+ test
  (require rackunit))

(struct distance
  (src tgt d)
  #:transparent)

(define (best-map sources targets metric)
  ;; The best map is the one most like a bijection
  ;; and with the shortest total length.
  ;; Return this map as a list of distances, and two lists:
  ;; - sources which have no mapping;
  ;; - targets which are not mapped.
  ;;
  ;; I think this is something like n^2 log n^2,
  ;; assuming sort is n log n
  (let ([ss (mutable-seteqv)]
        [ts (mutable-seteqv)])
    (values (for/list ([d (sort (for*/list ([src sources]
                                            [tgt targets])
                                  (distance src tgt (metric src tgt)))
                                ;; caching keys makes it a bit faster
                                ;; as best I can see
                                < #:key distance-d #:cache-keys? #t)]
                       #:unless (or (set-member? ss (distance-src d))
                                    (set-member? ts (distance-tgt d))))
              (set-add! ss (distance-src d))
              (set-add! ts (distance-tgt d))
              d)
            (set-subtract (list->seteqv sources) ss)
            (set-subtract (list->seteqv targets) ts))))

(module+ test
  (provide make-random-points euclidean)
  
  (define (make-random-points n)
    (for/list ([i n])
      (cons (random) (random))))

  (define (euclidean s d)
    (sqrt (+ (expt (- (car s) (car d)) 2)
             (expt (- (cdr s) (cdr d)) 2))))

  (let ([points (make-random-points 20)])
    (let-values ([(dists ms md) (best-map points points euclidean)])
      (check-eqv? (length dists) 20)
      (check-pred set-empty? ms)
      (check-pred set-empty? md)))

  (let ([p1 (make-random-points 10)]
        [p2 (make-random-points 20)])
    (let-values ([(dists ms md) (best-map p1 p2 euclidean)])
      (check-eqv? (length dists) 10)
      (check-pred set-empty? ms)
      (check-eqv? (set-count md) 10)
      (check-pred (λ (dl)
                    (define (checker c tl)
                      (if (null? tl)
                          #t
                          (let ((n (distance-d (first tl))))
                            (and (<= c n)
                                 (checker n (rest tl))))))
                    (checker (distance-d (first dl)) (rest dl)))
                  dists))))

(module+ bench
  (require (submod ".." test))
  (provide time-n-points m-n-points-ratio)

  (define (time-n-points n (trials 100))
    (let ((points (make-random-points n)))
      (/ (for/sum ([trial trials])
           (let-values ([(junk cpu real gc)
                         (time-apply
                          best-map (list points points euclidean))])
             real))
         trials)))

  (define (m-n-points-ratio m n (trials 100))
    (/ (time-n-points m trials)
       (time-n-points n trials))))