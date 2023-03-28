import json

COLORS = [(0, 0, 0), (150, 150, 150), (180, 0, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0), (0, 180, 0)]


class dataset:
    loaded: dict
    file_path: str
    name: str
    cmap: dict
    x_vals: list[float]
    y_vals: list[float]

    def __init__(self, file_path='./dataset/dataset/toronto.json') -> None:
        self.load_dataset(file_path)

    def get_loaded(self):
        return self.loaded

    def load_dataset(self, file_path):
        train_dataset = file_path
        file_obj = open(train_dataset, "r")
        self.loaded = json.load(file_obj)
        self.file_path = file_path
        self.cmap = {line: c for line, c in zip(self.loaded, COLORS)}

        # TODO, x and y are not actual pos coords
        self.x_vals = [self.loaded[x][y]['x'] for x in self.loaded for y in self.loaded[x]]
        self.y_vals = [self.loaded[x][y]['y'] for x in self.loaded for y in self.loaded[x]]
