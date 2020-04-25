from celery import Celery
from celery.schedules import crontab
from webapp import create_app
from webapp.receipt.utils.receipt_handler import add_receipt_db

celery_app = Celery('tasks', broker='redis://localhost:6379/1')

flask_app = create_app()


@celery_app.task
def get_receipt():
    """Adding detailed sales receipt information to database"""
    with flask_app.app_context():
        add_receipt_db()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Perform a periodic task"""
    sender.add_periodic_task(crontab(minute='*/2'), get_receipt.s())
