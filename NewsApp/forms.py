# newsapp/forms.py
from django import forms
from django.contrib.auth.models import User

from .models import News, Profile, Bank, Manager
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
            "Authorization": "Bearer gAAAAABmmVXaqnu4t9AkjgGKghEOZQMInu5iaA6vqioGy9nWZwu_oIQHbreGPIP-GvyHmmPAQHA5Xom_ox8Wgu8jxTcRLqKjagZ9nL_AfQzdV6BAh5HT3DEzw0I6nF0P2Y4-SgjWpCji",
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

class ManagerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_staff = True  # Сделать пользователя менеджером
        if commit:
            user.save()
            Manager.objects.create(user=user)
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']

class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=False, label='Поиск')


class NewsStatusForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['status']

class BankCreationForm(forms.ModelForm):
    manager = forms.ModelChoiceField(
        queryset=Manager.objects.all(),
        required=False,
        label='Manager',
        widget=forms.Select()
    )

    class Meta:
        model = Bank
        fields = ['name', 'ceo', 'manager']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manager'].queryset = Manager.objects.all().select_related('user')
        self.fields['manager'].label_from_instance = lambda obj: f"{obj.user.last_name} {obj.user.first_name}"


class BankManagerForm(forms.ModelForm):
    manager = forms.ModelChoiceField(
        queryset=Manager.objects.all(),
        required=False,
        label='Manager',
        widget=forms.Select()
    )

    class Meta:
        model = Bank
        fields = ['manager']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manager'].queryset = Manager.objects.all().select_related('user')
        self.fields['manager'].label_from_instance = lambda obj: f"{obj.user.last_name} {obj.user.first_name}"


class ManageBanksForm(forms.ModelForm):
    banks = forms.ModelMultipleChoiceField(
        queryset=Bank.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Banks"
    )

    class Meta:
        model = Manager
        fields = ['banks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['banks'].label_from_instance = lambda obj: obj.name