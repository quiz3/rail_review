"""CSC111 Title....

description
"""
from __future__ import annotations
from math import sqrt
# from typing import Optional, Any


class _Station:
    """A train station in a transit system.

    Instance Attributes:
      - name: the name of the train station
      - neighbours: a dict of the stations one stop away from self, mapping 
        the station name to the Euclidean distance from the station to self
      - x: the x-position of the train station on a Euclidean plane
      - y: the y-position of the train station on a Euclidean plane

    Representation Invariants:
      - name != ''
    """
    name: str
    # neighbours: set[_Station]  # old neighbours attribute
    neighbours: dict[str, float]
    x: float
    y: float

    def __init__(self, name: str, x: float, y: float) -> None:
        """..."""
        self.name = name
        self.neighbours = set()
        self.x = x
        self.y = y


class TransitSystem:
    """Description... it's like a graph
    """
    _stations: dict[str, _Station]
    # nested dict is name of neighbouring stations with values being distance to those
    # _new_dict: dict[str, dict[str, float]]

    def __init__(self) -> None:
        """..."""
        self._stations = {}

    def __contains__(self, station: str | _Station) -> bool:
        """Return whether station is in self.

        Implementation notes:
          - if station is a str object, return whether station is in self._stations
          - if station is a _Station object, return whether station.name is in self._stations
        """
        if isinstance(station, _Station):
            return station.name in self._stations
        else:  # station is a str object
            return station in self._stations

    def load_from_csv(self, file_path: str) -> None:
        """Load TransitSystem object from file_path.

        Implementation notes:
          - TODO: Gursi
        """
        pass

    def add_station(self, station: _Station) -> None:
        """Add _Station object <station> to this graph.

        Implementation notes:
          - do not raise an error when called on a station that is already in self
        """
        if station in self:
            pass
        else:
            self._stations[station.name] = station  # add station to self

    def add_edge(self, station1: str, station2: str) -> None:
        """Add an edge joining station1 and station2 in this graph.

        Preconditions:
          - station1 in self._stations
          - station2 in self._stations

        Implementation notes:
          - it's fine if an edge already exists between the stations
        """
        # Get _Station objects
        s1 = self._stations[station1]
        s2 = self._stations[station2]

        # Compute edge length
        edge_length = self.get_edge_length(station1, station2)

        # Add the edge
        s1.neighbours[station2] = edge_length
        s2.neighbours[station1] = edge_length

    def get_edge_length(self, station1: str, station2: str) -> float:
        """Return the length of the edge connecting station1 and station2 in this graph.

        Preconditions:
          - station1 in self
          - station2 in self
          - station1 != station2
          - station1 in self._stations[station2].neighbours
          - station2 in self._stations[station1].neighbours
        """
        s1 = self._stations[station1]  # get _Station object for station1
        s2 = self._stations[station2]  # get _Station object for station2

        x_diff = s2.x - s1.x  # Calculate delta x
        y_diff = s2.y - s1.y  # Calculate delta y

        # Compute and return Euclidean distance
        return sqrt(x_diff**2 + y_diff**2)

    def get_path_length(self, path: list[_Station]) -> float:
        """Return the length of the path formed by the stations in <path>
        using Euclidean distance.
        """
        # Initialize path length accumulator
        path_length_so_far = 0.0

        # Iterate for each edge (pair of stations) in <path>
        for station1, station2 in zip(path[:-1], path[1:]):
            path_length_so_far += self.get_edge_length(
                station1.name, station2.name)

        return path_length_so_far

    def find_shortest_path(self, station1: str, station2: str) -> list[_Station]:
        """Return the shortest path connecting station1 and station2 in the graph.

        Preconditions:
          - station1 in self._stations
          - station2 in self._stations

        Implementation notes:
          - TODO: Ricky
        """
        pass

    def get_total_edge_length(self) -> float:
        """Return the total edge length of this graph.

        Implementation notes:
          - TODO: Stephen
        """
        pass
