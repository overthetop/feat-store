import logging
import time
import uuid
from logging import config

from fastapi import FastAPI, Response, Request

import constants
from backfill import Backfill
from fake_data_lake import FakeDataLake
from feature_store import store_instance

config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = uuid.uuid4()
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    return response


@app.on_event("startup")
def startup():
    store_instance.open()


@app.on_event("shutdown")
def close_pool():
    store_instance.close()


@app.get("/api/schema")
def schema():
    return store_instance.get_schema()


@app.delete("/api/schema", status_code=200, response_class=Response)
def schema():
    return store_instance.drop_schema()


@app.get("/api/schema/check")
def check_schema():
    return store_instance.check_schema()


@app.get("/api/features/{location}")
def features(location: int):
    return store_instance.get_by_location(location)


@app.post("/api/backfill/{daily}", status_code=200, response_class=Response)
def backfill(daily: bool):
    source = FakeDataLake(constants.TEST_DATA_FILE_PATH)
    backfill_job = Backfill(daily, source, constants.FRAME_FEATURES, constants.ORG_FEATURES, store_instance)
    backfill_job.run()
