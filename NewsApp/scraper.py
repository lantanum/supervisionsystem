import requests
from bs4 import BeautifulSoup
from .models import News
from .forms import NewsForm

def fetch_news():
    base_url = "https://www.zakon.kz/api/today-news/"
    params = {
        'pn': 1,
        'pSize': 20
    }

    while True:
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch news data with status code {response.status_code}")
            break

        data = response.json()
        news_list = data.get('data_list', [])

        for item in news_list:
            try:
                title = item.get('page_title')
                alias = item.get('alias')
                source_link = f"https://www.zakon.kz/{alias}"

                # Сохранение только тех новостей, в которых 'alias' содержит 'finansy'
                if 'finansy' not in alias:
                    continue

                # Проверка на дублирование по source_link
                if News.objects.filter(source_link=source_link).exists():
                    print(f"News with source link {source_link} already exists")
                    continue

                # Получение полного текста новости
                full_text_response = requests.get(source_link)
                if full_text_response.status_code != 200:
                    print(f"Failed to fetch full article from {source_link} with status code {full_text_response.status_code}")
                    continue

                full_soup = BeautifulSoup(full_text_response.content, 'html.parser')
                intro_element = full_soup.find('div', class_='description')

                if intro_element:
                    intro = intro_element.text.strip()
                else:
                    intro = ""

                news = News(
                    title=title,
                    intro=intro,
                    source_link=source_link,
                    status='needs_review'
                )

                ai_status = NewsForm().get_ai_status(intro)
                news.ai_status = ai_status

                news.save()
                print(f"Saved news: {title}")
            except Exception as e:
                print(f"Error processing news item: {e}")
                continue

        # Переход к следующей странице, если она есть
        next_page = data.get('next')
        if not next_page:
            break

        # Обновление параметров запроса для следующей страницы
        params['pn'] += 1

if __name__ == "__main__":
    fetch_news()
