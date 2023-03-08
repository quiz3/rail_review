"""CSC111 Title....

description
"""
from __future__ import annotations
from typing import Optional, Any


class _Station:
    """Description...
    """
    name: str
    neighbours: set[_Station]
    lat: float
    lon: float

    def __init__(self) -> None:
        """..."""
        ...


class TransitSystem:
    """Description... it's like a graph
    """
    _stations: dict[str, _Station]

    def __init__(self) -> None:
        """..."""
        pass

    def load_from_csv(self, file_path: str) -> None:
        """..."""
        pass

    def add_station(self, station: _Station) -> None:
        """..."""
        pass

    def add_edge(self, station1: str, station2: str) -> None:
        """...

        Preconditions:
          - station1 in self._stations
          - station2 in self._stations
        """
        pass

    def get_path_length(self, path: list[_Station]) -> float:
        """Return the length of the path formed by the stations in <path>
        using Euclidean distance.
        """
        pass

    def find_shortest_path(self, station1: str, station2: str) -> list[_Station]:
        """Return the shortest path connecting station1 and station2 in the graph.

        Preconditions:
          - station1 in self._stations
          - station2 in self._stations
        """
        pass

    def get_total_edge_length(self) -> float:
        """..."""
        pass
