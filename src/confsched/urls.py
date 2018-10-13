"""confsched URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path

from scheduler.views import TalkListView, TalkReprioritizeView, TalkDeleteView, TalkAddView, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<slug:event_slug>/talks/', TalkListView.as_view(), name='talk_list'),
    path('<slug:event_slug>/talks/add', TalkAddView.as_view(), name='talk_add'),
    re_path(
        '(?P<event_slug>\w+)/talks/(?P<talk_id>\d+)/(?P<direction>up|down)',
        TalkReprioritizeView.as_view(),
        name='talk_reprioritize'),
    path('<slug:event_slug>/talks/<int:talk_id>/delete', TalkDeleteView.as_view(), name='talk_delete'),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             success_url='/',
             post_reset_login=True
         ),
         name='password_reset_confirm'),
]
