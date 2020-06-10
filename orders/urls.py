from django.views.generic import DetailView
from django.conf.urls import url
from .models import Order, MassOrder
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import (all_cod_order_view, create_single_order, added_one_detail,
                    create_multiple_order, added_multiple_detail, order_and_suggestion_view,
                    CODDeleteOrderView, CODOrderUpdateView, change_status, create_xls_project)
from .models import CODOrder

urlpatterns = [
    url(r'^(?P<pk>\d+)$', views.OrderAndSuggestionView.as_view(model=Order, template_name='orders/order.html'),
        name='order_detail'),
    url(r'^group_order/(?P<pk>\d+)$',
        views.GroupOrderAndSuggestionView.as_view(model=MassOrder,
                                                  template_name='orders/group_order.html'),
        name='group_order_detail'),

    path(r'<slug:url>/', views.order_categories, name='order_categories'),
    # url(r'^(?P<pk>\d+)/update/', views.OrderUpdateView.as_view(model=Order, template_name='orders/update.html'),
    # name='order_update'),
    #url(r'^(?P<pk>\d+)/delete/', views.DeleteOrderView.as_view(), name='order_delete'),
    #url(r'^(?P<pk>\d+)/status_in_work/', views.status_in_work, name='status_in_work'),
    #url(r'^(?P<pk>\d+)/status_ready/', views.status_ready, name='status_ready'),
    #url(r'^(?P<pk>\d+)/get_one_rating/', views.get_one_rating, name='get_one_rating'),
    #url(r'^(?P<pk>\d+)/get_two_rating/', views.get_two_rating, name='get_two_rating'),
    #url(r'^(?P<pk>\d+)/get_three_rating/', views.get_three_rating, name='get_three_rating'),
    #url(r'^(?P<pk>\d+)/get_four_rating/', views.get_four_rating, name='get_four_rating'),
    #url(r'^(?P<pk>\d+)/get_five_rating/', views.get_five_rating, name='get_five_rating'),
    path('view', all_cod_order_view, name='all_cod_order_view'),
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

