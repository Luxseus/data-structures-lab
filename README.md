# data-structures-lab

Структуры данных и сортировки на Python (TDD: сначала тесты, потом код).

| Модуль | Что внутри |
|---|---|
| `ds/dynamic_array.py` | Динамический массив `DynamicArray`: доступ по индексу, рост и сжатие буфера |
| `ds/linked_list.py` | Односвязный список `LinkedList` |
| `ds/deque.py` | Дек `Deque` на кольцевом буфере |
| `ds/avl_tree.py` | АВЛ-дерево `AVLTree`: вставка, удаление, поиск, обход |
| `ds/sorting.py` | Сортировки `bubble_sort` и `quick_sort` (поддерживают `key` и `reverse`) |

## Что умеет каждая структура

Все контейнеры поддерживают `len()`, итерацию, `in`, `==` (с таким же контейнером,
`list` и `tuple`), `repr()` и `clear()`.

- **`DynamicArray`** — `append`, `insert(index, value)`, `pop(index=-1)`, `index`,
  `remove`, `extend`, `len`, индексация `arr[i]` / `arr[i] = x`. Буфер удваивается при
  заполнении и сжимается в два раза, когда занято не больше четверти.
- **`LinkedList`** — `append`, `prepend`, `insert(index, value)`, `pop(index=-1)`,
  `index`, `remove`, `reverse`, индексация. Есть указатель на хвост, поэтому `append`
  и `pop()` работают за O(1).
- **`Deque`** — `append`, `appendleft`, `pop`, `popleft`, `peek`, `peekleft`,
  индексация. Реализован на кольцевом буфере, вставка и удаление с обоих концов
  амортизированно O(1).
- **`AVLTree`** — `insert`, `delete`, `min`, `max`, `height`, `in`, обход в порядке
  возрастания (итерация). Дерево само балансируется поворотами, высота — O(log n).
- **`bubble_sort` / `quick_sort`** — `f(iterable, key=None, reverse=False)`, возвращают
  новый список и не меняют вход. Оба **стабильны**: равные ключи сохраняют исходный
  порядок, как у `sorted()`.

## Исключения

| Ситуация | Исключение |
|---|---|
| Индекс вне диапазона, `pop`/`peek` из пустого | `IndexError` |
| Удаление отсутствующего значения (`remove`, `index`) | `ValueError` |
| `AVLTree.delete` отсутствующего ключа | `KeyError` |
| `AVLTree.min` / `max` на пустом дереве | `ValueError` |
| Проверка `key in tree` с несравнимым типом | не исключение, просто `False` |

## Примеры

```python
from ds.deque import Deque
from ds.avl_tree import AVLTree
from ds.sorting import quick_sort

d = Deque([2, 3])
d.appendleft(1)
d.append(4)
assert list(d) == [1, 2, 3, 4]

tree = AVLTree([5, 3, 8])
tree.insert(4)
assert list(tree) == [3, 4, 5, 8]
assert 4 in tree and "4" not in tree

assert quick_sort(["ccc", "a", "bb"], key=len) == ["a", "bb", "ccc"]
```

## Тесты

```bash
pip install -r requirements-dev.txt
pytest -v
```

Структуры в тестах сверяются со встроенными `list`, `collections.deque` и `set`,
а после каждой операции с АВЛ-деревом проверяются его инварианты (допустимый
бинарный поиск, баланс, корректность высот).

CI (GitHub Actions) прогоняет тесты на Python 3.10–3.13 при каждом push и pull request.
