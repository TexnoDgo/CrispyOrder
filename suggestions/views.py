from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from orders.models import CODOrder
from chat.models import CODMessage
from chat.forms import CODMessageCreateForm
from .forms import CreateSuggestionForm
from .models import CODSuggestion


@login_required
def create_suggestion(request, url):
    order = CODOrder.objects.get(pk=url)

    if request.method == 'POST':
        form = CreateSuggestionForm(request.POST)

        if form.is_valid():
            print('sug')
            suggestion = form.save(commit=False)
            suggestion.author = request.user
            suggestion.order = order
            suggestion.save()
            return redirect('order_and_suggestion_view', url=url)
    else:
        form = CreateSuggestionForm()

    context = {
        'order': order,
        'form': form,
    }

    return render(request, 'suggestions/create_suggestion.html', context)


@login_required
def suggestion_detail(request, url):
    suggestion = CODSuggestion.objects.get(pk=url)
    order = CODOrder.objects.get(pk=suggestion.order.pk)
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
        'suggestion': suggestion,
        'form': form,
        'order': order,
    }
    return render(request, 'suggestions/suggestion_view.html', context)
