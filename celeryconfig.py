import os

broker_url = os.getenv("BROKER_URL")
result_backend = os.getenv("MONGODB_URL")
mongodb_backend_settings = {
    "database": "celery",
    "taskmeta_collection": "celery-tasks",
}
timezone = "Europe/Warsaw"
enable_utc = True
imports = ("scrapers.tasks",)
