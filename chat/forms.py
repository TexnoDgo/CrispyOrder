from django import forms
from .models import Message, CODMessage


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']


class CODMessageCreateForm(forms.ModelForm):
    class Meta:
        model = CODMessage
        fields = ['message']
