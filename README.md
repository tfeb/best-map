# Computing the best map between two sets of objects
Given two sets of objects, in some kind of container indexed by small
integers, and a metric function which computes distances between
objects in one set and objects in another, then this code computes the
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

There is [documentation](python/README.md) for this.

### `racket`
This is the original proof-of-concept, implemented in
[Racket](http://racket-lang.org/).  It has no pretensions to be
production-quality code: it's just here for the record.

## Builds and tests
I have removed the Travis CI tests: it should still pass any tests
that it used to as nothing else has changed: `make test` in the
`python` directory will run them.

There are unit tests for the Racket module, which you can run with
`raco test` if you want (or `make test` in the `racket` directory).