# The best map
#

__all__ = ('best_map',)

from numpy import empty

def best_map(domain, image, metric,
             key=None, domain_key=None, image_key=None):
    if domain_key is None:
        domain_key = key
    if image_key is None:
        image_key = key
    if len(domain) >= 1<<16 or len(image) >= 1<<16:
        raise ValueError("lengths should be less than 2**16")
    # Compute the values, creating new arrays only if necessary. Doing
    # this in advance means we don't have to care about memoizing the
    # key functions: we will call them for each element of each array
    # anyway, so this is how big the caches would need to be.
    dvs = domain if domain_key is None else map(domain_key, domain)
    ivs = image if image_key is None else map(image_key, image)
    dlen = len(dvs)
    ilen = len(ivs)
    distances = empty((dlen, ilen),
                      dtype=[('x', 'u2'),
                             ('y', 'u2'),
                             ('d', 'float')])
    for (x, xe) in enumerate(dvs):
        for (y, ye) in enumerate(ivs):
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
    for (x, y, d) in distances:
        if x in unmapped_xs and y in unmapped_ys:
            mappings.append((x, y, d))
            unmapped_xs.remove(x)
            unmapped_ys.remove(y)
    return (mappings, unmapped_xs, unmapped_ys)
