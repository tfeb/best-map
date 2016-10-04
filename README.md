# Computing the best map between two sets of objects
[This README is extremely preliminary and there is no serious
documentation at all so far: *caveat emptor*.]

Given two sets of objects (in some kind of container indexed by small
integers) and a metric function which computes distances between
objects in one set and objects in another, then this computes the
mapping between the two sets which minimises the total distance.

For a long time I thought this must be equivalent to something like
the travelling salesman problem, but it's actually much more
tractable.

## What is here

### `python`
This contains a Python package, installable with 2.6 and 2.7 at least,
which implements the algorithm.  There are unit tests, a `setup.py`
and so on.  You need [NumPy](http://www.numpy.org/) to use it, and
[nose](https://nose.readthedocs.io/en/latest/) to run the unit tests.

### `racket`
This is the original proof-of-concept, implemented in
[Racket](http://racket-lang.org/).  It has no pretensions to be
production-quality code: it's just here for the record,

## Builds and tests
[![Build Status](https://travis-ci.org/tfeb/best-map.svg)](https://travis-ci.org/tfeb/best-map)

This status corresponds to
[`github.com/tfeb/best-map`](https://github.com/tfeb/best-map) and may
not completely correspond to the status of any other repo.