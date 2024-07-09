import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import News, Profile
from .forms import NewsForm, ManagerRegistrationForm, UserEditForm, ProfileEditForm, SearchForm

@login_required
def home(request):
    news_list = News.objects.all()
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        if query:
            news_list = news_list.filter(title__icontains=query)

    return render(request, 'newsapp/home.html', {'news_list': news_list, 'search_form': search_form})

@login_required
def account(request):
    # Ensure profile exists
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('account')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'newsapp/account.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def analytics(request):
    return render(request, 'newsapp/analytics.html')

@login_required
def lists(request):
    return render(request, 'newsapp/lists.html')

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

@login_required
def add_manager(request):
    if request.method == 'POST':
        form = ManagerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lists')
    else:
        form = ManagerRegistrationForm()
    return render(request, 'newsapp/add_manager.html', {'form': form})

@login_required
@csrf_exempt
def change_news_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            news_id = data.get('news_id')
            status = data.get('status')
            news = News.objects.get(id=news_id)
            news.status = status
            news.save()
            return JsonResponse({'success': True})
        except News.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Новость не найдена.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Ошибка декодирования JSON.'}, status=400)
    return JsonResponse({'success': False, 'message': 'Неправильный метод запроса.'}, status=400)
