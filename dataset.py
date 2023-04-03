"""CSC111 Winter 2023 Course Project - Rail Review!

This file contains the 'Dataset' class, which is used by other files in our project.
"""
import json


class Dataset:
    """Class representing a data set (which stores transit-related data).

    Representation Invariants:
      - loaded: dataset in dictionary form
      - file_path: location data set is loaded from
      - name: the name of the dataset
      - x_vals: list containing x-values of stations in the data set
      - y_vals: list containing y-values of stations in the data set
    """
    loaded: dict
    file_path: str
    name: str
    x_vals: list[float]
    y_vals: list[float]

    def __init__(self, file_path: str = './dataset/dataset/toronto.json') -> None:
        self.load_dataset(file_path)

    def get_loaded(self) -> dict:
        """Return loaded dataset (in dictionary form)."""
        return self.loaded

    def load_dataset(self, file_path: str) -> None:
        """Load the dataset stored at <file_path>."""
        train_dataset = file_path
        with open(train_dataset, "r") as file_obj:
            self.loaded = json.load(file_obj)
        self.file_path = file_path

        self.x_vals = [self.loaded[a][b]['x'] for a in self.loaded for b in self.loaded[a]]
        self.y_vals = [self.loaded[a][b]['y'] for a in self.loaded for b in self.loaded[a]]


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['json'],
        'allowed-io': ['Dataset.load_dataset']
    })
