# Python
# ----
# Django
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
# Apps
from orders.models import CODOrder, CODCategories, CODCity
from orders.filter import OrdersFilter
from suggestions.models import CODSuggestion
from chat.models import CODMessage
from users.models import Profile
from chat.forms import CODMessageCreateForm
# Local
# ----


def index(request):
    user_order = CODOrder.objects.filter(author=request.user)
    user_suggestion = CODSuggestion.objects.filter(author=request.user)
    user_profile = Profile.objects.get(user=request.user)
    order_len = len(user_order)
    suggestion_len = len(user_suggestion)

    order_and_suggestion_dict = {}

    for order in user_order:
        order_date_create = str(order.date_create)
        order_date_create = order_date_create[:19].replace("-", "")
        order_and_suggestion_dict[order_date_create] = order

    for suggestion in user_suggestion:
        suggestion_date_create = str(suggestion.date_create)
        suggestion_date_create = suggestion_date_create[:19].replace("-", "")
        order_and_suggestion_dict[suggestion_date_create] = suggestion

    # Сортировка словаря
    sort_order_and_suggestion_dict = {}
    order_and_suggestion_list = list(order_and_suggestion_dict.keys())
    order_and_suggestion_list.sort(reverse=True)

    for element in order_and_suggestion_list:
        sort_order_and_suggestion_dict[element] = order_and_suggestion_dict[element]
    # Заказы

    order_created = 0
    order_discussion = 0
    order_inwork = 0
    order_done = 0
    order_canceled = 0
    # Предложения
    suggestion_created = 0
    suggestion_discussion = 0
    suggestion_inwork = 0
    suggestion_done = 0
    suggestion_canceled = 0


    for order in user_order:
        order_created += 1
        if order.status == 'Discussion':
            order_discussion += 1
        elif order.status == 'InWork':
            order_inwork += 1
        elif order.status == 'Done':
            order_done += 1
        elif order.status == 'Canceled':
            order_canceled += 1
        else:
            print('ERROR ORDER')

    for sug in user_suggestion:
        suggestion_created += 1
        if sug.status == 'Discussion':
            suggestion_discussion += 1
        elif sug.status == 'InWork':
            suggestion_inwork += 1
        elif sug.status == 'Done':
            suggestion_done += 1
        elif sug.status == 'Canceled':
            suggestion_canceled += 1
        else:
            print('ERROR SUGGESTION')

    context = {
        'sort_order_and_suggestion_dict': sort_order_and_suggestion_dict,
        'user_order': user_order,
        'user_suggestion': user_suggestion,
        'order_len': order_len,
        'suggestion_len': suggestion_len,
        'user_profile': user_profile,
        # Счетчики заказов

        'order_created': order_created,
        'order_discussion': order_discussion,
        'order_inwork': order_inwork,
        'order_done': order_done,
        'order_canceled': order_canceled,
        # Счетчики предложений
        'suggestion_created': suggestion_created,
        'suggestion_discussion': suggestion_discussion,
        'suggestion_inwork': suggestion_inwork,
        'suggestion_done': suggestion_done,
        'suggestion_canceled': suggestion_canceled,
    }
    return render(request, 'dashboard/dashboard.html', context)


def dashboard_order(request):

    page_count = 6

    categories = CODCategories.objects.all()
    city = CODCity.objects.all()

    order = CODOrder.objects.filter(author=request.user)
    Discussion_order = CODOrder.objects.filter(author=request.user, status='Discussion')
    InWork_order = CODOrder.objects.filter(author=request.user, status='InWork')
    Done_order = CODOrder.objects.filter(author=request.user, status='Done')
    Canceled_order = CODOrder.objects.filter(author=request.user, status='Canceled')

    Discussion_order_f = OrdersFilter(request.GET, queryset=Discussion_order.order_by('-date_create'))
    InWork_order_f = OrdersFilter(request.GET, queryset=InWork_order.order_by('-date_create'))
    Done_order_f = OrdersFilter(request.GET, queryset=Done_order.order_by('-date_create'))
    Canceled_order_f = OrdersFilter(request.GET, queryset=Canceled_order.order_by('-date_create'))

    Discussion_order_paginator = Paginator(Discussion_order_f.qs, page_count)
    InWork_order_paginator = Paginator(InWork_order_f.qs, page_count)
    Done_order_paginator = Paginator(Done_order_f.qs, page_count)
    Canceled_order_paginator = Paginator(Canceled_order_f.qs, page_count)

    page_number = request.GET.get('page')

    Discussion_order_obj = Discussion_order_paginator.get_page(page_number)
    InWork_order_obj = InWork_order_paginator.get_page(page_number)
    Done_order_obj = Done_order_paginator.get_page(page_number)
    Canceled_order_obj = Canceled_order_paginator.get_page(page_number)

    context = {
        'orders': order,

        'Discussion_order_obj': Discussion_order_obj,
        'InWork_order_obj': InWork_order_obj,
        'Done_order_obj': Done_order_obj,
        'Canceled_order_obj': Canceled_order_obj,

        'categories': categories,
        'city': city,

        'Discussion_order_f': Discussion_order_f,
        'InWork_order_f': InWork_order_f,
        'Done_order_f': Done_order_f,
        'Canceled_order': Canceled_order,
    }
    return render(request, 'dashboard/dashboard-order.html', context)


def dashboard_order_dis(request):
    order = CODOrder.objects.filter(author=request.user)

    paginator = Paginator(order, 3)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    context = {
        'order': posts,
    }
    return render(request, 'dashboard/dashboard-order-dis.html', context)


def dashboard_order_ready(request):
    order = CODOrder.objects.filter(author=request.user)

    paginator = Paginator(order, 3)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    context = {
        'order': posts,
    }
    return render(request, 'dashboard/dashboard-order-ready.html', context)


def dashboard_sug_active(request):

    page_count = 3

    suggestions = CODSuggestion.objects.filter(author=request.user)
    orders = CODOrder.objects.all()

    Discussion_suggestions = CODSuggestion.objects.filter(author=request.user, status='Discussion')
    InWork_suggestions = CODSuggestion.objects.filter(author=request.user, status='InWork')
    Done_suggestions = CODSuggestion.objects.filter(author=request.user, status='Done')
    Canceled_suggestions = CODSuggestion.objects.filter(author=request.user, status='Canceled')

    Discussion_suggestions_f = OrdersFilter(request.GET, queryset=Discussion_suggestions.order_by('-date_create'))
    InWork_suggestions_f = OrdersFilter(request.GET, queryset=InWork_suggestions.order_by('-date_create'))
    Done_suggestions_f = OrdersFilter(request.GET, queryset=Done_suggestions.order_by('-date_create'))
    Canceled_suggestions_f = OrdersFilter(request.GET, queryset=Canceled_suggestions.order_by('-date_create'))

    Discussion_suggestions_paginator = Paginator(Discussion_suggestions_f.qs, page_count)
    InWork_suggestions_paginator = Paginator(InWork_suggestions_f.qs, page_count)
    Done_suggestions_paginator = Paginator(Done_suggestions_f.qs, page_count)
    Canceled_suggestions_paginator = Paginator(Canceled_suggestions_f.qs, page_count)

    page_number = request.GET.get('page')

    Discussion_suggestions_obj = Discussion_suggestions_paginator.get_page(page_number)
    InWork_suggestions_obj = InWork_suggestions_paginator.get_page(page_number)
    Done_suggestions_obj = Done_suggestions_paginator.get_page(page_number)
    Canceled_suggestions_obj = Canceled_suggestions_paginator.get_page(page_number)

    paginator = Paginator(suggestions, 3)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    context = {
        'suggestions': suggestions,
        'orders': orders,

        'Discussion_suggestions_obj': Discussion_suggestions_obj,
        'InWork_suggestions_obj': InWork_suggestions_obj,
        'Done_suggestions_obj': Done_suggestions_obj,
        'Canceled_suggestions_obj': Canceled_suggestions_obj,
        }
    return render(request, 'dashboard/dashboard-sug-active.html', context)


def dialogsView(request):
    suggestions = CODSuggestion.objects.all()
    user_suggestions = CODSuggestion.objects.filter(author=request.user)
    order_suggestion = CODSuggestion.objects.filter(order__author=request.user)
    all_suggestions = {}

    # Сбор предложений пользователя
    for sug in user_suggestions:
        suggestion_date_create = str(sug.date_create)
        suggestion_date_create = suggestion_date_create[:19].replace("-", "")
        all_suggestions[suggestion_date_create] = sug
    # Сбор предложений заказа пользователя

    for sug in order_suggestion:
        suggestion_date_create = str(sug.date_create)
        suggestion_date_create = suggestion_date_create[:19].replace("-", "")
        all_suggestions[suggestion_date_create] = sug

    sort_suggestions = {}
    suggestion_list = list(all_suggestions.keys())
    suggestion_list.sort(reverse=True)

    for element in suggestion_list:
        sort_suggestions[element] = all_suggestions[element]

    print(sort_suggestions)

    context = {
        'suggestions': suggestions,
        'sort_suggestions': sort_suggestions,
    }
    return render(request, 'dashboard/dashboard-messages.html', context)


def messages(request, url):
    suggestions = CODSuggestion.objects.all()
    user_suggestions = CODSuggestion.objects.filter(author=request.user)
    order_suggestion = CODSuggestion.objects.filter(order__author=request.user)
    all_suggestions = {}

    # Сбор предложений пользователя
    for sug in user_suggestions:
        suggestion_date_create = str(sug.date_create)
        suggestion_date_create = suggestion_date_create[:19].replace("-", "")
        all_suggestions[suggestion_date_create] = sug
    # Сбор предложений заказа пользователя

    for sug in order_suggestion:
        suggestion_date_create = str(sug.date_create)
        suggestion_date_create = suggestion_date_create[:19].replace("-", "")
        all_suggestions[suggestion_date_create] = sug

    sort_suggestions = {}
    suggestion_list = list(all_suggestions.keys())
    suggestion_list.sort(reverse=True)

    for element in suggestion_list:
        sort_suggestions[element] = all_suggestions[element]

    suggestion = CODSuggestion.objects.get(pk=url)
    suggestion_order = CODOrder.objects.get(pk=suggestion.order.pk)
    if request.method == 'POST':
        form = CODMessageCreateForm(request.POST)
        if form.is_valid():
            mes_form = form.save(commit=False)
            mes_form.suggestion = suggestion
            # Выбор автора сообщения
            mes_form.member = request.user
            mes_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CODMessageCreateForm()

    message = CODMessage.objects.filter(suggestion_id=url)

    context = {
        'message1': message,
        'suggestions': suggestions,
        'suggestion': suggestion,
        'form': form,
        'suggestion_order': suggestion_order,
        'sort_suggestions': sort_suggestions,
    }
    return render(request, 'dashboard/dashboard-message-view.html', context)
