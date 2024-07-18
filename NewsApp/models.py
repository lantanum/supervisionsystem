from django.contrib.auth.models import User
from django.db import models

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    banks_managed = models.ManyToManyField('Bank', related_name='managers')

    def __str__(self):
        return self.user.username

class Bank(models.Model):
    name = models.CharField(max_length=255)
    ceo = models.CharField(max_length=255)
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_banks')

    def __str__(self):
        return self.name

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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class ScheduledTask(models.Model):
    name = models.CharField(max_length=255)
    next_run_time = models.DateTimeField()
    interval_minutes = models.IntegerField()

    def __str__(self):
        return self.name