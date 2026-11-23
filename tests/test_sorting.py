import random

import pytest

from ds.sorting import bubble_sort, quick_sort

SORTS = [bubble_sort, quick_sort]

CASES = [
    [],
    [1],
    [2, 1],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [3, 1, 2, 3, 1, 2],
    [7, 7, 7, 7],
    [-3, 10, 0, -1, 5],
    [1.5, -0.5, 2.25, 0.0],
    ["pear", "apple", "fig"],
]


@pytest.mark.parametrize("sort", SORTS)
@pytest.mark.parametrize("data", CASES)
def test_known_cases(sort, data):
    assert sort(data) == sorted(data)


@pytest.mark.parametrize("sort", SORTS)
def test_does_not_mutate_input(sort):
    data = [3, 1, 2]
    sort(data)
    assert data == [3, 1, 2]


@pytest.mark.parametrize("sort", SORTS)
def test_accepts_any_iterable(sort):
    assert sort((3, 1, 2)) == [1, 2, 3]
    assert sort(x for x in [2, 1]) == [1, 2]
    assert sort(range(3, 0, -1)) == [1, 2, 3]


@pytest.mark.parametrize("sort", SORTS)
def test_key_and_reverse(sort):
    words = ["ccc", "a", "bb"]
    assert sort(words, key=len) == ["a", "bb", "ccc"]
    assert sort([1, 3, 2], reverse=True) == [3, 2, 1]
    assert sort(words, key=len, reverse=True) == ["ccc", "bb", "a"]


@pytest.mark.parametrize("sort", SORTS)
@pytest.mark.parametrize("seed", range(10))
def test_random(sort, seed):
    rng = random.Random(seed)
    data = [rng.randint(-100, 100) for _ in range(rng.randint(0, 200))]
    assert sort(data) == sorted(data)


def test_quick_sort_large_input():
    data = list(range(5000))
    assert quick_sort(data) == data
    assert quick_sort(data[::-1]) == data
    assert quick_sort([5] * 5000) == [5] * 5000


@pytest.mark.parametrize("sort", SORTS)
def test_reverse_key_and_reverse_stability(sort):
    # Regression: quick_sort used to swap equal keys when reverse=True.
    data = [("a", 1), ("b", 0), ("c", 0), ("d", 1)]
    expected = [("b", 0), ("c", 0), ("a", 1), ("d", 1)]
    assert sort(data, key=lambda pair: pair[1]) == expected
    expected_reverse = [("a", 1), ("d", 1), ("b", 0), ("c", 0)]
    assert sort(data, key=lambda pair: pair[1], reverse=True) == expected_reverse


@pytest.mark.parametrize("sort", SORTS)
def test_matches_sorted_for_random_keyed_data(sort):
    rng = random.Random(3)
    for _ in range(20):
        data = [(rng.randrange(5), rng.random()) for _ in range(rng.randrange(0, 40))]
        for reverse in (False, True):
            assert sort(data, key=lambda p: p[0], reverse=reverse) == sorted(
                data, key=lambda p: p[0], reverse=reverse
            )


@pytest.mark.parametrize("sort", SORTS)
def test_stability_on_equal_keys(sort):
    data = [(1, "a"), (1, "b"), (0, "c"), (1, "d")]
    assert sort(data, key=lambda p: p[0]) == [(0, "c"), (1, "a"), (1, "b"), (1, "d")]


@pytest.mark.parametrize("sort", SORTS)
def test_returns_new_list(sort):
    data = [3, 1, 2]
    result = sort(data)
    assert isinstance(result, list)
    assert result is not data


def test_bubble_sort_integer_and_none_key():
    assert bubble_sort([2, 1], key=None) == [1, 2]
    assert quick_sort([2, 1], key=None) == [1, 2]

