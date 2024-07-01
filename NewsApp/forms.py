# newsapp/forms.py
from django import forms
from .models import News
import requests

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'intro', 'status', 'source_link']

    def save(self, commit=True):
        news_instance = super().save(commit=False)
        ai_status = self.get_ai_status(news_instance.intro)
        news_instance.ai_status = ai_status
        if commit:
            news_instance.save()
        return news_instance

    def get_ai_status(self, intro):
        url = "https://api.textcortex.com/v1/texts/completions"
        headers = {
            "Authorization": "Bearer gAAAAABmgwkdm-ZC21HMwnUZyR5CJjVXKisxVeFBxLIxAJwJjCCKMCLBot0hS-PBv4xyv0r8gABxFrf0QZJQ2jbkL70ikDtN9WOztvqsyOW9QKGFIElZgoI6oIHzXbRmXdGPP76-Gc1-",
            "Content-Type": "application/json"
        }
        data = {
            "formality": "default",
            "max_tokens": 2048,
            "model": "claude-3-haiku",
            "n": 1,
            "source_lang": "ru",
            "target_lang": "ru",
            "temperature": None,
            "text": f"Определите тон новости, это плохая или хорошая новость? Если хорошая то возвращай ответ good если плохая новость то возвращай ответ bad. Возвращаешь только good или bad. {intro}"
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            ai_response = response.json()
            ai_content = ai_response['data']['outputs'][0]['text'].strip().lower()
            if ai_content in ['good', 'bad']:
                return ai_content
        return 'needs_review'
