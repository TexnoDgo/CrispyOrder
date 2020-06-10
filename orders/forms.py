from django import forms
from .models import Order, Suggestion, File, MassOrder
from django.views.generic import CreateView
from django.forms import formset_factory, modelformset_factory
from django.forms.models import inlineformset_factory


from .models import CODCity, CODMaterial, CODCategories, CODOrder, CODDetail, CODFile


class OrderCreateForm(forms.ModelForm):

    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Order
        fields = ['title', 'description', 'amount', 'city', 'lead_time', 'pdf_view', 'image_view', 'proposed_budget',
                  'activity', 'categories', 'files']

        # Привязка авторезированого пользователя к автору заказа
        def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)


class OrderUpdateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['title', 'description', 'amount', 'city', 'lead_time', 'image_view', 'pdf_view', 'proposed_budget',
                  'status', 'categories']


class CreateGroupOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['title', 'description', 'city', 'lead_time', 'pdf_view', 'proposed_budget']


class SuggestionCreateForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['offer_description', 'deadline', 'offer_price']


# -------------------------------------------------------------------------------
class GroupCreateOrderForm(forms.ModelForm):
    class Meta:
        model = MassOrder
        fields = ['other_files', 'title', 'description', 'city', 'lead_time', 'proposed_budget', 'crushed_order']

        def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)


class UpdateGroupOrderForm(forms.ModelForm):
    class Meta:
        pass
# --------------------------------------------------------------------------------


class SendOrderForm(forms.Form):
    email = forms.EmailField(label='Введите email')
    fields = ['email']


# -------------------------------------------------------NEW MODELS----------------------------------------------------
class SingleOrderCreateForm(forms.ModelForm):
    class Meta:
        model = CODOrder
        fields = ['title', 'description', 'pdf_cover', 'city', 'proposed_budget']

        def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)


class MultipleOrderCreateForm(forms.ModelForm):
    class Meta:
        model = CODOrder
        fields = ['title', 'description', 'archive', 'pdf_cover', 'city', 'proposed_budget']

        def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)


class AddedOneDetailForm(forms.ModelForm):

    class Meta:
        model = CODDetail
        fields = ['amount', 'material', 'whose_material',
                  'Note', 'Categories', 'Deadline', 'pdf', 'dxf', 'step', 'part']
# -------------------------------------------------------NEW MODELS----------------------------------------------------
