from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from learn_aim_check import views
from learn_aim_check.views import LearnCheckChartAPIView, ToggleTodoAPIView


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'learn-check', views.LearnAimViewSet, basename='learn-check')

# Rest API Routers
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('drf_auth.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/learn-check/chart/<int:pk>/', LearnCheckChartAPIView.as_view(), name='learn_check_chart'),
    path('api/v1/learn-aim/<int:pk>/toggle-todo/', ToggleTodoAPIView.as_view(),
         name='learn_aim_toggle_todo'),
    # path('api/v1/users/trainee-detail/<int:trainee_id>/', TraineeDetailView.as_view(), name='trainee_detail'),

]
