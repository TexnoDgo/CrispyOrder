# Python
import requests
import json
# Django
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Apps
# -----
# Local
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CompanyProfileCreateForm,ProfileNotificationForm
from .models import Profile, CompanyProfile

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        #  Сообщение об успешной регистрации
        if form.is_valid():
            form.save()  # Сохранение  формы
            username = form.cleaned_data.get('username')  # Получение имени из формы
            messages.success(request, f'You account has been created! You are now able to log in')  # Формирование сообщения со вложенным именем
            return redirect('conf_reg')  # Перенаправление на страницу подтверждения регистрации
    else:
        form = UserRegisterForm()
    return render(request, 'users/singup.html', {'form': form})


def conf_reg(request):
    return render(request, 'users/conf_reg.html')


def profile_view(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = CompanyProfileCreateForm(request.POST)

        if form.is_valid():
            company_profile = form.save(commit=False)

            # -----API-----
            empty_field = 'edrpou'
            value = company_profile.edrpou
            print(value)
            prelink = '{%22' + empty_field + '%22:%22' + value + '%22}'
            print(prelink)
            link = 'http://edr.data-gov-ua.org/api/companies?where=' + prelink
            print('link:' + link)
            response = requests.get(link)
            data = json.loads(response.text)
            print(data)
            first = data[0]
            print(first)
            # -----API-----
            company_profile.user_name = request.user
            company_profile.name = first["name"]
            company_profile.officialName = first["officialName"]
            company_profile.address = first["address"]
            company_profile.mainPerson = first["mainPerson"]
            company_profile.occupation = first["occupation"]
            company_profile.status = first["status"]
            company_profile.save()

            return redirect('/')
    else:
        form = CompanyProfileCreateForm()

    try:
        company = CompanyProfile.objects.get(user_name=request.user)
    except:
        company = None
    context = {
        'profile_view': profile,
        'company': company,
        'form': form,
    }
    return render(request, 'users/profile.html', context)


@login_required
def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,
                             f'Your account has been update!')  # Формирование сообщения Alert
            return redirect('profile_update')  # Перенаправление на страницу Профиля

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile_view': profile,
    }

    return render(request, 'users/profile_update.html', context)


class UserListViews(ListView):
    model = User


def createCompanyProfile(request):
    if request.method == 'POST':
        form = CompanyProfileCreateForm(request.POST)

        if form.is_valid():
            company_profile = form.save(commit=False)

            # -----API-----
            empty_field = 'edrpou'
            value = company_profile.edrpou
            print(value)
            prelink = '{%22' + empty_field + '%22:%22' + value + '%22}'
            print(prelink)
            link = 'http://edr.data-gov-ua.org/api/companies?where=' + prelink
            print('link:' + link)
            response = requests.get(link)
            data = json.loads(response.text)
            print(data)
            first = data[0]
            print(first)
            # -----API-----
            company_profile.user_name = request.user
            company_profile.name = first["name"]
            company_profile.officialName = first["officialName"]
            company_profile.address = first["address"]
            company_profile.mainPerson = first["mainPerson"]
            company_profile.occupation = first["occupation"]
            company_profile.status = first["status"]
            company_profile.save()

            return redirect('orders')
    else:
        form = CompanyProfileCreateForm()
    return render(request, 'users/company_profile_create.html', {'form': form})


@login_required
def set_up_notifications(request):
    if request.method == 'POST':
        form = ProfileNotificationForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = ProfileNotificationForm(instance=request.user.profile)
    context = {
        'form': form,
    }
    return render(request, 'users/set-up-notifications.html', context)


def signup(request):
    all_users = User.objects.all()
    users_email = []
    for one_user in all_users:
        users_email.append(one_user.email)
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'users_email': users_email,
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')