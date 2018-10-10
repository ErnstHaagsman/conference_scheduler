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
from django.urls import path, include, re_path

from scheduler.views import TalkListView, TalkReprioritizeView, TalkDeleteView, TalkAddView

urlpatterns = [
    path('<slug:event_slug>/talks/', TalkListView.as_view(), name='talk_list'),
    path('<slug:event_slug>/talks/add', TalkAddView.as_view(), name='talk_add'),
    re_path(
        '(?P<event_slug>\w+)/talks/(?P<talk_id>\d+)/(?P<direction>up|down)',
        TalkReprioritizeView.as_view(),
        name='talk_reprioritize'),
    path('<slug:event_slug>/talks/<int:talk_id>/delete', TalkDeleteView.as_view(), name='talk_delete'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
