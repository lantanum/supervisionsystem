# newsapp/cron.py
from .scraper import fetch_news

def my_scheduled_job():
    fetch_news()
