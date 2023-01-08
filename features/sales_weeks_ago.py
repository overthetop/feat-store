import pandas as pd

from features.base_feature import BaseFeature


class SalesWeeksAgo(BaseFeature):
    def __init__(self, name: str, weeks_ago: int):
        super().__init__(name)
        self.weeks_ago = weeks_ago

    def calculate(self, dfs: list[pd.DataFrame]) -> None:
        for df in dfs:
            df[self.name] = df['sales'].shift(7 * self.weeks_ago, freq='D')
