# newsapp/tasks.py
from celery import shared_task
from .scraper import fetch_news

@shared_task
def scrape_news():
    fetch_news()
