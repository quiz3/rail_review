from graph import TransitSystem, _Station

# Singapore test
singapore = TransitSystem()
singapore.load_from_json("dataset/dataset/singapore.json")
singapore.temporary_render(show_name=True)

# Toronto test
...
