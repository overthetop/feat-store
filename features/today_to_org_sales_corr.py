import pandas as pd

from features.base_feature import BaseFeature


class TodayToOrgSalesCorr(BaseFeature):
    def __init__(self, name):
        super().__init__(name)

    def calculate(self, dfs: list[pd.DataFrame]) -> None:
        for df in dfs:
            df[self.name] = df['today_sales'].corr(df['prev_7_days'])
