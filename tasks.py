from celery import Celery
from celery.schedules import crontab
from webapp import create_app
from webapp.receipt.utils.receipt_handler import receipt_get_handler

celery_app = Celery('tasks', broker='redis://localhost:6379/1')

flask_app = create_app()


@celery_app.task
def get_receipt():
    with flask_app.app_context():
        receipt_get_handler()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/2'), get_receipt.s())