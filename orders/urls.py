from django.views.generic import DetailView
from django.conf.urls import url
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import (all_cod_order_view, create_single_order, added_one_detail,
                    create_multiple_order, added_multiple_detail, order_and_suggestion_view,
                    CODDeleteOrderView, CODOrderUpdateView, change_status, create_xls_project,
                    CODDetailUpdate, CODDetailDelete)
from .models import CODOrder, CODDetail

urlpatterns = [
    path('view/', all_cod_order_view, name='all_cod_order_view'),
    path('create_single_order', create_single_order, name='create_single_order'),
    path('create_multiple_order', create_multiple_order, name='create_multiple_order'),
    path(r'views/single_detail/<slug:url>', added_one_detail, name='added_one_detail'),
    path(r'views/multiple_detail/<slug:url>', added_multiple_detail, name='added_multiple_detail'),
    path(r'view/<slug:url>', order_and_suggestion_view, name='order_and_suggestion_view'),
    # Status URL
    path(r'view/<slug:url>/change_status', change_status, name='change_status'),
    re_path(r'view/(?P<pk>\d+)/delete', CODDeleteOrderView.as_view(), name='cod_order_delete'),
    re_path(r'view/(?P<pk>\d+)/update', CODOrderUpdateView.as_view(model=CODOrder,
                                                                   template_name='orders/cod_update.html'),
            name='order_update'),
    path(r'view/<slug:url>/create_xls_project', create_xls_project, name='create_xls_project'),
    re_path(r'view/detail/(?P<pk>\d+)/update', CODDetailUpdate.as_view(model=CODDetail,
                                                                      template_name='orders/cod_detail_update.html'),
            name='cod_detail_update'),
    re_path(r'view/detail/(?P<pk>\d+)/delete', CODDetailDelete.as_view(), name='cod_detail_delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


