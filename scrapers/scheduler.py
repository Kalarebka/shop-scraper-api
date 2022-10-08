# under construction

import os

from celery.app.base import Celery
from celery.schedules import crontab

from scrapers.run_spiders import run_spiders

app = Celery('scheduler', broker=os.getenv('BROKER_URL'))

@app.task
def scheduled_run_spiders() -> None:
    run_spiders()

app.conf.beat_schedule = {
    "scraper_task": {
        "task": "scheduler.scheduled_run_spiders",
        "schedule": crontab(minute=0, hour=0)
    }
}
