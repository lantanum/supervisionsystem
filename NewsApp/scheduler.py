# scheduler/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import atexit

from .tasks import my_scheduled_task, my_scheduled_task_2

scheduler = BackgroundScheduler()

scheduler.add_job(
    my_scheduled_task,
    trigger=IntervalTrigger(minutes=60),
    id='my_scheduled_task',
    name='Run my scheduled task every 10 minute',
    replace_existing=True
)
scheduler.add_job(
    my_scheduled_task_2,
    trigger=IntervalTrigger(minutes=60),
    id='my_scheduled_task_2',
    name='Run my scheduled task every minute',
    replace_existing=True
)

def start():
    if not scheduler.running:
        scheduler.start()
        atexit.register(lambda: scheduler.shutdown())
