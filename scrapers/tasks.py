import subprocess

from typing import Any, Union

from celery import Celery
from celery.schedules import crontab

# from scrapers.run_spiders import run_spiders


app = Celery("tasks")

app.config_from_object("celeryconfig")


@app.task(name="tasks.run_spiders")
def run_spiders(query: Union[str, None]=None) -> None:
    # run_spiders()
    for spider in ['matras', 'bonito', 'tantis']:
        subprocess.run(["scrapy", "runspider", f"scrapers/spiders/{spider}.py", "-a", f"query={query}"])


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs: Any) -> None:
    sender.add_periodic_task(
        # crontab(hour=0, minute=0),
        crontab(minute=43),
        run_spiders.s(),
        name="run all spiders every night at 12 PM",
    )
