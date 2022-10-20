from celery import Celery
from celery.schedules import crontab

from run_spiders import run_spiders


app = Celery("tasks")

app.config_from_object("celeryconfig")




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
