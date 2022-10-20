from celery import Celery

app = Celery("scrapers")

app.config_from_object("scrapers.celeryconfig")
