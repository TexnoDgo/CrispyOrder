from django import forms
from orders.models import CODOrder
from .models import CODSuggestion


class CreateSuggestionForm(forms.ModelForm):
    class Meta:
        model = CODSuggestion
        fields = ['offer_description', 'deadline', 'offer_price']
