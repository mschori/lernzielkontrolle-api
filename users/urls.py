from django.urls import path

from . import views
from .views import AllTraineesView, SingleTraineeView, TraineeLearnDataView

urlpatterns = [
    path('check-user-group', views.CheckUserGroupView.as_view(), name='check-user-group'),
    path('trainees/', AllTraineesView.as_view({'get': 'list'}), name='trainees'),
    path('check-user-group', views.CheckUserGroupView.as_view(), name='check-user-group'),
    path('trainee/<int:pk>/', SingleTraineeView.as_view(), name='trainee-detail'),
    path('trainee/learn-data/<int:trainee_id>/', TraineeLearnDataView.as_view(), name='specific-trainee-learn-data'),

]
