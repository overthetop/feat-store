import logging
import math

import pandas as pd
import psycopg
from psycopg_pool import ConnectionPool

from settings import Settings
from settings import settings

logger = logging.getLogger(__name__)


class FeatureStore:
    def __init__(self, data: Settings):
        self.tbl = 'feat_tbl'
        self.user = data.database_username
        self.password = data.database_password
        self.host = data.database_hostname
        self.port = data.database_port
        self.database = data.database_name
        self.pool = ConnectionPool(
            psycopg.conninfo.make_conninfo('',
                                           host=data.database_hostname,
                                           port=data.database_port,
                                           dbname=data.database_name,
                                           user=data.database_username,
                                           password=data.database_password))

    def open(self):
        self.pool.open()

    def close(self):
        self.pool.close()

    def get_by_location(self, location: int):
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT * FROM {self.tbl} WHERE location = %s;", [location])
                return [x for x in cur]

    def check_schema(self):
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT EXISTS ( SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename  = '{self.tbl}');")
                return [{'initialized': x[0]} for x in cur]

    def get_schema(self):
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT column_name, data_type, is_nullable from INFORMATION_SCHEMA.COLUMNS where table_name = '{self.tbl}';")
                return [{'column': x[0], 'data_type': x[1], 'is_nullable': x[2]} for x in cur]

    def drop_schema(self) -> None:
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                drop = f"DROP TABLE IF EXISTS public.{self.tbl};"
                cur.execute(drop)

    def init_schema(self, df: pd.DataFrame, index: list[str]) -> None:
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                # drop first
                drop = f"DROP TABLE IF EXISTS public.{self.tbl};"
                cur.execute(drop)

                # create new
                query = f"CREATE TABLE IF NOT EXISTS public.{self.tbl} ("

                for col in df.columns:
                    if pd.api.types.is_datetime64_any_dtype(df.dtypes[col]):
                        query += f"{col} DATE, "
                    elif pd.api.types.is_float_dtype(df.dtypes[col]):
                        query += f"{col} NUMERIC, "
                    elif pd.api.types.is_integer_dtype(df.dtypes[col]):
                        query += f"{col} INTEGER, "
                    elif pd.api.types.is_bool_dtype(df.dtypes[col]):
                        query += f"{col} BOOLEAN, "

                query += 'PRIMARY KEY (' + ', '.join(index) + ')'
                query += ');'

                cur.execute(query)

    def save(self, df: pd.DataFrame, split_by: str = None) -> None:
        if split_by is not None:
            grouped = df.groupby([split_by])
            for name in grouped.groups:
                d = grouped.get_group(name)
                d.reset_index(drop=True)
                self.append(d)
        else:
            self.append(df)

    def append(self, df: pd.DataFrame) -> None:
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cols_clause = ', '.join(list(df.columns))
                tuples = list(set([tuple(x) for x in df.to_numpy()]))

                if len(tuples) == 0:
                    # nothing to insert
                    return

                values = []
                for t in tuples:
                    row = '('
                    for item in t:
                        if pd.api.types.is_bool(item):
                            row += str(item) + ', '
                        elif pd.api.types.is_float(item) or pd.api.types.is_integer(item):
                            if math.isnan(item):
                                row += 'NULL' + ', '
                            else:
                                row += str(item) + ', '
                        elif pd.api.types.is_string_dtype(item) or pd.api.types.is_datetime64_any_dtype(
                                item) or isinstance(item, pd.Timestamp):
                            row += "'" + str(item) + "', "
                        else:
                            logger.info('unknown type')
                    row = row[:-2]
                    row += ')'
                    values.append(row)

                values_clause = ','.join(values)
                query = f"INSERT INTO {self.tbl} ({cols_clause}) VALUES {values_clause};"
                cur.execute(query)


store_instance = FeatureStore(settings)
