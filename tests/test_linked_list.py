import random

import pytest

from ds.linked_list import LinkedList


def test_empty():
    lst = LinkedList()
    assert len(lst) == 0
    assert list(lst) == []


def test_init_from_iterable():
    lst = LinkedList([1, 2, 3])
    assert list(lst) == [1, 2, 3]
    assert len(lst) == 3


def test_append_and_prepend():
    lst = LinkedList()
    lst.append(2)
    lst.append(3)
    lst.prepend(1)
    assert list(lst) == [1, 2, 3]


def test_insert():
    lst = LinkedList([1, 3])
    lst.insert(1, 2)
    lst.insert(0, 0)
    lst.insert(4, 4)
    assert list(lst) == [0, 1, 2, 3, 4]


def test_insert_out_of_range():
    lst = LinkedList([1])
    with pytest.raises(IndexError):
        lst.insert(5, 0)
    with pytest.raises(IndexError):
        lst.insert(-1, 0)


def test_getitem_setitem():
    lst = LinkedList([10, 20, 30])
    assert lst[0] == 10
    assert lst[-1] == 30
    lst[1] = 25
    assert list(lst) == [10, 25, 30]
    with pytest.raises(IndexError):
        lst[3]
    with pytest.raises(IndexError):
        lst[-4] = 0


def test_pop():
    lst = LinkedList([1, 2, 3, 4])
    assert lst.pop() == 4
    assert lst.pop(0) == 1
    assert lst.pop(1) == 3
    assert list(lst) == [2]
    assert lst.pop() == 2
    assert len(lst) == 0
    with pytest.raises(IndexError):
        lst.pop()


def test_append_after_pop_last():
    lst = LinkedList([1, 2])
    lst.pop()
    lst.append(3)
    assert list(lst) == [1, 3]


def test_remove_index_contains():
    lst = LinkedList([1, 2, 3, 2])
    assert 3 in lst
    assert 9 not in lst
    assert lst.index(3) == 2
    lst.remove(2)
    assert list(lst) == [1, 3, 2]
    with pytest.raises(ValueError):
        lst.remove(42)
    with pytest.raises(ValueError):
        lst.index(42)


def test_reverse():
    lst = LinkedList([1, 2, 3])
    lst.reverse()
    assert list(lst) == [3, 2, 1]
    lst.append(0)
    assert list(lst) == [3, 2, 1, 0]


def test_clear_eq_repr():
    lst = LinkedList([1, 2])
    assert repr(lst) == "LinkedList([1, 2])"
    assert lst == LinkedList([1, 2])
    assert lst != LinkedList([2, 1])
    lst.clear()
    assert len(lst) == 0
    assert list(lst) == []


def test_random_operations_match_list():
    rng = random.Random(2)
    lst, ref = LinkedList(), []
    for _ in range(300):
        op = rng.randrange(4)
        if op == 0 or not ref:
            x = rng.randrange(50)
            lst.append(x)
            ref.append(x)
        elif op == 1:
            x = rng.randrange(50)
            lst.prepend(x)
            ref.insert(0, x)
        elif op == 2:
            i = rng.randrange(len(ref))
            assert lst.pop(i) == ref.pop(i)
        else:
            i = rng.randrange(len(ref))
            x = rng.randrange(50)
            lst[i] = x
            ref[i] = x
        assert list(lst) == ref
