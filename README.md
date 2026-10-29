# data-structures-lab

Структуры данных и сортировки на Python (TDD: сначала тесты, потом код).

| Модуль | Что внутри |
|---|---|
| `ds/dynamic_array.py` | Динамический массив `DynamicArray`: доступ по индексу, рост и сжатие буфера |
| `ds/linked_list.py` | Односвязный список `LinkedList` |
| `ds/deque.py` | Дек `Deque` на кольцевом буфере |
| `ds/avl_tree.py` | АВЛ-дерево `AVLTree`: вставка, удаление, поиск, обход |
| `ds/sorting.py` | Сортировки `bubble_sort` и `quick_sort` (поддерживают `key` и `reverse`) |

## Тесты

```bash
pip install pytest
pytest -v
```

Структуры в тестах сверяются со встроенными `list`, `collections.deque` и `set`,
а после каждой операции с АВЛ-деревом проверяются его инварианты.

CI (GitHub Actions) прогоняет тесты на Python 3.10–3.13 при каждом push и pull request.
