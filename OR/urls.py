from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from HomePage.views import index, index2
from chat import views as chat_views
from users import views as user_views
from orders import views as orders_views

from chat import views as chat_views

from django.conf.urls import include

urlpatterns = [
    path('', index, name='index'),
    path('example/', index2, name='index2'),

    path('register/', user_views.register, name='register'),
    path('all_users/', user_views.UserListViews.as_view(), name='all_users'),


    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('account/', include('allauth.urls')),
    path('profile/set-up-notifications/', user_views.set_up_notifications, name='set-up-notifications'),

    path('admin/', admin.site.urls),

    path('orders/', include('orders.urls')),
    path('suggestions/', include('suggestions.urls')),
    path('profile/', include('users.urls')),
    path('dashboard/', include('dashboard.urls')),

    path('', include('chat.urls')),
    path('conf_reg/', user_views.conf_reg, name='conf_reg'),

    url(r'send_order_to_friend/(?P<pk>\d+)$', orders_views.send_order_to_friend, name='send_order_to_friend'),

    url(r'^signup/$', user_views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        user_views.activate, name='activate'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

