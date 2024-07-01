# newsapp/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import News
from .forms import NewsForm

@login_required
def home(request):
    news_list = News.objects.all()
    return render(request, 'newsapp/home.html', {'news_list': news_list})

@login_required
def account(request):
    return render(request, 'newsapp/account.html')

@login_required
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NewsForm()
    return render(request, 'newsapp/add_news.html', {'form': form})
