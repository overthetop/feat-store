import pandas as pd


class BaseFeature:
    def __init__(self, name: str):
        self.name = name

    def calculate(self, dfs: list[pd.DataFrame]) -> None:
        pass
