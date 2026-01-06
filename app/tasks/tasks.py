import time
from app.celery import celery_app



@celery_app.task
def debug_task(time_to_sleep):
    time.sleep(time_to_sleep)
    return True

