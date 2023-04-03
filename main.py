"""TODO: ...
"""
from interface import interface_runner
from graph import TransitSystem


def run_quick_demo_test():
    """This is only a demo for two cities, some of the others take much longer to run since they have more stations.
    The interface is run from assets/cached_transit_stats.json, which stores the precomputed transit scores
    to save time.
    """
    for city in ["Toronto", "Singapore"]:
        test_city = TransitSystem(city)
        test_city.load_from_json(f"datasets/dataset/{city.lower()}.json")
        # test_city.temporary_render(name_size=10, show_name=True)
        # shortest_path = test_city.find_shortest_path("Downsview", "Wilson")
        print("-" * 10 + f" {city} " + "-" * 10)
        test_city.compute_transit_system_score()
        print(f"Total number of stations: {len(test_city.get_stations())}")
        # test_city.compute_transit_system_score()
        print(f"Total number of paths: {test_city.transit_info_dict['total_paths']}")
        print(f"Total distance: {test_city.transit_info_dict['total_distance']}")
        print(f"Total edge length: {test_city.transit_info_dict['total_edge_length']}")
        print(f"Transit system score: {round(test_city.transit_info_dict['transit_score'] * 100, 3)}")


if __name__ == "__main__":
    # run_quick_demo_test()
    interface_runner()

    # Run python-TA checks
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['interface', 'graph'],
        'allowed-io': []
    })
