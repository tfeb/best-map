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
    def doom(s):
        raise Exception(s)
    a = range(length)

    for i in range(iters):
        b = range(length)
        shuffle(b)
        l = b.pop()
        (mapping, unmapped_a, unmapped_b) = best_map(a, b,
                                                     lambda x, y: abs(x - y),
                                                     metric_dtype='i2')
        if sum(m[2] for m in mapping) > 0:
            doom("mapping cost greater than zero")
        if len(unmapped_b) > 0:
            doom("unmapped elements in image")
        if len(unmapped_a) != 1:
            doom("should be a single unmapped element in domain")
        if a[unmapped_a.pop()] != l:
            doom("unexpected unmapped element")
