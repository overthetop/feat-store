import pandas as pd

from features.base_feature import BaseFeature


class SMA(BaseFeature):
    def __init__(self, name, days: int):
        super().__init__(name)
        self.days = days

    def calculate(self, dfs: list[pd.DataFrame]) -> None:
        for df in dfs:
            df[self.name] = df['sales'].rolling(self.days).mean()
