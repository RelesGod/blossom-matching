"""
Алгоритм Эдмондса–Габбова для максимального паросочетания в невзвешенном графе.
Сложность O(n^3). Использует неявное сжатие цветков через массив base.
"""
from collections import deque


def max_matching_edmonds(graph):
    n = len(graph)
    mate = [-1] * n         # партнёр в паросочетании
    parent = [-1] * n       # предок в чередующемся лесу
    base = list(range(n))   # база сжатого цветка
    q = deque()             # очередь для BFS

    def lca(u, v):
        """Наименьший общий предок для двух вершин в лесу."""
        used = [False] * n
        while True:
            u = base[u]
            used[u] = True
            if mate[u] == -1:
                break
            u = parent[mate[u]]
        while True:
            v = base[v]
            if used[v]:
                return v
            v = parent[mate[v]]

    def mark_path(v, b, child, blossom):
        """Помечает путь от v до базы b как часть цветка."""
        while base[v] != b:
            blossom[base[v]] = blossom[base[mate[v]]] = True
            parent[v] = child
            child = mate[v]
            v = parent[mate[v]]

    def find_path(root):
        """Ищет увеличивающий путь из свободной вершины root."""
        nonlocal q, parent
        used = [False] * n
        for i in range(n):
            base[i] = i
        q.clear()
        q.append(root)
        used[root] = True
        while q:
            v = q.popleft()
            for to in graph[v]:
                if base[v] == base[to] or mate[v] == to:
                    continue
                if to == root or (mate[to] != -1 and parent[mate[to]] != -1):
                    # Найден цветок
                    curbase = lca(v, to)
                    blossom = [False] * n
                    mark_path(v, curbase, to, blossom)
                    mark_path(to, curbase, v, blossom)
                    for i in range(n):
                        if blossom[base[i]]:
                            base[i] = curbase
                            if not used[i]:
                                used[i] = True
                                q.append(i)
                elif parent[to] == -1:
                    parent[to] = v
                    if mate[to] == -1:
                        # Найден увеличивающий путь
                        cur = to
                        while cur != -1:
                            prev = parent[cur]
                            nxt = mate[prev] if prev != -1 else -1
                            mate[cur] = prev
                            mate[prev] = cur
                            cur = nxt
                        return True
                    else:
                        used[mate[to]] = True
                        q.append(mate[to])
        return False


    for i in range(n):
        if mate[i] == -1:
            parent = [-1] * n
            find_path(i)

    # Формируем ответ
    matching = []
    for v in range(n):
        if v < mate[v]:
            matching.append((v, mate[v]))
    return matching