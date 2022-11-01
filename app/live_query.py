import os

from time import sleep
from typing import List

from celery import Celery
from celery.result import AsyncResult 

from app.db_handler import DBHandler

TIMEOUT_LIMIT = 20
RESULT_CHECK_INTERVAL = 1

db = DBHandler()
celery_app = Celery()
celery_app.config_from_object('app.celeryconfig')


async def request_live_query(query: str) -> List[dict]:
    # add a task to redis with celery
    task: AsyncResult = celery_app.send_task("tasks.run_spiders")
    # check the status of the task 
    num_checks: int = 0
    while num_checks < (TIMEOUT_LIMIT):
        if task.ready():
            results: List[dict] = await db.get_offers(query)
            return results
        sleep(RESULT_CHECK_INTERVAL)
    return []

    
