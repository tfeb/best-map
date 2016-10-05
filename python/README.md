# The best map
This package provides a function which will compute the best map
between two sets of objects for a specified metric.

## The algorithm
Given an object from each set then the distance, or cost, of the
mapping between them is given by the metric function.  The best
mapping between the two sets of objects is then the one which
minimises the total distance amongst all possible pairings.

This is computed as follows:
* for each object in the first set, record the distance to each object
  in the second set as well as the two objects concerned;
* sort this set of distances in increasing order;
* now iterate over the distances, and for each entry, if neither
  object has already been paired then add this pairing to the result;
* continue this until all objects from one set have been used: the
  resulting set of pairings is the best map.

Note that if the two sets are different sizes then there will be
unpaired elements from the larger set.

## The implementation
The package `bestmap` contains a single function, `best_map`:

```python
best_map(domain, image, metric,
         key=None, domain_key=None, image_key=None,
         metric_dtype='float')
    -> (mappings, domain_unmapped, image_unmapped)
```

This computes the best mapping between `domain` and `image` using
`metric` as the distance function.

* `domain` and `image` contain the objects to map.  They need to be
  iterable, and indexable by small integers: `domain[i]` is the `i`th
  element of `domain` & similarly for `image`. The mapping is returned
  in terms of pairs of indices.
* `metric` is a function of two arguments which returns the distance
  between its arguments.  The return value needs to be something that
  can be stored in a NumPy array of dtype `metric_dtype`, and needs to
  be a type that NumPy knows how to sort.
* `key`, `domain_key` and `image_key`, if given, specify functions of
  one argument which are applied to the elements of `domain` and
  `image` and should return a suitable value for an argument to
  `metric`.  If only `key` is given then it is used as the defaul for
  both `domain` and `range`, if `domain_key` or `range_key` is given
  then they override the default for the corresponding argument.
* `metric_dtype` specifies the NumPy `dtype` for the array which holds
  the results of calling `metric`.  See `metric` for constraints on
  this.

The return values are as follows.

* `mappings`: this is a list of tuples of the form `(from, to,
  distance)`, where `from` is an index of `domain`, `to` is an index
  of `image` and `distance` is the cost of the mapping.  The mappings
  don't appear in any particular order (in practice they appear in
  order of increasing `distance`, but don't rely on this).
* `domain_unmapped` and `image_unmapped` are sets of indices for
  `domain` and `image` respectively.  Only one of these will be
  non-empty: if `domain` is larger than `range` then `domain_unmapped`
  will contain the unmapped indices from `domain` `image_unmapped`
  will be empty & *vice versa*.

`domain` and `image` should have no more than 65536 ($2^{16}$)
elements.  In practice, since the algorithm is at least quadratic in
time and space, this is not a restriction.

If just `key` is given then `metric` is called essentially as
`metric(key(domain[i]), key(image[j]))`; if, for instance, just
`domain_key` is given then it would be called as
`metric(domain_key(domain[i]), image[j])`; if none of the `key*`
arguments are given then it is called as `metric(domain[i],
image[j])`.

## Notes
You can compute the cost of a mapping by, for example,

```python
(mappings, domain_unmapped, image_unmapped) = best_map(domain, image, metric)
cost = sum(mapping[2] for mapping in mappings)
```

## An example
This creates an array of random floats, shuffles a copy and then uses
`best_map` to compute the mapping.  The mapping will depend on the
details of the shuffling, but its cost should always be zero.

```python

from random import shuffle, random
from bestmap import best_map

# Create the two arrays
a = [random() for i in range(100)]
b = [e for e in a]
shuffle(b)                      # permute b in some indeterminate way

(mappings, unmapped_a, unmapped_b) = best_map(a, b, lambda x, y: abs(x-y),
                                              metric_dtype='double')

# Sanity checks
assert len(unmapped_a) == 0, "unmapped elts in a"
assert len(unmapped_b) == 0, "unmapped elts in b"
assert sum(mapping[2] for mapping in mappings) == 0.0, "nonzero mapping cost"

# The mappings are not interesting, but print them anyway
for (x, y, d) in mappings:
    print "{} -> {} cost {}".format(x, y, d)
```

(Note that the mapping cost is identically `0.0`: the float comparison
is OK here.)