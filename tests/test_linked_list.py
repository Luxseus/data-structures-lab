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


def test_tail_stays_correct_after_operations():
    # Tail bookkeeping is the classic bug source for a singly linked list:
    # every path is checked through an append at the very end.
    lst = LinkedList([1, 2, 3])
    lst.pop()
    lst.append(4)
    assert list(lst) == [1, 2, 4]
    lst.pop(0)
    lst.append(5)
    assert list(lst) == [2, 4, 5]
    lst.reverse()
    lst.append(6)
    assert list(lst) == [5, 4, 2, 6]
    lst.clear()
    lst.append(7)
    assert list(lst) == [7]
    assert lst.pop() == 7
    assert len(lst) == 0


def test_getitem_setitem_out_of_range():
    lst = LinkedList([1, 2])
    for bad in (2, -3, 100):
        with pytest.raises(IndexError):
            lst[bad]
        with pytest.raises(IndexError):
            lst.pop(bad)


def test_insert_bounds_match_list_semantics():
    lst = LinkedList([1, 2, 3])
    with pytest.raises(IndexError):
        lst.insert(-1, 0)
    lst.insert(3, 4)
    assert list(lst) == [1, 2, 3, 4]


def test_truthiness():
    assert not LinkedList()
    assert LinkedList([0])


def test_index_returns_first_occurrence():
    lst = LinkedList([1, 2, 2, 3])
    assert lst.index(2) == 1


def test_iteration_while_appending_terminates():
    # Appending during iteration must not loop forever: the walker follows
    # ``next`` pointers, so new nodes are simply visited too.
    lst = LinkedList(range(5))
    count = 0
    for _ in lst:
        count += 1
        if count <= 5:
            lst.append(None)
    assert count == 10

