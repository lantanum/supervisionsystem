# newsapp/urls.py
from django.urls import path
from django.conf.urls.static import static

from NewsProject import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account/', views.account, name='account'),
    path('analytics/', views.analytics, name='analytics'),
    path('lists/', views.lists, name='lists'),
    path('add_news/', views.add_news, name='add_news'),
    path('add_manager/', views.add_manager, name='add_manager'),  # Новый URL для добавления менеджера
    path('change_news_status/', views.change_news_status, name='change_news_status'),
    path('banks/update_manager/<int:bank_id>/', views.update_bank_manager, name='update_bank_manager'),
    path('banks/create/', views.create_bank, name='create_bank'),
    path('remove_bank/<int:bank_id>/', views.remove_bank, name='remove_bank'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)