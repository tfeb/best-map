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

## Builds and tests
[![Build Status](https://travis-ci.org/tfeb/best-map.svg)](https://travis-ci.org/tfeb/best-map)

This status corresponds to
[`github.com/tfeb/best-map`](https://github.com/tfeb/best-map) and may
not completely correspond to the status of any other repo.