from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, CompanyProfile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class CompanyProfileCreateForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        #fields = ['user', 'name', 'edrpou', 'officialName', 'address', 'mainPerson', 'occupation', 'status']
        fields = ['edrpou']

        # Привязка авторезированого пользователя к автору заказа
        def form_valid(self, form):
            form.instance.user_name = self.request.user
            return super().form_valid(form)


class ProfileNotificationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['notifications', 'notifi_account', 'notifi_email', 'notifi_sms', 'notifi_news',
                  'notifi_articles', 'notifi_updates', 'timing', 'categories']


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
        return self.cleaned_data
