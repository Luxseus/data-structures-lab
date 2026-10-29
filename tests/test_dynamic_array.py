import random

import pytest

from ds.dynamic_array import DynamicArray


def test_empty():
    arr = DynamicArray()
    assert len(arr) == 0
    assert list(arr) == []
    assert arr.capacity >= 1


def test_init_from_iterable():
    arr = DynamicArray([1, 2, 3])
    assert list(arr) == [1, 2, 3]
    assert len(arr) == 3


def test_append_grows_capacity():
    arr = DynamicArray()
    for i in range(100):
        arr.append(i)
    assert len(arr) == 100
    assert list(arr) == list(range(100))
    assert arr.capacity >= 100


def test_getitem_setitem():
    arr = DynamicArray([1, 2, 3])
    assert arr[0] == 1
    assert arr[-1] == 3
    arr[1] = 20
    assert list(arr) == [1, 20, 3]
    with pytest.raises(IndexError):
        arr[3]
    with pytest.raises(IndexError):
        arr[-4] = 0


def test_insert():
    arr = DynamicArray([1, 3])
    arr.insert(1, 2)
    arr.insert(0, 0)
    arr.insert(len(arr), 4)
    assert list(arr) == [0, 1, 2, 3, 4]
    with pytest.raises(IndexError):
        arr.insert(10, 0)


def test_pop():
    arr = DynamicArray([1, 2, 3, 4])
    assert arr.pop() == 4
    assert arr.pop(0) == 1
    assert list(arr) == [2, 3]
    arr.pop()
    arr.pop()
    with pytest.raises(IndexError):
        arr.pop()


def test_shrinks_after_many_pops():
    arr = DynamicArray(range(500))
    big = arr.capacity
    while len(arr) > 1:
        arr.pop()
    assert arr.capacity < big


def test_index_remove_contains():
    arr = DynamicArray([5, 6, 7, 6])
    assert arr.index(6) == 1
    assert 7 in arr
    assert 42 not in arr
    arr.remove(6)
    assert list(arr) == [5, 7, 6]
    with pytest.raises(ValueError):
        arr.remove(42)
    with pytest.raises(ValueError):
        arr.index(42)


def test_extend_clear_repr():
    arr = DynamicArray([1])
    arr.extend([2, 3])
    assert list(arr) == [1, 2, 3]
    assert repr(arr) == "DynamicArray([1, 2, 3])"
    arr.clear()
    assert len(arr) == 0
    assert list(arr) == []
    assert arr == DynamicArray()


def test_random_operations_match_list():
    rng = random.Random(1)
    arr, ref = DynamicArray(), []
    for _ in range(300):
        op = rng.randrange(4)
        if op == 0 or not ref:
            x = rng.randrange(50)
            arr.append(x)
            ref.append(x)
        elif op == 1:
            i = rng.randrange(len(ref) + 1)
            x = rng.randrange(50)
            arr.insert(i, x)
            ref.insert(i, x)
        elif op == 2:
            i = rng.randrange(len(ref))
            assert arr.pop(i) == ref.pop(i)
        else:
            i = rng.randrange(len(ref))
            x = rng.randrange(50)
            arr[i] = x
            ref[i] = x
        assert list(arr) == ref
