from django.urls import path

from . import views

urlpatterns = [
    path('check-user-group', views.CheckUserGroupView.as_view(), name='check-user-group'),
]
