import pandas as pd
import logging

from fake_data_lake import FakeDataLake
from feature_store import FeatureStore
from features.base_feature import BaseFeature

logger = logging.getLogger(__name__)


class Backfill:
    def __init__(self, daily: bool, source: FakeDataLake, frame_features: list[BaseFeature],
                 org_features: list[BaseFeature], storage: FeatureStore):
        self.daily = daily
        self.source = source
        self.frame_features = frame_features
        self.org_features = org_features
        self.storage = storage

    def run(self) -> None:
        # load the data
        dfs = self.source.latest() if self.daily else self.source.all()

        # calculate frame features
        for feature in self.frame_features:
            feature.calculate(dfs)

        # calculate organization scope features
        df = pd.concat(dfs, ignore_index=True, sort=False)
        df.set_index(['location', 'date'], inplace=True, drop=False)

        for feature in self.org_features:
            feature.calculate([df])

        # save to storage
        if not len(df) == 0:
            self.storage.init_schema(df, ['location', 'date'])
            self.storage.save(df)
        else:
            logger.info('nothing to store')
