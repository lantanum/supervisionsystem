# newsapp/models.py
from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200)  # Заголовок
    intro = models.TextField()  # Вводная часть новости
    status_choices = [
        ('good', 'Хорошая'),
        ('needs_review', 'Требует проверки'),
        ('bad', 'Плохая'),
    ]
    status = models.CharField(max_length=15, choices=status_choices, default='needs_review')  # Статус новости
    source_link = models.URLField()  # Ссылка на источник
    ai_status = models.CharField(max_length=15, choices=status_choices, blank=True, null=True)  # Статус ИИ

    def __str__(self):
        return self.title
