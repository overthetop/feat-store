import datetime
from datetime import timedelta

import pandas as pd


class FakeDataLake:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def all(self) -> list[pd.DataFrame]:
        df = pd.read_csv(self.file_path, parse_dates=['date'])
        grouped = df.groupby(['location'])
        chunks = []
        for name in grouped.groups:
            d = grouped.get_group(name)
            d.set_index('date', inplace=True, drop=False)
            chunks.append(d)

        return chunks

    def latest(self) -> list[pd.DataFrame]:
        # just for a demonstration we shrink the dataframe to contain only the last 365 days
        # so that SMA feature could be calculated for the passed 365 days
        chunks = self.all()
        shrank = []
        for chunk in chunks:
            to_dt = datetime.date.today()
            from_dt = to_dt - timedelta(days=365)
            df = chunk.loc[from_dt:to_dt]
            shrank.append(df)

        return shrank
