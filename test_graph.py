from graph import TransitSystem

# Choose city for which to generate map
TEST_CITY = 'Toronto'

# Show map for the TEST_CITY
test_city = TransitSystem(TEST_CITY)
test_city.load_from_json(f"dataset/dataset/{TEST_CITY.lower()}.json")
test_city.temporary_render(name_size = 10, show_name=True)
shortest_path = test_city.find_shortest_path("Downsview", "Yorkdale")
print(shortest_path)

