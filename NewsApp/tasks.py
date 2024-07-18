from datetime import datetime
from .management.commands.scrape_news import fetch_news, update_news_ai_status


def my_scheduled_task():
    fetch_news()
    print(f"Scheduled task is running at {datetime.now()}")

def my_scheduled_task_2():
    update_news_ai_status()
    print(f"Scheduled task is running at {datetime.now()}")