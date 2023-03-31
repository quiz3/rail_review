from graph import TransitSystem

# Choose city for which to generate map


for city in ["Toronto", "Tokyo", "Singapore", "Seoul", "Delhi"]:
    test_city = TransitSystem(city)
    test_city.load_from_json(f"dataset/dataset/{city.lower()}.json")
    # test_city.temporary_render(name_size=10, show_name=True)
    # shortest_path = test_city.find_shortest_path("Downsview", "Wilson")
    test_city.load_from_cache_dict("cached_transit_stats.json")
    print("-" * 10 + f" {city} " + "-" * 10)
    print(f"Total number of stations: {len(test_city._stations)}")
    # test_city.compute_transit_system_score()
    print(f"Total number of paths: {test_city.transit_info_dict['total_paths']}")
    print(f"Total distance: {test_city.transit_info_dict['total_distance']}")
    print(f"Total edge length: {test_city.transit_info_dict['total_edge_length']}")
    print(f"Transit system score: {round(test_city.transit_info_dict['transit_score'] * 100, 3)}")
