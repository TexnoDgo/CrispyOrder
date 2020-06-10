# Python
# ----
# Django
from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView, View
from django.db.models import Count
from django.contrib import messages
from django.http import HttpResponseRedirect
# Apps
from orders.models import Suggestion, Order
# Local
from .models import Message
from .forms import MessageCreateForm


def message_of_suggestion(request, pk):
    suggestion = Suggestion.objects.get(pk=pk)
    suggestion_order = Order.objects.get(pk=suggestion.order.pk)
    if request.method == 'POST':
        form = MessageCreateForm(request.POST)
        if form.is_valid():
            mes_form = form.save(commit=False)
            mes_form.suggestion = suggestion
            # Выбор автора сообщения
            mes_form.member = request.user
            mes_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = MessageCreateForm()

    message = Message.objects.filter(suggestion_id=pk)

    context = {
        'message1': message,
        'suggestion': suggestion,
        'form': form,
        'suggestion_order': suggestion_order,
    }
    return render(request, 'orders/suggestion_view.html', context)
