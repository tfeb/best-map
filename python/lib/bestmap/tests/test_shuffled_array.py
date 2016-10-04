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
    def doom(s):
        raise Exception(s)

    a = [random() for i in range(length)]
    b = [e for e in a]

    for i in range(iters):
        shuffle(b)
        (mapping, unmapped_a, unmapped_b) = best_map(a, b,
                                                     lambda x, y: abs(x - y),
                                                     metric_dtype='double')
        # Check that there are no unmapped objects
        if len(unmapped_a) > 0 or len(unmapped_b) > 0:
            doom("unmapped elements")
        # Check for zero cost
        if sum(m[2] for m in mapping) > 0.0:
            doom("mapping cost greater than zero")


def test_shuffled_indexed_array(iters=100, length=100):
    # The idea of this is create an array, shuffle a copy of it, and
    # then ask best_map to construct a mapping: this mapping should
    # always have zero cost, should never have unmapped elements and
    # should map elements onto their shuffled counterparts.  We do
    # this a bunch of times.
    #
    def doom(s):
        raise Exception(s)

    a = [(i,i) for i in range(length)]
    b = [e for e in a]
    for i in range(iters):
        shuffle(b)
        (mapping, unmapped_a, unmapped_b) = best_map(a, b,
                                                     lambda x, y: abs(x - y),
                                                     key=lambda e: e[1],
                                                     metric_dtype='u2')
        # Check that there are no unmapped objects
        if len(unmapped_a) > 0 or len(unmapped_b) > 0:
            doom("unmapped elements")
        # Check for zero cost
        if sum(m[2] for m in mapping) > 0:
            doom("mapping cost greater than zero")
        for (li, ri, c) in mapping:
            if a[li] != b[ri]:
                doom("mapping failed miserably")
