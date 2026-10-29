import random

import pytest

from ds.avl_tree import AVLTree


def check_invariants(tree):
    def walk(node, lo, hi):
        if node is None:
            return 0
        assert (lo is None or node.key > lo) and (hi is None or node.key < hi)
        left = walk(node.left, lo, node.key)
        right = walk(node.right, node.key, hi)
        assert abs(left - right) <= 1
        assert node.height == 1 + max(left, right)
        return node.height

    return walk(tree._root, None, None)


def test_empty():
    t = AVLTree()
    assert len(t) == 0
    assert list(t) == []
    assert 1 not in t
    assert t.height() == 0
    with pytest.raises(ValueError):
        t.min()
    with pytest.raises(ValueError):
        t.max()


def test_insert_and_inorder():
    t = AVLTree()
    for key in [5, 3, 8, 1, 4, 7, 9]:
        t.insert(key)
    assert list(t) == [1, 3, 4, 5, 7, 8, 9]
    assert len(t) == 7
    assert t.min() == 1
    assert t.max() == 9
    check_invariants(t)


def test_duplicates_are_ignored():
    t = AVLTree([2, 2, 1])
    assert len(t) == 2
    assert list(t) == [1, 2]


@pytest.mark.parametrize(
    "keys",
    [
        [3, 2, 1],  # LL
        [1, 2, 3],  # RR
        [3, 1, 2],  # LR
        [1, 3, 2],  # RL
    ],
)
def test_rotations(keys):
    t = AVLTree(keys)
    assert t._root.key == 2
    assert t.height() == 2
    check_invariants(t)


def test_sorted_insert_stays_balanced():
    t = AVLTree(range(1023))
    check_invariants(t)
    assert t.height() <= 21


def test_delete():
    t = AVLTree(range(10))
    t.delete(0)
    t.delete(3)
    t.delete(t._root.key)
    assert 0 not in t and 3 not in t
    assert len(t) == 7
    check_invariants(t)
    with pytest.raises(KeyError):
        t.delete(100)


def test_delete_all():
    rng = random.Random(5)
    keys = list(range(200))
    t = AVLTree(keys)
    rng.shuffle(keys)
    for key in keys:
        t.delete(key)
        check_invariants(t)
    assert len(t) == 0
    assert list(t) == []


def test_random_against_set():
    rng = random.Random(42)
    t, ref = AVLTree(), set()
    for _ in range(2000):
        key = rng.randrange(400)
        if rng.random() < 0.6:
            t.insert(key)
            ref.add(key)
        elif key in ref:
            t.delete(key)
            ref.remove(key)
        else:
            with pytest.raises(KeyError):
                t.delete(key)
        assert len(t) == len(ref)
    assert list(t) == sorted(ref)
    check_invariants(t)


def test_clear_and_repr():
    t = AVLTree([2, 1])
    assert repr(t) == "AVLTree([1, 2])"
    t.clear()
    assert len(t) == 0
    assert list(t) == []
