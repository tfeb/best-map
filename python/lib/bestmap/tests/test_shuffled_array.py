# Test that best_map will untangle randomly shuffled arrays
#

from random import shuffle, random
from bestmap import best_map

def test_shuffled_float_array(iters=100, length=100):
    # Create an array of random floats, shuffle a copy and get
    # best_map to find a mapping: it should have zero (actually zero,
    # not epsilon, if you think) cost and no unmapped elements.  Do it
    # a bunch of times.
    #
    a = [random() for i in range(length)]
    b = [e for e in a]

    for i in range(iters):
        shuffle(b)
        (mapping, unmapped_a, unmapped_b) = best_map(a, b,
                                                     lambda x, y: abs(x - y),
                                                     metric_dtype='double')
        # Check every element is mapped
        assert len(mapping) == len(a), "wrong mapping length"
        # Check that there are no unmapped objects
        assert (len(unmapped_a) == 0
                and len(unmapped_b) == 0), "unmapped elements"
        assert sum(m[2] for m in mapping) == 0.0, "mapping cost > zero"


def test_shuffled_indexed_array(iters=100, length=100):
    # The idea of this is create an array, shuffle a copy of it, and
    # then ask best_map to construct a mapping: this mapping should
    # always have zero cost, should never have unmapped elements and
    # should map elements onto their shuffled counterparts.  We do
    # this a bunch of times.
    #
    a = [(i,i) for i in range(length)]
    b = [e for e in a]
    for i in range(iters):
        shuffle(b)
        (mapping, unmapped_a, unmapped_b) = best_map(a, b,
                                                     lambda x, y: abs(x - y),
                                                     key=lambda e: e[1],
                                                     metric_dtype='u2')
        # Check every element is mapped
        assert len(mapping) == len(a), "wrong mapping length"
        # Check that there are no unmapped objects
        assert (len(unmapped_a) == 0
                and len(unmapped_b) == 0), "unmapped elements"
        # Check for zero cost
        assert sum(m[2] for m in mapping) == 0, "mapping cost > zero"
        # And check the mapping is what we expect it to be
        for (li, ri, c) in mapping:
            assert a[li] == b[ri], "mapping failed miserably"
