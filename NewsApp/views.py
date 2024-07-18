import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import News, Profile, Bank, Manager
from .forms import NewsForm, ManagerRegistrationForm, UserEditForm, ProfileEditForm, SearchForm, BankManagerForm, \
    BankCreationForm, ManageBanksForm


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

    # Ensure manager profile exists
    if not hasattr(request.user, 'manager'):
        Manager.objects.create(user=request.user)

    manager = request.user.manager

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        banks_form = ManageBanksForm(request.POST, instance=manager)
        if user_form.is_valid() and profile_form.is_valid() and banks_form.is_valid():
            user_form.save()
            profile_form.save()
            banks_form.save()
            return redirect('account')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        banks_form = ManageBanksForm(instance=manager)

    return render(request, 'newsapp/account.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'banks_form': banks_form,
        'manager': manager,
    })

@login_required
def analytics(request):
    return render(request, 'newsapp/analytics.html')


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

def lists(request):
    banks = Bank.objects.all()
    return render(request, 'newsapp/lists.html', {'banks': banks})

def update_bank_manager(request, bank_id):
    bank = get_object_or_404(Bank, id=bank_id)
    if request.method == 'POST':
        form = BankManagerForm(request.POST, instance=bank)
        if form.is_valid():
            form.save()
            return redirect('lists')
    else:
        form = BankManagerForm(instance=bank)
    return render(request, 'newsapp/update_bank_manager.html', {'form': form, 'bank': bank})

def create_bank(request):
    if request.method == 'POST':
        form = BankCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bank_list')
    else:
        form = BankCreationForm()
    return render(request, 'newsapp/create_bank.html', {'form': form})


@login_required
def remove_bank(request, bank_id):
    manager = request.user.manager
    bank = get_object_or_404(Bank, id=bank_id)
    manager.banks_managed.remove(bank)
    return redirect('account')