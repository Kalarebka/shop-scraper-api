from datetime import timedelta

from celery.schedules import crontab

from scrapers.celery import app
from scrapers.run_spiders import run_spiders


@app.task()
def scheduled_run_spiders() -> None:
    run_spiders()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs) -> None:
    sender.add_periodic_task(
        # crontab(hour=0, minute=0),
        crontab(minute=43),
        scheduled_run_spiders.s(),
        name="run all spiders every night at 12 PM",
    )
