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
    items = list(iterable)
    key = key or _identity
    keys = [key(item) for item in items]
    less = _less(reverse)

    def swap(i, j):
        items[i], items[j] = items[j], items[i]
        keys[i], keys[j] = keys[j], keys[i]

    def partition(lo, hi):
        mid = (lo + hi) // 2
        if less(keys[mid], keys[lo]):
            swap(mid, lo)
        if less(keys[hi], keys[lo]):
            swap(hi, lo)
        if less(keys[hi], keys[mid]):
            swap(hi, mid)
        swap(mid, hi)
        pivot = keys[hi]
        i = lo
        for j in range(lo, hi):
            if less(keys[j], pivot):
                swap(i, j)
                i += 1
        swap(i, hi)
        return i

    def sort(lo, hi):
        while lo < hi:
            pivot = partition(lo, hi)
            if pivot - lo < hi - pivot:
                sort(lo, pivot - 1)
                lo = pivot + 1
            else:
                sort(pivot + 1, hi)
                hi = pivot - 1

    if items:
        sort(0, len(items) - 1)
    return items
