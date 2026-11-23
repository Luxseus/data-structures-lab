def _identity(x):
    return x


def _less(reverse):
    return (lambda a, b: a > b) if reverse else (lambda a, b: a < b)


def bubble_sort(iterable, key=None, reverse=False):
    items = list(iterable)
    key = key or _identity
    less = _less(reverse)
    for end in range(len(items) - 1, 0, -1):
        swapped = False
        for i in range(end):
            if less(key(items[i + 1]), key(items[i])):
                items[i], items[i + 1] = items[i + 1], items[i]
                swapped = True
        if not swapped:
            break
    return items


def quick_sort(iterable, key=None, reverse=False):
    """Quicksort with a median-of-three pivot; returns a new list.

    Elements are grouped by key into "less", "equal" and "greater" buckets
    (three-way partition). The pivot is chosen without reordering anything and
    equal keys keep their original relative order, so the result is stable
    like ``sorted()``.
    """
    items = list(iterable)
    if not items:
        return items
    key = key or _identity
    keys = [key(item) for item in items]
    less = _less(reverse)

    def median_of_three(order, lo, hi):
        a, b, c = order[lo], order[(lo + hi) // 2], order[hi]
        if less(keys[b], keys[a]):
            a, b = b, a
        if less(keys[c], keys[b]):
            b, c = c, b
        if less(keys[b], keys[a]):
            a, b = b, a
        return b

    def three_way_partition(indices):
        pivot = keys[median_of_three(indices, 0, len(indices) - 1)]
        lower, equal, higher = [], [], []
        for index in indices:
            if less(keys[index], pivot):
                lower.append(index)
            elif less(pivot, keys[index]):
                higher.append(index)
            else:
                equal.append(index)
        return lower, equal, higher

    def sort(indices):
        if len(indices) < 2:
            return indices
        lower, equal, higher = three_way_partition(indices)
        return sort(lower) + equal + sort(higher)

    order = sort(list(range(len(items))))
    return [items[i] for i in order]
