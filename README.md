# Edmonds' Blossom Algorithm

Реализация алгоритма Эдмондса–Габбова для поиска максимального паросочетания в произвольном графе на Python. Сложность O(n³).

## Использование
```python
graph = [[1], [0, 2], [1, 3, 4], [2, 4], [2, 3, 5], [5]]
matching = max_matching_edmonds(graph)
print(matching)  # [(0, 1), (2, 3), (4, 5)]
