"""Utilities for liberating values from restrictive collections."""


def liberator(values, blocked_values):
    """Return values that are not blocked while preserving order.

    Parameters
    ----------
    values : iterable
        Items to process.
    blocked_values : iterable
        Items that should be removed from ``values``.

    Returns
    -------
    list
        A list containing only values that do not appear in ``blocked_values``.
    """
    blocked_set = set(blocked_values)
    return [value for value in values if value not in blocked_set]
