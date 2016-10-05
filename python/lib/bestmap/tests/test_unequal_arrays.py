# Test unequal length arrays
#

from random import shuffle
from bestmap import best_map

def test_unequal_arrays(iters=100, length=100):
    # This creates an array counting from 0, shuffles a copy and then
    # removes the last element of the shuffled copy.  best_map should
    # then construct a zero cost mapping, with one unmapped element
    # from a, and this should correspond to the element we popped from
    # b.
    #
    a = range(length)

    for i in range(iters):
        b = range(length)
        shuffle(b)
        l = b.pop()
        (mapping, unmapped_a, unmapped_b) = best_map(a, b,
                                                     lambda x, y: abs(x - y),
                                                     metric_dtype='i2')
        assert len(mapping) == min(len(a), len(b)), "mapping length wrong"
        assert sum(m[2] for m in mapping) == 0, "mapping cost greater than zero"
        assert len(unmapped_b) == 0, "unmapped elements in image"
        assert len(unmapped_a) == 1, "should be a single unmapped elt in domain"
        assert a[unmapped_a.pop()] == l, "unexpected unmapped element"
