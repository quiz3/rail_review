from graph import TransitSystem

# Choose city for which to generate map
TEST_CITY = 'Seoul'

# Show map for the TEST_CITY
test_city = TransitSystem(TEST_CITY)
test_city.load_from_json(f"dataset/dataset/{TEST_CITY.lower()}.json")
test_city.temporary_render(show_name=True)
