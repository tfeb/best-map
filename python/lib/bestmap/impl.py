# The best map
#

__all__ = ('best_map',)

from numpy import empty

def best_map(domain, image, metric,
             key=None, domain_key=None, image_key=None,
             metric_dtype='float'):
    """Compute the best map between two sets of objects, using a metric.

    Given two sets of objects and a metric function which provides a
    distance between objects in the first and second set, the best map
    is the pairing of objects which minimises the total distance.

    Arguments:
    - domain -- the first set of objects (domain of a function);
    - image -- the second set of objects (image of a function);
    - metric -- the metric function;
    - key, domain_key, image_key -- if given these are key functions
      which extract a value from both domain and image, or just domain
      and image which is used as the corresponding argument to the
      metric function -- by default the objects themselves are used;
    - metric_dtype -- if given this is a NumPy dtype which describes
      the type of the return value of the metric function -- this is
      used as the dtype of the array of results of the function, and
      must be something NumPy knows how to sort -- the default is
      'float', which is reasonably safe for any real numeric type
      (although floating-point rounding might be a problem).

    Although domain and image are described here as sets of objects
    they should actually be tuples, lists or some other type indexed
    by integers.

    The function returns a tuple of threee elements:
    - a list of tuples of the form (dom_index, img_index, distance),
      each of which describes a mapping between an element of domain
      and of image together with the distance between them, so
      domain[dom_index] is mapped to image[img_index];
    - a set of indices from domain which have no mappings;
    - a set of indices from image which have no mappings.

    Note that if the domain and image are the same size there will
    never be any unmapped elements, and that only one of the sets will
    ever have any elements in it.

    Note that you can compute the total cost of the mappings by, for
    instance sum(mapping[2] for mapping in mappings).

    The domain and image can have no more than 65536 elements (and if
    you try sizes anything like that big the function will be
    *extremely* slow and require a lot of memory).

    The algorithm is at least quadratic both time and space in the size
    of the domain and image, and in fact slightly worse than that.

    """
    # Default the keys and sanity check the set sizes.
    if domain_key is None:
        domain_key = key
    if image_key is None:
        image_key = key
    if len(domain) >= 1<<16 or len(image) >= 1<<16:
        # Two 65536 elt arrays would require 64GB of memory I think:
        # don't even think about it.
        raise ValueError("array lengths should be 16 bit numbers")
    # Compute the values, creating new arrays only if necessary. Doing
    # this in advance means we don't have to care about memoizing the
    # key functions: we will call them for each element of each array
    # anyway, so this is how big the caches would need to be.
    dom = domain if domain_key is None else map(domain_key, domain)
    img = image if image_key is None else map(image_key, image)
    dlen = len(dom)
    ilen = len(img)
    # Create and populate a big two dimensional array of distances
    distances = empty((dlen, ilen),
                      dtype=[('x', 'u2'),
                             ('y', 'u2'),
                             ('d', metric_dtype)])
    for (x, xe) in enumerate(dom):
        for (y, ye) in enumerate(img):
            distances[x, y] = (x, y, metric(xe, ye))
    # Reshape the array to be one dimensional, and sort it in
    # increasing order of distance
    distances.shape = reduce(lambda a, b: a*b, distances.shape, 1)
    distances.sort(order='d')
    # Now go through distances, noting the mappings.  Everything here
    # works on indices.
    unmapped_xs = set(range(dlen))
    unmapped_ys = set(range(ilen))
    mappings = list()
    remaining = min(dlen, ilen) # how many left to do?
    for (x, y, d) in distances:
        if x in unmapped_xs and y in unmapped_ys:
            mappings.append((x, y, d))
            unmapped_xs.remove(x)
            unmapped_ys.remove(y)
            remaining -= 1
            if remaining == 0:
                # We are done: sanity check and finish
                assert len(unmapped_xs) == 0 or len(unmapped_ys) == 0, "oops"
                break
    return (mappings, unmapped_xs, unmapped_ys)
