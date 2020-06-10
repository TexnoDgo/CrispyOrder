from django.views.generic import DetailView
from django.conf.urls import url
from django.urls import path, re_path
from .views import index, dashboard_order, dashboard_order_dis, dashboard_order_ready, dashboard_sug_active, dialogsView
from orders import views
from orders.models import CODOrder
from dashboard import views as das_views

urlpatterns = [
    path('', index, name='dashboard'),

    path('dashboard-order/', dashboard_order, name='dashboard-order'),
    path('dashboard-messages/', dialogsView, name='dashboard-messages'),
    path('dashboard-message-view/<slug:url>/', das_views.messages, name='dashboard-message-view'),

    path('dashboard-sug/active/', dashboard_sug_active, name='dashboard_sug_active'),

    path('dashboard-order/<slug:url>/', views.OrderAndSuggestionView.as_view(model=CODOrder,
                                                                                  template_name='orders/order.html'),
            name='order_detail'),
]
