from celery import Celery

app = Celery("celery")

app.config_from_object("celeryconfig")
