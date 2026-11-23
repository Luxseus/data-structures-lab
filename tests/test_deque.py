import collections
import random

import pytest

from ds.deque import Deque


def test_empty():
    d = Deque()
    assert len(d) == 0
    assert list(d) == []
    with pytest.raises(IndexError):
        d.pop()
    with pytest.raises(IndexError):
        d.popleft()
    with pytest.raises(IndexError):
        d.peek()
    with pytest.raises(IndexError):
        d.peekleft()


def test_append_both_ends():
    d = Deque()
    d.append(2)
    d.append(3)
    d.appendleft(1)
    d.appendleft(0)
    assert list(d) == [0, 1, 2, 3]
    assert d.peekleft() == 0
    assert d.peek() == 3


def test_pop_both_ends():
    d = Deque([1, 2, 3, 4])
    assert d.pop() == 4
    assert d.popleft() == 1
    assert list(d) == [2, 3]


def test_indexing():
    d = Deque([1, 2, 3])
    d.appendleft(0)
    assert d[0] == 0
    assert d[-1] == 3
    d[1] = 10
    assert list(d) == [0, 10, 2, 3]
    with pytest.raises(IndexError):
        d[4]


def test_growth_with_wraparound():
    d = Deque()
    for i in range(50):
        d.appendleft(-i)
        d.append(i)
    assert len(d) == 100
    assert list(d) == list(range(-49, 1)) + list(range(50))


def test_clear_eq_repr():
    d = Deque([1, 2])
    assert repr(d) == "Deque([1, 2])"
    assert d == Deque([1, 2])
    assert 2 in d
    assert 5 not in d
    d.clear()
    assert len(d) == 0
    assert list(d) == []


def test_matches_collections_deque():
    rng = random.Random(0)
    mine, ref = Deque(), collections.deque()
    for _ in range(3000):
        op = rng.randrange(6)
        if op == 0 or not ref:
            x = rng.randrange(100)
            mine.append(x)
            ref.append(x)
        elif op == 1:
            x = rng.randrange(100)
            mine.appendleft(x)
            ref.appendleft(x)
        elif op == 2:
            assert mine.pop() == ref.pop()
        elif op == 3:
            assert mine.popleft() == ref.popleft()
        elif op == 4:
            assert mine.peek() == ref[-1]
        else:
            i = rng.randrange(len(ref))
            assert mine[i] == ref[i]
        assert len(mine) == len(ref)
    assert list(mine) == list(ref)


def test_wraparound_last_index_and_pop():
    # Regression for ring-buffer indexing: after the head wraps past the end
    # of the backing list, negative and last indices must still resolve.
    d = Deque()
    for i in range(30):
        d.append(i)
    for _ in range(25):
        d.popleft()
    for i in range(30, 40):
        d.append(i)
    assert len(d) == 15
    assert list(d) == list(range(25, 40))
    assert d[-1] == 39
    assert d.peek() == 39
    assert d.pop() == 39
    assert list(d) == list(range(25, 39))


def test_pop_all_then_reuse():
    d = Deque(range(10))
    while d:
        d.popleft()
    assert len(d) == 0
    for i in range(20):
        d.append(i)
    assert list(d) == list(range(20))


def test_getitem_out_of_range():
    d = Deque([1, 2, 3])
    for bad in (3, -4, 100):
        with pytest.raises(IndexError):
            d[bad]


def test_truthiness():
    assert not Deque()
    assert Deque([0])


def test_reverse_and_duplicates_containment():
    d = Deque([1, 1, 2])
    assert list(reversed(list(d))) == [2, 1, 1]
    assert 1 in d
    d[-1] = 3
    assert list(d) == [1, 1, 3]


def test_equality_with_other_iterables():
    d = Deque([1, 2])
    assert d == Deque([1, 2])
    assert d == [1, 2]
    assert d == (1, 2)
    assert d != [2, 1]
    assert (d == "12") is False

