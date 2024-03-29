"""CSC111 Winter 2023 Course Project - Rail Review!

- This file contains an implementation of the graph ADT representing a transit system.
- This file contains the _Station and TransitSystem classes, which correspond to the _Node and Graph ADTs we have looked
  at during this course.
"""
from __future__ import annotations
from typing import Optional
import math
import json
import matplotlib.pyplot as plt
from tqdm import tqdm


class _Station:
    """A train station in a transit system.

    This class represents a node of a graph represented by the TransitSystem object.

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
          - self.neighbours is initialized as an empty dict, later mutated
            by TransitSystem methods to contain edges
        """
        self.name = name
        self.neighbours = {}
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        """Return the hash of this station object.
        """
        return hash(self.name)

    def __eq__(self, other_station: _Station) -> bool:
        """Define equality comparison of this object with another _Station object.
        """
        return self.__class__ == other_station.__class__ and self.name == other_station.name

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
        return math.sqrt(x_diff**2 + y_diff**2)

    def get_total_edge_length(self, visited: set[str], station_dict: dict[str, _Station]) -> float:
        """Get total edge length of the graph this station is part of WITHOUT
        including edges that connect to stations (whose names are) in visited.

        Preconditions:
          - self.name not in visited
          - all neighbouring stations are in the same transit system as self

        Implementation notes:
          - initially call to this method made by
            get_total_edge_length TransitSystem method
        """
        # Add self to set of visited stations
        visited.add(self.name)

        # Initialize edge length accumulator
        edge_len_so_far = 0.0

        for u in self.neighbours:
            if u not in visited:
                edge_len_so_far += self.get_edge_length_to(station_dict[u])
                edge_len_so_far += station_dict[u].get_total_edge_length(visited, station_dict)

        return edge_len_so_far


class TransitSystem:
    """An implementation of the graph ADT whose nodes are train stations.
    This represents a network of train stations and the tracks connecting them.
    The train stations are represented by the _Station class.

    Instance Attributes:
      - name: the name of the transit system's city
      - transit_info_dict: mapping containing various pieces of information about the transit system object

    Representation Invariants:
      - self is a connected graph
      - every station name is unique
    """
    name: str
    transit_info_dict: dict
    # Private Instance Attributes:
    #   - _stations:
    #       A collection of the stations contained in this graph.
    #       Maps station name to _Station object.
    _stations: dict[str, _Station]

    def __init__(self, name: str) -> None:
        """Initialize object representing a transit system."""
        self.name = name
        self._stations = {}
        self.transit_info_dict = {}

    def __contains__(self, station: str | _Station) -> bool:
        """Return whether station is in self.

        Implementation notes:
          - if station is a str object, return whether station is in self._stations
          - if station is a _Station object, return whether station.name is in self._stations
        """
        if isinstance(station, _Station):  # <station> is a _Station object
            return station.name in self._stations
        else:  # <station> is a str object
            return station in self._stations

    def load_from_json(self, file_path: str) -> None:
        """Load TransitSystem object from json data set at <file_path>.
        """
        with open(file_path, "r") as f:
            dataset = json.load(f)

            for line_stations in dataset.values():
                station_iter = iter(line_stations.keys())
                prev_station_name = next(station_iter)
                station_obj = _Station(
                    name=prev_station_name,
                    x=line_stations[prev_station_name]["x"],
                    y=line_stations[prev_station_name]["y"]
                )
                # NOTE: will not raise error when station_obj already in transit system
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

    def get_stations(self) -> dict[str, _Station]:
        """Return the private instance attribute self._stations.
        NOTE: required because the mapping self._stations could not otherwise be accessed outside of this class.
        """
        return self._stations

    def get_station_by_name(self, station_name: str) -> Optional[_Station]:
        """Return station (value) corresponding to key <station_name> in self._stations.
        This method is defined as a way of accessing _Station objects stored in a private instance attribute by name.

        Implementation notes:
          - return None when station_name not in self._stations (do NOT raise error)
        """
        # Alternate condition: station_name not in self (thanks to __contains__ method)
        if station_name not in self._stations:
            return None

        return self._stations[station_name]

    def system_to_dict(self) -> dict[str, dict[str, float]]:
        """Convert TransitSystem object into dictionary useable by Dijkstra's algorithm.
        """
        # Initialize accumulator dictionary
        system_dict = {}

        # Add information for each station to system_dict in required form for Dijkstra's algorithm
        for station in self._stations.values():
            # station.neighbours already formatted as required
            system_dict[station.name] = station.neighbours

        return system_dict

    def add_station(self, station: _Station) -> None:
        """Add _Station object <station> to this graph.

        Implementation notes:
          - do NOT raise an error when called on a station that is already in self
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

    def get_edge_length(self, station1: str | _Station, station2: str | _Station) -> float:
        """Return the length of the edge connecting station1 and station2 in this graph.

        Preconditions:
          - station1 in self
          - station2 in self
          - station1 != station2
          - station1 and station2 are adjacent
        """
        if isinstance(station1, str):
            station1 = self._stations[station1]  # get _Station object for station1
        if isinstance(station2, str):
            station2 = self._stations[station2]  # get _Station object for station2

        x_diff = station2.x - station1.x  # Calculate delta x
        y_diff = station2.y - station1.y  # Calculate delta y

        # Compute and return Euclidean distance
        return math.sqrt(x_diff ** 2 + y_diff ** 2)

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

    def find_shortest_path(self, start_station: str, dest_station: str) -> tuple[list[str], float]:
        """Return a tuple containing the shortest path connecting station1 and station2 in the graph
        and the length of this path (in Euclidean distance).

        Preconditions:
          - start_station in self._stations
          - dest_station in self._stations

        Implementation notes:
          - Use Dijkstra's algorithm
          - Return list of strings
        """
        shortest_distance = {}
        track_prev_station = {}
        unvisited_stations = self.system_to_dict()
        path = []
        total_path_distance = 0.0

        for station in unvisited_stations:
            shortest_distance[station] = math.inf
        shortest_distance[start_station] = 0.0

        while unvisited_stations:
            min_distance_station = None

            for station in unvisited_stations:
                if min_distance_station is None:
                    min_distance_station = station
                elif shortest_distance[station] < shortest_distance[min_distance_station]:
                    min_distance_station = station

            possible_paths = self.system_to_dict()[min_distance_station].items()

            for neighbour, dist in possible_paths:
                if dist + shortest_distance[min_distance_station] < shortest_distance[neighbour]:
                    shortest_distance[neighbour] = dist + shortest_distance[min_distance_station]
                    track_prev_station[neighbour] = min_distance_station

            unvisited_stations.pop(min_distance_station)

        curr_station = dest_station

        while curr_station != start_station:
            path.append(curr_station)
            total_path_distance += self.get_edge_length(curr_station, track_prev_station[curr_station])
            curr_station = track_prev_station[curr_station]

        path.append(start_station)
        path.reverse()

        return path, total_path_distance

    def get_total_edge_length(self) -> float:
        """Return the total edge length of this graph.

        Implementation notes:
          - call private _Station method of same name
          - begin recursive process with first station in self._stations
        """
        starting_station = list(self._stations.values())[0]  # extract first station in transit system
        return starting_station.get_total_edge_length(set(), self._stations)  # call recursive _Station method

    def compute_transit_system_score(self) -> None:
        """Computes an objective score to rank this transit system.
        This method returns None and the computed score is stored in self.transit_score.
        """
        total_distance = 0
        total_paths = int(len(self._stations) * (len(self._stations) - 1) / 2)
        computed_pairs = []
        loop = tqdm(enumerate(self._stations), total=len(self._stations),
                    leave=False, position=0, bar_format='{l_bar}{bar:20}{r_bar}{bar:-20b}')

        for _, source_station_name in loop:
            for target_station_name in self._stations:
                already_checked = ((source_station_name, target_station_name) in computed_pairs) or \
                                  ((target_station_name, source_station_name) in computed_pairs)
                if target_station_name != source_station_name and not already_checked:
                    _, dist = self.find_shortest_path(source_station_name, target_station_name)
                    total_distance += dist
                    computed_pairs.append((source_station_name, target_station_name))
        total_edge_length = self.get_total_edge_length()

        self.transit_info_dict["total_num_stations"] = len(self._stations)
        self.transit_info_dict["total_paths"] = total_paths
        self.transit_info_dict["total_distance"] = total_distance
        self.transit_info_dict["total_edge_length"] = total_edge_length
        self.transit_info_dict["transit_score"] = total_distance / total_paths / total_edge_length

    def load_from_cache_dict(self, cache_file_name: str = 'cached_transit_stats.json') -> None:
        """Update transit_info_dict attribute by loading data from <cache_file_name>.
        """
        with open(cache_file_name, "r") as f:
            json_object = json.load(f)
            for d in json_object:
                if self.name == str.lower(d["city"]):
                    self.transit_info_dict = d
                    break

    def temporary_render(self, name_size: int = 4, figsize: tuple[int, int] = (20, 10), show_name: bool = True) -> None:
        """This is a rendering method for debugging purposes.
        """
        _, ax = plt.subplots(figsize=figsize)  # NOTE: '_' here usually written as 'fig'
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


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['typing', 'math', 'json', 'matplotlib.pyplot', 'tqdm'],
        'allowed-io': ['TransitSystem.load_from_json', 'TransitSystem.load_from_cache_dict']
    })
