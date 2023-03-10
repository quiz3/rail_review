from graph import TransitSystem, _Station

singapore = TransitSystem()
singapore.load_from_json("dataset/dataset/singapore.json")
singapore.temporary_render(show_name=True)

