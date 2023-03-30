"""Rail Review!

CSC111 Winter 2023 Course Project

TODO: file description
"""
from __future__ import annotations
from math import sqrt
import math
import json
import matplotlib.pyplot as plt


class _Station:
    """A train station in a transit system.

    Instance Attributes:
      - name: the name of the train station
      - neighbours: a dict of the stations one stop away from self, mapping 
        station name to the Euclidean distance from the station to self
      - x: the x-position of the train station on a Euclidean plane
      - y: the y-position of the train station on a Euclidean plane

    Representation Invariants:
      - name != ''
    """
    name: str
    neighbours: dict[str, float]
    x: float
    y: float

    def __init__(self, name: str, x: float, y: float) -> None:
        """Initialize this _Station object.

        The object will have the given name and x- and y-coordinates.

        Preconditions:
          - name != ''

        Implementation notes:
          - self.neighbours is initialised as an empty dict, later mutated
            by TransitSystem methods to contain edges
        """
        self.name = name
        self.neighbours = {}
        self.x = x
        self.y = y

    def get_edge_length_to(self, other_station: _Station) -> float:
        """Return the length of the edge from self to other_station.

        Preconditions:
          - self and other_station in same transit system
          - self.name != other_station.name
          - self.name in other_station.neighbours
          - other_station.name in self.neighbours
        """
        x_diff = other_station.x - self.x  # Calculate delta x
        y_diff = other_station.y - self.y  # Calculate delta y

        # Compute and return Euclidean distance between stations
        return sqrt(x_diff**2 + y_diff**2)

    def get_total_edge_length(self, visited: set[str]) -> float:
        """Get total edge length of the graph this station is part of WITHOUT 
        including edges that connect to stations (whose names are) in visited.

        Preconditions:
          - self.name not in visited
          - all neighbouring stations are in the same transit system as self

        Implementation notes:
          - initially call to this method made by 
            get_total_edge_length TransitSystem method
          - TODO: Stephen
        """
        # Add self to set of visited stations
        visited.add(self.name)

        # Initialize edge length accumulator
        edge_len_so_far = 0.0

        for u in self.neighbours:
            if u not in visited:
                edge_length_so_far += self.get_edge_length_to(u)
                edge_len_so_far += u.get_total_edge_length(visited)

        return edge_len_so_far


class TransitSystem:
    """Description... it's just a normal graph bro

    Instance Attributes:
      - name: the name of the transit system's city

    Representation Invariants:
      - self is a connected graph
    """
    name: str
    # Private Instance Attributes:
    #     - _stations:
    #         A collection of the stations contained in this graph.
    #         Maps station name to _Station object.
    _stations: dict[str, _Station]

    def __init__(self, name: str) -> None:
        """..."""
        self.name = name
        self._stations = {}
        self._station_to_name = {}

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

    def load_from_json(self, file_path: str) -> None:
        """Load TransitSystem object from file_path.

        Implementation notes:
          - Open file without using with-block to reduce number of nested indentations
        """
        f = open(file_path, "r")
        dataset = json.load(f)
        for line_stations in dataset.values():
            station_iter = iter(line_stations.keys())
            prev_station_name = next(station_iter)
            station_obj = _Station(
                name=prev_station_name,
                x=line_stations[prev_station_name]["x"],
                y=line_stations[prev_station_name]["y"]
            )
            # will not raise error if station_obj already in transit system
            self.add_station(station_obj)

            for station_name in station_iter:
                station_obj = _Station(
                    name=station_name,
                    x=line_stations[station_name]["x"],
                    y=line_stations[station_name]["y"]
                )
                self.add_station(station_obj)  # no ValueError (see above)
                self.add_edge(station_name, prev_station_name)
                prev_station_name = station_name
        f.close()
        self._station_to_name = {val: key for val, key in self._stations.items()}

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

    def get_path_length(self, path: list[str]) -> float:
        """Return the length of the path formed by the stations in <path> 
        using Euclidean distance.
        """
        # Initialize path length accumulator
        path_length_so_far = 0.0

        # Iterate for each edge (pair of stations) in <path>
        for station1, station2 in zip(path[:-1], path[1:]):
            path_length_so_far += self.get_edge_length(station1, station2)

        return path_length_so_far

    def find_shortest_path(self, start_station: str, dest_station: str) -> list[_Station]:
        """Return the shortest path connecting station1 and station2 in the graph.

        Preconditions:
          - station1 in self._stations
          - station2 in self._stations

        Implementation notes:
          - TODO: Ricky
          - Use Dijkstra's algorithm
        """
        shortest_dist = {}
        visited_stations = {}
        unvisited_stations = self._stations
        path = []
        curr_station = self._stations[start_station]

        for station in unvisited_stations:
            shortest_dist[station] = math.inf

        shortest_dist[self._stations[start_station]] = 0

        while unvisited_stations:
            min_distance_station = None

            for station in unvisited_stations:
                if min_distance_station is None:
                    min_distance_station = station
                elif shortest_dist[station] < shortest_dist[min_distance_station]:
                    min_distance_station = station

            possible_paths = self._stations[min_distance_station].neighbours
            for neighbour in possible_paths:
                if curr_station.neighbours[neighbour] + shortest_dist[min_distance_station] < shortest_dist[neighbour]:
                    shortest_dist[neighbour] = curr_station.neighbours[neighbour] + shortest_dist[min_distance_station]
                    visited_stations[neighbour] = min_distance_station

            unvisited_stations.pop(min_distance_station)

        current_station = self._stations[dest_station]
        while current_station != self._stations[start_station]:
            path.insert(0, current_station)
            current_station = visited_stations[current_station]

        if shortest_dist[dest_station] != math.inf:
            return path

    def get_total_edge_length(self) -> float:
        """Return the total edge length of this graph.

        Implementation notes:
          - call private _Station method of same name
          - begin recursive process with first station in self._stations
        """
        starting_station = self._stations.values()[0]
        return starting_station.get_total_edge_length(set())

    def temporary_render(self,
                         name_size: int = 4,
                         figsize: tuple[int, int] = (20, 10),
                         show_name: bool = True) -> None:
        """Temporary rendering method until Zain makes the real one.

        Preconditions:
          - everything is calm
        """
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_title(self.name, size=40)
        for station_name in self._stations:
            stat = self._stations[station_name]
            ax.scatter(stat.x, stat.y, c="black")
            if show_name:
                ax.annotate(stat.name, (stat.x, stat.y),
                            size=name_size, c="black")
            for n_stat_name in self._stations[station_name].neighbours:
                n_stat = self._stations[n_stat_name]
                ax.plot((stat.x, n_stat.x), (stat.y, n_stat.y), c="black")
                x_pos = stat.x - (stat.x - n_stat.x) / 2
                y_pos = stat.y - (stat.y - n_stat.y) / 2
                dist = round(stat.neighbours[n_stat_name], 3)
                ax.annotate(str(dist), (x_pos, y_pos),
                            size=name_size + 3, c="black")
        plt.show()


# NOTE: We should really run tests on all this stuff
# NOTE: im bein' sewious guys
