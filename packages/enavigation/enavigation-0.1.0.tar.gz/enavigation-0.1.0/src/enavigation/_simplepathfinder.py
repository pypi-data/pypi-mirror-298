from __future__ import annotations

__all__ = ["SimplePathFinder"]

# enavigation
from ._graph import Graph
from ._graph import Weighted

# sortedcontainers
from sortedcontainers import SortedList

# python
from typing import Generator
from typing import Generic
from typing import Hashable
from typing import TypeVar

M = TypeVar("M")
T = TypeVar("T", bound=Hashable)
W = TypeVar("W", bound=Weighted)


class SimplePathFinder(Generic[T, W]):
    def __init__(self, graph: Graph[T, W], start: T, end: T):
        self._graph = graph
        self._start_node = start
        self._end_node = end
        self._ignore_nodes: set[T] = set()
        self._iter = self._find()

    def __next__(self) -> tuple[T, ...]:
        return next(self._iter)

    def __iter__(self: M) -> M:
        return self

    def _find(self) -> Generator[tuple[T, ...], None, None]:
        if not self._graph.contains_node(self._start_node) or not self._graph.contains_node(
            self._end_node
        ):
            return
        # this is (roughly) dijkstra's algorithm
        sorted_weighted_paths = SortedList([((self._start_node,), 0)], key=lambda pw: -pw[1])
        while True:
            try:
                path, weight = sorted_weighted_paths.pop(-1)
            except IndexError:
                return
            visited_nodes = set(path)
            if len(visited_nodes - self._ignore_nodes) < len(path):
                continue
            last_node = path[-1]
            if last_node == self._end_node:
                yield path
            else:
                sorted_weighted_paths.update(
                    (
                        ((*path, next_node), weight + next_weight)
                        for next_node, next_weight in self._graph.get_node_edges(last_node)
                        if next_node not in visited_nodes
                    )
                )

    def ignore_node(self, node: T) -> None:
        self._ignore_nodes.add(node)
