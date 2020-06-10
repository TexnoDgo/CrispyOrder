# Python
# ----
# Django
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
# Apps
from orders.models import CODOrder
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
    count = 0
    count2 = 0
    count3 = 0
    count4 = 0
    # Предложения
    count5 = 0
    count6 = 0
    count7 = 0
    count8 = 0

    for order in user_order:
        count += 1
        if order.status == 'In work':
            count2 += 1
        elif order.status == 'Done':
            count3 += 1
        elif order.status == 'In discussion':
            count4 += 1

    for sug in user_suggestion:
        count5 += 1
        if sug.status == 'In work':
            count6 += 1
        elif sug.status == 'Done':
            count7 += 1
        elif sug.status == 'In discussion':
            count8 += 1
    context = {
        'sort_order_and_suggestion_dict': sort_order_and_suggestion_dict,
        'user_order': user_order,
        'user_suggestion': user_suggestion,
        'order_len': order_len,
        'suggestion_len': suggestion_len,
        'user_profile': user_profile,
        # Счетчики заказов
        'user_order_count': count,
        'user_order_count_in_work': count2,
        'user_order_count_ready': count3,
        'user_order_count_dis': count4,
        # Счетчики предложений
        'user_suggestion_count': count5,
        'user_suggestion_count_in_work': count6,
        'user_suggestion_count_ready': count7,
        'user_suggestion_count_dis': count8,
    }
    return render(request, 'dashboard/dashboard.html', context)


def dashboard_order(request):
    order = CODOrder.objects.filter(author=request.user)

    paginator = Paginator(order, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)
    context = {
        'orders': order,
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

    suggestions = CODSuggestion.objects.filter(author=request.user)

    orders = CODOrder.objects.all()

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
