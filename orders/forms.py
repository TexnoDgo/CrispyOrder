from django import forms
#from .models import Order, Suggestion, File, MassOrder
from django.views.generic import CreateView
from django.forms import formset_factory, modelformset_factory
from django.forms.models import inlineformset_factory


from .models import CODCity, CODMaterial, CODCategories, CODOrder, CODDetail, CODFile


class SendOrderForm(forms.Form):
    email = forms.EmailField(label='Введите email')
    fields = ['email']


# -------------------------------------------------------NEW MODELS----------------------------------------------------
class SingleOrderCreateForm(forms.ModelForm):
    class Meta:
        model = CODOrder
        fields = ['title', 'description', 'pdf_cover', 'Categories', 'city', 'proposed_budget']

        def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)


class MultipleOrderCreateForm(forms.ModelForm):
    class Meta:
        model = CODOrder
        fields = ['title', 'description', 'archive', 'pdf_cover', 'Categories', 'city', 'proposed_budget']

        def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)


class AddedOneDetailForm(forms.ModelForm):

    class Meta:
        model = CODDetail
        fields = ['amount', 'material', 'whose_material',
                  'Note', 'Deadline', 'pdf', 'dxf', 'step', 'part']
# -------------------------------------------------------NEW MODELS----------------------------------------------------
