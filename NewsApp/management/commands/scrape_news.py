# newsapp/management/commands/scrape_news.py
from django.core.management.base import BaseCommand
from NewsApp.scraper import fetch_news, update_news_ai_status

class Command(BaseCommand):
    help = 'Fetch news from external websites and save to the database'

    def handle(self, *args, **kwargs):
        fetch_news()
        update_news_ai_status()
        self.stdout.write(self.style.SUCCESS('Successfully fetched and saved news articles'))
