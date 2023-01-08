from datetime import datetime

import pandas as pd

from features.base_feature import BaseFeature


class IsToday(BaseFeature):
    def __init__(self, name):
        super().__init__(name)

    def calculate(self, dfs: list[pd.DataFrame]) -> None:
        today_date = datetime.today().date()
        for df in dfs:
            df['is_today'] = pd.to_datetime(df['date']).dt.date == today_date
