# https://numpy.org/doc/stable/reference/routines.sort.html
import numpy as np

from numgrad._vjp import _bind_vjp


def _unpermute(a, permutation, axis):
    unpermutation = np.zeros(a.shape, dtype=int)
    np.put_along_axis(
        unpermutation,
        permutation,
        np.argsort(np.ones(a.shape, dtype=int), axis),
        axis,
    )
    return np.take_along_axis(a, unpermutation, axis)


def _sort_vjp(g, r, a, axis=-1):
    if axis is None:
        return _unpermute(g, np.argsort(a, axis), 0).reshape(a.shape)
    return _unpermute(g, np.argsort(a, axis), axis)


# https://numpy.org/doc/stable/reference/routines.sort.html#sorting
_bind_vjp(np.sort, _sort_vjp)
