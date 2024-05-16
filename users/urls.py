from django.urls import path

from . import views
from .views import TraineeDetailView

urlpatterns = [
    path('check-user-group', views.CheckUserGroupView.as_view(), name='check-user-group'),
    path('trainee-list', views.TraineeListView.as_view(), name='trainee-list'),

]
